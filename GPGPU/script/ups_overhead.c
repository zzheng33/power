#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdint.h>
#include <time.h>

// Constants
#define MAX_RAPL_FILES 10
#define MONITOR_DURATION 40000  // Total monitoring duration in seconds
#define INTERVAL 0.3         // Interval between readings in seconds
#define OUTPUT_FILE "dram_ipc_monitor.csv"

// Structure to store monitoring data
typedef struct {
    double time;
    double dram_power;
    double ipc;
} PowerIpcData;

// Array to store paths to DRAM energy files
char *dram_energy_files[MAX_RAPL_FILES];
int num_dram_files = 0;

// Function to discover DRAM energy files from RAPL
void discover_dram_rapl_files() {
    const char *rapl_base_path = "/sys/class/powercap";
    char path[256];

    for (int socket_id = 0; socket_id < 2; socket_id++) {  // Adjust for more sockets if needed
        snprintf(path, sizeof(path), "%s/intel-rapl:%d/intel-rapl:%d:0/energy_uj", rapl_base_path, socket_id, socket_id);
        if (access(path, F_OK) == 0) {  // Check if the file exists
            dram_energy_files[num_dram_files] = strdup(path);
            if (dram_energy_files[num_dram_files] == NULL) {
                perror("Error duplicating path string");
                exit(EXIT_FAILURE);
            }
            num_dram_files++;
        }
    }

    if (num_dram_files == 0) {
        fprintf(stderr, "No DRAM energy files found. Exiting.\n");
        exit(EXIT_FAILURE);
    }
}

// Function to read DRAM energy in joules
double read_dram_energy() {
    double total_energy = 0;
    char buffer[32];

    for (int i = 0; i < num_dram_files; i++) {
        int fd = open(dram_energy_files[i], O_RDONLY);
        if (fd < 0) {
            perror("Error opening energy file");
            continue;
        }

        ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
        if (bytes_read <= 0) {
            perror("Error reading energy file");
            close(fd);
            continue;
        }
        buffer[bytes_read] = '\0';  // Null-terminate the string
        close(fd);

        total_energy += atof(buffer) / 1000000.0;  // Convert to joules
    }

    return total_energy;
}

// Function to collect IPC using perf
double collect_ipc() {
    FILE *fp = popen("perf stat -e instructions,cycles -a --no-merge --field-separator=, -x, sleep 0.05 2>&1", "r");
    if (fp == NULL) {
        perror("Error running perf command");
        return -1;
    }

    char line[256];
    double instructions = 0;
    double cycles = 0;

    while (fgets(line, sizeof(line), fp) != NULL) {
        if (strstr(line, "instructions")) {
            instructions = atof(strtok(line, ","));
        }
        if (strstr(line, "cycles")) {
            cycles = atof(strtok(line, ","));
        }
    }

    pclose(fp);
    return (cycles > 0) ? (instructions / cycles) : 0;
}

int main() {
    discover_dram_rapl_files();

    FILE *file = fopen(OUTPUT_FILE, "w");
    if (file == NULL) {
        perror("Error opening output file");
        exit(EXIT_FAILURE);
    }

    fprintf(file, "Time (s), DRAM Power (W), IPC\n");  // CSV Header
    printf("Monitoring DRAM Power and IPC for %d seconds...\n", MONITOR_DURATION);

    double start_energy = read_dram_energy();
    struct timespec start_time, current_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    int iterations = (int)(MONITOR_DURATION / INTERVAL);

    for (int i = 0; i < iterations; i++) {
        // usleep((int)(INTERVAL * 1000000));  // Convert to microseconds

        clock_gettime(CLOCK_MONOTONIC, &current_time);
        double elapsed_time = (current_time.tv_sec - start_time.tv_sec) +
                              (current_time.tv_nsec - start_time.tv_nsec) / 1.0e9;

        double current_energy = read_dram_energy();
        double dram_power = (current_energy - start_energy) / INTERVAL;  // Power = Energy / Time
        start_energy = current_energy;

        double ipc = collect_ipc();

        printf("Time: %.2f s | DRAM Power: %.2f W | IPC: %.3f\n", elapsed_time, dram_power, ipc);
        fprintf(file, "%.2f, %.2f, %.3f\n", elapsed_time, dram_power, ipc);
    }

    fclose(file);
    printf("Data saved to %s\n", OUTPUT_FILE);
    return 0;
}

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <stdint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <errno.h>


int dual_cap = 0;

typedef struct {
    double time_sec;
    double utilization;
} cpu_sample;


// void SoC(util) {
   
// }

void monitor_cpu_util(int pid, const char *output_csv, double interval) {
    // Initial capacity for data storage
    size_t capacity = 100000;
    size_t count = 0;
    cpu_sample *data = malloc(capacity * sizeof(cpu_sample));
    if (!data) {
        perror("malloc failed");
        exit(EXIT_FAILURE);
    }

    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);
    while (kill(pid, 0) == 0) {
            struct timespec current_time;
            clock_gettime(CLOCK_MONOTONIC, &current_time);
    
            double elapsed_time_ms = (current_time.tv_sec - start_time.tv_sec) * 1000.0 
                                     + (current_time.tv_nsec - start_time.tv_nsec) / 1e6;
            double elapsed_time_sec = elapsed_time_ms / 1000.0;
    
            // Run mpstat and capture the output
            FILE *fp = popen("mpstat", "r");
            if (!fp) {
                perror("popen failed");
                free(data);
                exit(EXIT_FAILURE);
            }
    
            char line[1024];
            double idle = -1.0;
            while (fgets(line, sizeof(line), fp)) {
                // The "all" line typically looks like:
                // Average:     all    2.44    0.02    0.28    0.11    0.00    0.00    0.00    0.00    0.00   97.16
                // or without "Average:" depending on distribution:
                // 10:09:44     all    2.44    0.02    0.28    0.11    0.00    0.00    0.00    0.00    0.00   97.16
                // We look for a line containing "all" and extract the last field as %idle.
                if (strstr(line, "all")) {
                    // mpstat output format: CPU   %usr %nice %sys %iowait %irq %soft %steal %guest %gnice %idle
                    // Typically 11 fields after 'all', we need the 12th field for %idle.
                    // We'll split by whitespace and find the last field
                    char *token;
                    char *saveptr;
                    int field_count = 0;
                    double fields[11];
                    char *tmp = strdup(line);
                    token = strtok_r(tmp, " \t\n", &saveptr);
    
                    // Scan through tokens until we find "all"
                    while (token != NULL) {
                        if (strcmp(token, "all") == 0) {
                            // Now read the next 10 fields for CPU stats
                            int idx = 0;
                            while ((token = strtok_r(NULL, " \t\n", &saveptr)) != NULL && idx < 10) {
                                fields[idx++] = atof(token);
                            }
                            // The last field in these 10 is %idle
                            idle = fields[9];
                            break;
                        }
                        token = strtok_r(NULL, " \t\n", &saveptr);
                    }
                    free(tmp);
                    break;
                }
            }
            pclose(fp);
    
            if (idle < 0) {
                // Could not find 'all' line or parse idle
                fprintf(stderr, "Warning: Could not parse mpstat output\n");
                idle = 100.0; // assume idle if error
            }
    
            double utilization = 100.0 - idle;
    
            // Store the sample
            if (count == capacity) {
                capacity *= 2;
                cpu_sample *new_data = realloc(data, capacity * sizeof(cpu_sample));
                if (!new_data) {
                    perror("realloc failed");
                    free(data);
                    exit(EXIT_FAILURE);
                }
                data = new_data;
            }
    
            data[count].time_sec = elapsed_time_sec;
            data[count].utilization = utilization;
            count++;
    
    
            // SoC(utilization);
            // Sleep for 0.2 seconds
            usleep((useconds_t)(interval * 1e6));
        }
    
        // Write all collected data to CSV
        FILE *fp_out = fopen(output_csv, "w");
        if (fp_out == NULL) {
            perror("Error opening CSV file");
            free(data);
            exit(EXIT_FAILURE);
        }
    
        // Write header
        fprintf(fp_out, "time,utilization\n");
    
        // Write each sample
        for (size_t i = 0; i < count; i++) {
            fprintf(fp_out, "%.2f,%.2f\n", data[i].time_sec, data[i].utilization);
        }
    
        fclose(fp_out);
        free(data);
}



int main(int argc, char *argv[]) {
    int pid = -1;
    const char *output_csv = NULL;
    double interval = 0.1;

    // Check if the arguments are in the form --param=value
    for (int i = 1; i < argc; i++) {
        if (strncmp(argv[i], "--pid=", 6) == 0) {
            pid = atoi(argv[i] + 6);
        } else if (strncmp(argv[i], "--output_csv=", 13) == 0) {
            output_csv = argv[i] + 13;
        } else if (strncmp(argv[i], "--dual_cap=", 11) == 0) {
            dual_cap = atoi(argv[i] + 11);
        } else {
            fprintf(stderr, "Unknown argument: %s\n", argv[i]);
            exit(EXIT_FAILURE);
        }
    }

    // Check if the required arguments were provided
    if (pid == -1 || output_csv == NULL) {
        fprintf(stderr, "Usage: %s --pid=<PID> --output_csv=<output_csv>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    monitor_cpu_util(pid, output_csv, interval);

    return 0;
}
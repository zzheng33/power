#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE 1000000000 // Adjust the size as per your requirement

void benchmark_copy(double *a, double *c, size_t size) {
    size_t i;

    // Perform the copy operation: Read from 'a' and Write to 'c'
    for (i = 0; i < size; i++) {
        c[i] = a[i];
    }
}

int main() {
    double *a, *c;
    size_t i;
    struct timespec start, end;
    double elapsed_time, total_bytes, bandwidth;

    // Allocate memory for the arrays
    a = (double*)malloc(ARRAY_SIZE * sizeof(double));
    c = (double*)malloc(ARRAY_SIZE * sizeof(double));

    if (a == NULL || c == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    // Initialize the arrays
    for (i = 0; i < ARRAY_SIZE; i++) {
        a[i] = 1.0; // Initialize 'a' with some value
        c[i] = 0.0; // Initialize 'c' with zeros
    }

    // Start the timer
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Perform the copy benchmark
    benchmark_copy(a, c, ARRAY_SIZE);

    // Stop the timer
    clock_gettime(CLOCK_MONOTONIC, &end);

    // Calculate elapsed time in seconds
    elapsed_time = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    // Print the elapsed time to see if it's a reasonable value
    printf("Elapsed time: %.9f seconds\n", elapsed_time);

    if (elapsed_time == 0) {
        printf("Elapsed time is zero, timing might be too fast for the resolution. Increase the array size.\n");
        free(a);
        free(c);
        return 1;
    }

    // Calculate total bytes transferred (reads from 'a' and writes to 'c')
    total_bytes = 2 * ARRAY_SIZE * sizeof(double); // 2 operations: read + write

    // Calculate bandwidth in MB/s
    bandwidth = total_bytes / (elapsed_time * 1e6); // Convert bytes to MB by dividing by 1e6

    // Print the results
    printf("Total bytes transferred: %.2f MB\n", total_bytes / 1e6);
    printf("Bandwidth: %.2f MB/s\n", bandwidth);

    // Free allocated memory
    free(a);
    free(c);

    return 0;
}

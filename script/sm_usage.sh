#!/bin/bash

# Output file where the results will be saved
OUTPUT_FILE="gpu_usage_log.txt"

# Clear the output file if it already exists
> $OUTPUT_FILE

echo "Starting GPU utilization logging to $OUTPUT_FILE every 0.1 seconds..."

# Infinite loop to query and log GPU utilization every 0.1 seconds
while true; do
    # Get the current date and time
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

    # Run nvidia-smi with query options to get a single snapshot of utilization
    OUTPUT=$(nvidia-smi --query-gpu=utilization.gpu,utilization.memory --format=csv,noheader,nounits)

    # Append the results to the output file with a timestamp
    echo "$TIMESTAMP, $OUTPUT" >> $OUTPUT_FILE

    # Wait for 0.1 seconds before the next iteration
    sleep 0.1
done

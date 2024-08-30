#!/bin/bash

# Check if at least two arguments are provided (CPU IDs and frequency)
if [ $# -lt 2 ]; then
    echo "Usage: $0 <CPU_IDs> <FREQUENCY>"
    echo "Example: $0 0 1 2.3GHz"
    exit 1
fi

# Extract the last argument as the frequency
FREQUENCY=${@: -1}

# Extract all but the last argument as CPU IDs
CPU_IDS=${@:1:$#-1}

# Iterate over each CPU ID and apply the settings
for CPU_ID in $CPU_IDS; do
    # Set the governor to userspace for the specified CPU core
    sudo cpufreq-set -c $CPU_ID -g userspace
    
    # Set the desired frequency for the specified CPU core using cpufreq-set
    sudo cpufreq-set -c $CPU_ID -f $FREQUENCY

    echo "CPU $CPU_ID frequency set to $FREQUENCY"
done

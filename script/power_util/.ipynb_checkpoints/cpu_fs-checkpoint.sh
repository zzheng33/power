#!/bin/bash

# Check if at least two arguments are provided (CPU IDs and frequency)
if [ $# -lt 2 ]; then
    echo "Usage: $0 <CPU_IDs> <FREQUENCY>"
    echo "Example: $0 0 1 2.4GHz"
    exit 1
fi

# Extract the last argument as the frequency
FREQUENCY=${@: -1}

# Remove the "GHz" suffix and convert to a floating-point number for comparison
FREQUENCY_NUM=$(echo $FREQUENCY | sed 's/GHz//' | bc)

# Check if the frequency is within the allowed range (0.8 GHz to 2.2 GHz)
if (( $(echo "$FREQUENCY_NUM < 0.8" | bc -l) )) || (( $(echo "$FREQUENCY_NUM > 2.2" | bc -l) )); then
    echo "Error: Frequency must be between 0.8 GHz and 2.2 GHz"
    exit 1
fi

# Extract all but the last argument as CPU IDs
CPU_IDS=${@:1:$#-1}

# Iterate over each CPU ID and apply the settings
for CPU_ID in $CPU_IDS; do
    # Set the governor to userspace for the specified CPU core
    sudo cpufreq-set -c $CPU_ID -g userspace
    
    # Set the desired frequency for the specified CPU core
    sudo cpupower -c $CPU_ID frequency-set -f $FREQUENCY

    echo "CPU $CPU_ID frequency set to $FREQUENCY"
done

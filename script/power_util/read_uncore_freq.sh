#!/bin/bash

# Function to read the uncore frequency from the MSR 0x621
read_uncore_frequency() {
    CPU_ID=$1
    MSR_VALUE=$(sudo rdmsr -p $CPU_ID 0x621)

    # Extract the lower 8 bits of the MSR value to get the current uncore frequency ratio
    UNCORE_RATIO=$((MSR_VALUE & 0xFF))

    # Calculate the uncore frequency in GHz (Ratio * 100 MHz / 1000)
    UNCORE_FREQUENCY=$(echo "scale=2; $UNCORE_RATIO / 10" | bc)

    echo "CPU $CPU_ID uncore frequency: $UNCORE_FREQUENCY GHz"
}

# Read uncore frequency for CPU 0
read_uncore_frequency 0

# Read uncore frequency for CPU 1
read_uncore_frequency 1

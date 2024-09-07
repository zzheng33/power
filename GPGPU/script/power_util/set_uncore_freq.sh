#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <FREQUENCY_GHz>"
    echo "Example: $0 2.2"
    exit 1
fi

# Assign the argument to a variable
FREQUENCY_GHZ=$1

# Check if the frequency is within the allowed range (0.8 GHz to 2.2 GHz)
if (( $(echo "$FREQUENCY_GHZ < 0.8" | bc -l) )) || (( $(echo "$FREQUENCY_GHZ > 2.4" | bc -l) )); then
    echo "Error: Frequency must be between 0.8 GHz and 2.4 GHz"
    exit 1
fi

# Calculate the ratio (frequency in GHz * 10)
# The base clock is typically 100 MHz, so a 1 GHz ratio is 10
RATIO=$(echo "$FREQUENCY_GHZ * 10" | bc | awk '{printf "%d\n", $1}')

# Convert the ratio to hexadecimal
RATIO_HEX=$(printf '%02X' $RATIO)

# Combine the ratio for both min and max (min=max)
COMBINED_HEX="0x${RATIO_HEX}${RATIO_HEX}"

# Write to MSR 0x620 for both CPU 0 and CPU 1
sudo wrmsr -p 0 0x620 $COMBINED_HEX
sudo wrmsr -p 1 0x620 $COMBINED_HEX

# echo "Set uncore frequency to $FREQUENCY_GHZ GHz (Hex: $COMBINED_HEX) for CPU 0 and 1"


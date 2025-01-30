#!/bin/bash

# Define the directory where the files are located
dir="/home/cc/power/GPGPU/data/altis_power_res/no_power_shift/magus_comb"

# Iterate over all .csv files in the directory
for file in "$dir"/*.csv; do
    # Extract filename without the directory path
    filename=$(basename "$file")

    # Remove the first occurrence of ".csv" only
    new_filename="${filename/.csv/}"

    # Rename the file
    mv "$file" "$dir/$new_filename"
    echo "Renamed: $filename -> $new_filename"
done

echo "All files have been renamed."

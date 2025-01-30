#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb


# Define parameter ranges
inc_ts_vals=(100 200 300 400 500 600 700 800 900 1000)
dec_ts_vals=(100 200 300 400 500 600 700 800 900 1000)
burst_up_vals=(0.4 0.5 0.6 0.7 0.8 0.9 1.0)
burst_low_vals=(0.1 0.2 0.3)
memory_throughput_ts_vals=(40000 60000 80000 100000)

# Generate 9 unique random combinations
declare -A used_combinations
count=0

while [ $count -lt 9 ]; do
    inc_ts=${inc_ts_vals[$RANDOM % ${#inc_ts_vals[@]}]}
    dec_ts=${dec_ts_vals[$RANDOM % ${#dec_ts_vals[@]}]}
    burst_up=${burst_up_vals[$RANDOM % ${#burst_up_vals[@]}]}
    burst_low=${burst_low_vals[$RANDOM % ${#burst_low_vals[@]}]}
    memory_throughput_ts=${memory_throughput_ts_vals[$RANDOM % ${#memory_throughput_ts_vals[@]}]}

    key="${inc_ts}_${dec_ts}_${burst_up}_${burst_low}_${memory_throughput_ts}"

    if [[ -z "${used_combinations[$key]}" ]]; then
        used_combinations[$key]=1
        count=$((count + 1))

        echo "Running experiment with inc_ts=$inc_ts, dec_ts=$dec_ts, burst_up=$burst_up, burst_low=$burst_low, memory_throughput_ts=$memory_throughput_ts"

        python3 exp_power_motif.py --suite 1 --test 0 --dynamic_ufs_gpuP 0 \
            --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 \
            --inc_ts "$inc_ts" --dec_ts "$dec_ts" --history 5 --dual_cap 1 \
            --burst_up "$burst_up" --burst_low "$burst_low" \
            --memory_throughput_ts "$memory_throughput_ts" --ups 0 \
            --benchmark srad

        sleep 3

        # Move and rename the output CSV files
        target_dir="/home/cc/power/GPGPU/data/altis_power_res/no_power_shift/magus_comb"
        sudo mkdir -p "$target_dir"

        for file in /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/*.csv; do
            if [[ -f "$file" ]]; then
                filename=$(basename "$file" .csv)
                sudo mv "$file" "$target_dir/${filename}_${key}.csv"
            fi
        done
    fi
done







./power_util/set_uncore_freq.sh 2.2 2.2





TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;
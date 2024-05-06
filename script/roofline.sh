#!/bin/bash

# Source the oneAPI environment
source /home/cc/intel/oneapi/setvars.sh

# Array of NPB benchmarks
declare -a npb_benchmarks=("bt" "cg" "ep" "ft" "is" "lu" "mg" "sp" "ua")

# Loop through each benchmark
for app in "${npb_benchmarks[@]}"; do
    # Run advisor for Roofline collection
    advisor --collect=roofline --project-dir=/home/cc/advisor_res -- /home/cc/benchmark/CPU-only/NPB3.4.2/NPB3.4-OMP/bin/${app}.C.x

    # Generate Roofline report
    advisor --report=roofline --project-dir=/home/cc/advisor_res --report-output=/home/cc/advisor_res/roofline_${app}.html
done

echo "Advisor analysis and report generation completed."

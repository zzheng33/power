#!/bin/bash

# Define paths and executables
HOME_DIR=$(echo ~$USER)
PYTHON_EXECUTABLE=$(which python3)  # Adjust based on your Python version
MONITOR_SCRIPT_PATH="./monitor_cpu_power.py"
RUN_BENCHMARK_SCRIPT_PATH="./run_benchmark.py"

# Define your benchmarks
BENCHMARKS=('FT' 'CG' 'LULESH' 'Nekbone' 'AMG2013' 'miniFE')
# For testing, you can replace the above line with the following to just run 'LULESH'
# BENCHMARKS=('FT')

sudo modprobe msr
sudo sysctl -n kernel.perf_event_paranoid=-1

for BENCHMARK in "${BENCHMARKS[@]}"; do
    OUTPUT="../data/power_res/${BENCHMARK}_power.csv"  

    # Execute the benchmark and get its PID
    RUN_BENCHMARK_COMMAND="$PYTHON_EXECUTABLE $RUN_BENCHMARK_SCRIPT_PATH --benchmark $BENCHMARK"
    $RUN_BENCHMARK_COMMAND &
    BENCHMARK_PID=$!

    # Start power monitoring, passing the PID of the benchmark process
    MONITOR_COMMAND="echo 9900 | sudo -S $PYTHON_EXECUTABLE $MONITOR_SCRIPT_PATH --home_dir $HOME_DIR --output_csv $OUTPUT --pid $BENCHMARK_PID"
    
    # On cloudlab, you might use the following instead:
    # MONITOR_COMMAND="sudo $PYTHON_EXECUTABLE $MONITOR_SCRIPT_PATH --home_dir $HOME_DIR --output_csv $OUTPUT --pid $BENCHMARK_PID"

    $MONITOR_COMMAND &
    MONITOR_PID=$!

    # Wait for the benchmark process to complete
    wait $BENCHMARK_PID
    BENCHMARK_EXIT_CODE=$?
    if [ $BENCHMARK_EXIT_CODE -ne 0 ]; then
        echo "Benchmark $BENCHMARK failed"
    else
        echo "Completed benchmark: $BENCHMARK"
    fi

    # Here, the monitor process should stop automatically as the benchmark completes,
    # but if you need to stop it manually, uncomment the following line:
    # kill $MONITOR_PID
done

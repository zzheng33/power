import time
import os
import csv
import argparse
import psutil
import pandas as pd
from pynvml import nvmlInit, nvmlShutdown, nvmlDeviceGetHandleByIndex, nvmlDeviceGetPowerUsage, nvmlDeviceGetCount

# Initialize NVML
nvmlInit()

# Function to get current GPU power usage using pynvml
def get_gpu_power():
    try:
        device_count = nvmlDeviceGetCount()  # Get the number of GPUs
        power_draws = []
        for i in range(device_count):
            handle = nvmlDeviceGetHandleByIndex(i)
            power_draw = nvmlDeviceGetPowerUsage(handle) / 1000.0  # Convert milliwatts to watts
            power_draws.append(power_draw)
        return power_draws
    except Exception as e:
        print(f"Error getting GPU power usage: {e}")
        return []

# Function to monitor power consumption of all GPUs
def monitor_gpu_power(benchmark_pid, output_csv, avg, interval=0.1):
    start_time = time.time()
    power_data = []

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time

        gpu_powers = get_gpu_power()
        row = [elapsed_time] + gpu_powers
        power_data.append(row)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if avg:
        file_exists = os.path.isfile(output_csv)
        total_time = power_data[-1][0]  # Total elapsed time is the time value in the last row
        # Calculate average power for all GPUs and then total energy
        avg_power_all_gpus = sum([sum(p[i] for p in power_data) / len(power_data) for i in range(1, len(gpu_powers) + 1)])
        total_energy = round(avg_power_all_gpus * total_time, 2)  # Total energy for all GPUs
    
        with open(output_csv, 'a', newline='') as file:  # Open file in append mode
            writer = csv.writer(file)
            if not file_exists:  # If the file doesn't exist, add the header
                writer.writerow(['GPU_E (J)'])
            writer.writerow([total_energy])  # Append the total energy

    else:   
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            # Adjust the header based on the number of GPUs
            headers = ['Time (s)'] + [f'GPU {i} Power (W)' for i in range(len(gpu_powers))]
            writer.writerow(headers)
            writer.writerows(power_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor GPU power usage using pynvml.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    parser.add_argument('--avg', type=str, help='avg_power', default=0)
    args = parser.parse_args()

    monitor_gpu_power(args.pid, args.output_csv, args.avg)

    # Shutdown NVML after monitoring
    nvmlShutdown()

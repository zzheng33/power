import time
import os
import csv
import argparse
import psutil
import subprocess  # Import subprocess to run nvidia-smi

# Function to get current GPU power usage
def get_gpu_power():
    try:
        # Run the nvidia-smi command to get power usage, parse it
        smi_output = subprocess.check_output(['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'], encoding='utf-8')
        power_draw = float(smi_output.strip())  # Convert power draw from string to float
        return power_draw
    except Exception as e:
        print(f"Error getting GPU power usage: {e}")
        return 0

# Function to monitor power consumption of GPU
def monitor_gpu_power(benchmark_pid, output_csv, interval=0.1):
    start_time = time.time()
    power_data = []

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time

        gpu_power = get_gpu_power()

        power_data.append([elapsed_time, gpu_power])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'GPU Power (W)'])
        writer.writerows(power_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor GPU power usage using nvidia-smi.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    args = parser.parse_args()

    monitor_gpu_power(args.pid, args.output_csv)

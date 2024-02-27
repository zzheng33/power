import subprocess
import time
import os
import csv
import argparse
import psutil

# Parse command-line arguments for home directory and output CSV file
parser = argparse.ArgumentParser(description='Monitor CPU and DRAM power usage.')
parser.add_argument('--home_dir', type=str, help='User home directory', required=True)
parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
args = parser.parse_args()
benchmark_pid = args.pid

args = parser.parse_args()

home_directory = args.home_dir
output_csv = args.output_csv

def read_rapl_energy():
    # Paths for CPU and DRAM energy
    cpu_energy_path = '/sys/class/powercap/intel-rapl:0/energy_uj'
    dram_energy_path = '/sys/class/powercap/intel-rapl:0:2/energy_uj'
    
    with open(cpu_energy_path, 'r') as cpu_file:
        cpu_energy_uj = int(cpu_file.read().strip())
    
    with open(dram_energy_path, 'r') as dram_file:
        dram_energy_uj = int(dram_file.read().strip())

    return cpu_energy_uj, dram_energy_uj

# Function to monitor power consumption
def monitor_power(interval=1):  # Default duration 30 seconds, interval 1 seconds
    start_time = time.time()
    initial_cpu_energy, initial_dram_energy = read_rapl_energy()

    power_data = []  # List to store power data

    while True:
        if not psutil.pid_exists(benchmark_pid):
            print(f"Benchmark process with PID {benchmark_pid} has completed.")
            break  # Exit the loop if the benchmark process is not running anymore
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_cpu_energy, current_dram_energy = read_rapl_energy()

        cpu_energy_consumed = (current_cpu_energy - initial_cpu_energy) / 1_000_000  # Convert microjoules to joules
        dram_energy_consumed = (current_dram_energy - initial_dram_energy) / 1_000_000  # Convert microjoules to joules

        # Update initial energy for next iteration
        initial_cpu_energy, initial_dram_energy = current_cpu_energy, current_dram_energy

        cpu_average_power = cpu_energy_consumed / interval  # Power = Energy / Time
        dram_average_power = dram_energy_consumed / interval  # Power = Energy / Time

        # Append the time, CPU, and DRAM power data to the list
        power_data.append([elapsed_time, cpu_average_power, dram_average_power])

    # Write the collected power data to a CSV file
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Package Power (W)', 'DRAM Power (W)'])
        writer.writerows(power_data)

if __name__ == "__main__":
    monitor_power()  

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
home_directory = args.home_dir
output_csv = args.output_csv

# Constants for MSR
MSR_RAPL_POWER_UNIT = 0x606
MSR_PKG_ENERGY_STATUS = 0x611
MSR_DRAM_ENERGY_STATUS = 0x619  # Adjust this if the DRAM energy status register differs
ENERGY_UNITS_MASK = 0x1F00

def read_msr(msr):
    cpu = 0  # Assuming a single CPU system; adjust as needed.
    with open(f'/dev/cpu/{cpu}/msr', 'rb') as f:
        f.seek(msr)
        return int.from_bytes(f.read(8), 'little')

def get_energy_units():
    rapl_power_unit = read_msr(MSR_RAPL_POWER_UNIT)
    return 1 / (2 ** ((rapl_power_unit & ENERGY_UNITS_MASK) >> 8))

def read_rapl_energy(energy_units):
    cpu_energy_uj = read_msr(MSR_PKG_ENERGY_STATUS) * energy_units
    dram_energy_uj = read_msr(MSR_DRAM_ENERGY_STATUS) * energy_units
    return cpu_energy_uj, dram_energy_uj

# Function to monitor power consumption
def monitor_power(interval=0.1):
    energy_units = get_energy_units()
    start_time = time.time()
    initial_cpu_energy, initial_dram_energy = read_rapl_energy(energy_units)

    power_data = []  # List to store power data

    while True:
        if not psutil.pid_exists(benchmark_pid):
            print(f"Benchmark process with PID {benchmark_pid} has completed.")
            break  # Exit the loop if the benchmark process is not running anymore
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_cpu_energy, current_dram_energy = read_rapl_energy(energy_units)

        cpu_energy_consumed = (current_cpu_energy - initial_cpu_energy)  # Energy already in Joules
        dram_energy_consumed = (current_dram_energy - initial_dram_energy)  # Energy already in Joules

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
        writer.writerow(['Time (s)', 'CPU Power (W)', 'DRAM Power (W)'])
        writer.writerows(power_data)

if __name__ == "__main__":
    monitor_power()

import subprocess
import time
import os
import csv
import argparse
import psutil

# Constants for MSR
MSR_RAPL_POWER_UNIT = 0x606
MSR_PKG_ENERGY_STATUS = 0x611
MSR_DRAM_ENERGY_STATUS = 0x619  # Adjust this if the DRAM energy status register differs
ENERGY_UNITS_MASK = 0x1F00  # Ensure this mask is correct for your CPU model

# Function to read from a Model-Specific Register (MSR)
def read_msr(msr, cpu):
    try:
        with open(f'/dev/cpu/{cpu}/msr', 'rb') as f:
            f.seek(msr)
            return int.from_bytes(f.read(8), 'little')
    except FileNotFoundError:
        print(f"MSR file for CPU {cpu} not found.")
    except PermissionError:
        print(f"Permission denied when reading MSR for CPU {cpu}.")
    except Exception as e:
        print(f"Error reading MSR for CPU {cpu}: {e}")
    return 0  # Return 0 on error

# Function to calculate the energy units from MSR
def get_energy_units():
    cpu = 0  # Assuming we can use the first CPU to get global energy units
    raw_power_unit = read_msr(MSR_RAPL_POWER_UNIT, cpu)
    energy_units = (raw_power_unit & ENERGY_UNITS_MASK) >> 8
    return 1 / (2 ** energy_units)

# Function to read the current energy status
def read_rapl_energy(energy_units):
    cpu_count = len([name for name in os.listdir('/dev/cpu/') if name.isdigit()])
    total_cpu_energy = 0
    total_dram_energy = 0
    for cpu in range(cpu_count):
        total_cpu_energy += read_msr(MSR_PKG_ENERGY_STATUS, cpu)
        total_dram_energy += read_msr(MSR_DRAM_ENERGY_STATUS, cpu)
    return total_cpu_energy * energy_units, total_dram_energy * energy_units

# Main function to monitor power consumption
def monitor_power(benchmark_pid, output_csv, interval=0.1):
    energy_units = get_energy_units()
    start_time = time.time()
    initial_cpu_energy, initial_dram_energy = read_rapl_energy(energy_units)

   

    power_data = []

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_cpu_energy, current_dram_energy = read_rapl_energy(energy_units)

        cpu_energy_consumed = current_cpu_energy - initial_cpu_energy
        dram_energy_consumed = current_dram_energy - initial_dram_energy

        initial_cpu_energy, initial_dram_energy = current_cpu_energy, current_dram_energy

        cpu_power = cpu_energy_consumed / interval
        dram_power = dram_energy_consumed / interval

        power_data.append([elapsed_time, cpu_power, dram_power])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Time (s)', 'Package Power (W)', 'DRAM Power (W)'])
        writer.writerows(power_data)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Monitor CPU and DRAM power usage.')
    parser.add_argument('--home_dir', type=str, help='User home directory', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    args = parser.parse_args()

    monitor_power(args.pid, args.output_csv)

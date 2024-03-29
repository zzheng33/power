# import subprocess
# import time
# import os
# import csv
# import argparse
# import psutil

# # Constants for MSR
# MSR_RAPL_POWER_UNIT = 0x606
# MSR_PKG_ENERGY_STATUS = 0x611
# MSR_DRAM_ENERGY_STATUS = 0x619  # Adjust this if the DRAM energy status register differs
# ENERGY_UNITS_MASK = 0x1F00  # Ensure this mask is correct for your CPU model

# # Function to read from a Model-Specific Register (MSR)
# def read_msr(msr, cpu):
#     with open(f'/dev/cpu/{cpu}/msr', 'rb') as f:
#         f.seek(msr)
#         return int.from_bytes(f.read(8), 'little')
   

# # Function to calculate the energy units from MSR
# def get_energy_units():
#     cpu = 0  # Assuming we can use the first CPU to get global energy units
#     raw_power_unit = read_msr(MSR_RAPL_POWER_UNIT, cpu)
#     energy_units = (raw_power_unit & ENERGY_UNITS_MASK) >> 8
#     return 1 / (2 ** energy_units)

# # Function to read the current energy status
# def read_rapl_energy(energy_units):
#     cpu_count = len([name for name in os.listdir('/dev/cpu/') if name.isdigit()])
#     total_cpu_energy = 0
#     total_dram_energy = 0
#     for cpu in range(cpu_count):
#         total_cpu_energy += read_msr(MSR_PKG_ENERGY_STATUS, cpu)
#         total_dram_energy += read_msr(MSR_DRAM_ENERGY_STATUS, cpu)
#     return total_cpu_energy * energy_units, total_dram_energy * energy_units

# # Main function to monitor power consumption
# def monitor_power(benchmark_pid, output_csv, interval=0.1):
#     energy_units = get_energy_units()
#     start_time = time.time()
#     initial_cpu_energy, initial_dram_energy = read_rapl_energy(energy_units)

#     power_data = []

#     while psutil.pid_exists(benchmark_pid):
#         time.sleep(interval)
#         current_time = time.time()
#         elapsed_time = current_time - start_time
#         current_cpu_energy, current_dram_energy = read_rapl_energy(energy_units)

#         cpu_energy_consumed = current_cpu_energy - initial_cpu_energy
#         dram_energy_consumed = current_dram_energy - initial_dram_energy

#         initial_cpu_energy, initial_dram_energy = current_cpu_energy, current_dram_energy

#         cpu_power = cpu_energy_consumed / interval
#         dram_power = dram_energy_consumed / interval

#         power_data.append([elapsed_time, cpu_power, dram_power])

#     os.makedirs(os.path.dirname(output_csv), exist_ok=True)
#     with open(output_csv, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Time (s)', 'Package Power (W)', 'DRAM Power (W)'])
#         writer.writerows(power_data)

# if __name__ == "__main__":
#     # Parse command-line arguments
#     parser = argparse.ArgumentParser(description='Monitor CPU and DRAM power usage.')
#     parser.add_argument('--home_dir', type=str, help='User home directory', required=True)
#     parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
#     parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
#     args = parser.parse_args()

#     monitor_power(args.pid, args.output_csv)


import time
import os
import csv
import argparse
import psutil

# Constants for RAPL energy files specific to your system
RAPL_PATH = "/sys/class/powercap/"
def discover_rapl_sockets():
    rapl_path = "/sys/class/powercap/"
    energy_files = {}
    # Check and add energy files for existing sockets
    for socket_id in range(2):  # Assuming a maximum of two sockets for this example
        cpu_energy_file = os.path.join(rapl_path, f'intel-rapl:{socket_id}', 'energy_uj')
        if os.path.exists(cpu_energy_file):
            energy_files[f'cpu_socket{socket_id}'] = cpu_energy_file
    return energy_files

# Initialize ENERGY_FILES with available sockets
ENERGY_FILES = discover_rapl_sockets()


def read_energy(file_path):
    try:
        with open(file_path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return 0
    except PermissionError:
        print(f"Permission denied when reading the file {file_path}.")
        return 0
    except Exception as e:
        print(f"Error reading the file {file_path}: {e}")
        return 0
    
# Function to monitor power consumption updated to add socket powers together
def monitor_power(benchmark_pid, output_csv, avg, interval=0.1):
    start_time = time.time()
    initial_values = {key: read_energy(os.path.join(RAPL_PATH, path)) for key, path in ENERGY_FILES.items()}
    power_data = []
    tot = 0
    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_values = {key: read_energy(os.path.join(RAPL_PATH, path)) for key, path in ENERGY_FILES.items()}

        energy_consumed = {key: (current_values[key] - initial_values[key]) / 1_000_000 for key in ENERGY_FILES}  # Convert microjoules to joules
        initial_values = current_values

        # Sum the energy for the CPU sockets
        total_cpu_energy = sum(energy_consumed[key] for key in energy_consumed if 'cpu_socket' in key)
        tot += total_cpu_energy
        # Calculate individual power for DRAM or any other component if necessary
        # total_dram_energy = sum(energy_consumed[key] for key in energy_consumed if 'dram_socket' in key)
        # Convert energy to power
        cpu_power = total_cpu_energy / interval
        # dram_power = total_dram_energy / interval

        power_data.append([elapsed_time, cpu_power])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if avg:
        file_exists = os.path.isfile(output_csv)
        with open(output_csv, 'a', newline='') as file:  # Open file in append mode
            writer = csv.writer(file)
            if not file_exists:  # If the file doesn't exist, add the header
                writer.writerow(['CPU_E (J)'])
            writer.writerow([round(tot,2)])  # Append the total energy
    else:
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'Package Power (W)'])
            writer.writerows(power_data)

# Main function and argument parsing remains the same

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor total power usage using RAPL for all CPU sockets and DRAM.')
    parser.add_argument('--pid', type=int, help='PID of the benchmark process', required=True)
    parser.add_argument('--output_csv', type=str, help='Output CSV file path', required=True)
    parser.add_argument('--avg', type=str, help='avg_power', default=0)
    args = parser.parse_args()

    monitor_power(args.pid, args.output_csv,args.avg)

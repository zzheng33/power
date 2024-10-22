import time
import os
import csv
import argparse
import psutil

# Constants for RAPL energy files specific to your system
RAPL_PATH = "/sys/class/powercap/"

def discover_rapl_sockets():
    """Discover CPU and DRAM energy files from RAPL."""
    energy_files = {}
    # Check and add energy files for CPU sockets
    for socket_id in range(2):  # Assuming a maximum of two sockets for this example
        cpu_energy_file = os.path.join(RAPL_PATH, f'intel-rapl:{socket_id}', 'energy_uj')
        dram_energy_file = os.path.join(RAPL_PATH, f'intel-rapl:{socket_id}', 'intel-rapl:{socket_id}:0', 'energy_uj')
        
        if os.path.exists(cpu_energy_file):
            energy_files[f'cpu_socket{socket_id}'] = cpu_energy_file
        if os.path.exists(dram_energy_file):
            energy_files[f'dram_socket{socket_id}'] = dram_energy_file

    return energy_files

# Initialize ENERGY_FILES with available sockets
ENERGY_FILES = discover_rapl_sockets()

def read_energy(file_path):
    """Read the energy value from a given RAPL energy file."""
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

def monitor_power(benchmark_pid, output_csv, avg, interval=0.1):
    """Monitor power consumption for CPU sockets and DRAM."""
    start_time = time.time()
    initial_values = {key: read_energy(path) for key, path in ENERGY_FILES.items()}
    power_data = []
    total_cpu_energy = 0
    total_dram_energy = 0

    while psutil.pid_exists(benchmark_pid):
        time.sleep(interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        current_values = {key: read_energy(path) for key, path in ENERGY_FILES.items()}

        energy_consumed = {
            key: (current_values[key] - initial_values[key]) / 1_000_000  # Convert to joules
            for key in ENERGY_FILES
        }
        initial_values = current_values

        # Sum energy for CPU and DRAM sockets
        cpu_energy = sum(energy_consumed[key] for key in energy_consumed if 'cpu_socket' in key)
        dram_energy = sum(energy_consumed[key] for key in energy_consumed if 'dram_socket' in key)
        
        total_cpu_energy += cpu_energy
        total_dram_energy += dram_energy

        # Convert energy to power (Watts)
        cpu_power = cpu_energy / interval
        dram_power = dram_energy / interval

        power_data.append([elapsed_time, cpu_power, dram_power])

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if avg:
        file_exists = os.path.isfile(output_csv)
        with open(output_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['CPU_E (J)', 'DRAM_E (J)'])
            writer.writerow([round(total_cpu_energy, 2), round(total_dram_energy, 2)])
    else:
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'CPU Power (W)', 'DRAM Power (W)'])
            writer.writerows(power_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor power usage using RAPL for all CPU sockets and DRAM.')
    parser.add_argument('--pid', type=int, required=True, help='PID of the benchmark process')
    parser.add_argument('--output_csv', type=str, required=True, help='Output CSV file path')
    parser.add_argument('--avg', type=int, default=0, help='Collect average energy (1 for True, 0 for False)')
    args = parser.parse_args()

    monitor_power(args.pid, args.output_csv, args.avg)

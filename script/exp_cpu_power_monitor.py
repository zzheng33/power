import os
import subprocess

def main():
    home_dir = os.path.expanduser('~')
    python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version
    monitor_script_path = "./monitor_cpu_power.py"
    run_benchmark_script_path = "./run_benchmark.py"

    # Define your benchmarks here
    benchmarks = ['FT','CG','LULESH', 'Nekbone', 'AMG2013', 'miniFE']
    # For testing, you can uncomment the next line to just run 'LULESH'
    benchmarks = ['FT']

    for benchmark in benchmarks:
        output = f'../data/power_res/{benchmark}_power.csv'  # Append '_power.csv' to make it clear it's power data

        # Execute the benchmark and get its PID
        run_benchmark_command = f'{python_executable} {run_benchmark_script_path} --benchmark {benchmark}'
        benchmark_process = subprocess.Popen(run_benchmark_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Start power monitoring, passing the PID of the benchmark process
        monitor_command = f'echo 9900 | sudo -S {python_executable} {monitor_script_path} --home_dir {home_dir} --output_csv {output} --pid {benchmark_process.pid}'
        
        # Uncomment the line below in cloudlab (and ensure you handle password input securely)
        # monitor_command = f'sudo {python_executable} {monitor_script_path} --home_dir {home_dir} --output_csv {output} --pid {benchmark_process.pid}'
        monitor_process = subprocess.Popen(monitor_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for the benchmark process to complete
        stdout, stderr = benchmark_process.communicate()
        if benchmark_process.returncode != 0:
            print(f"Benchmark {benchmark} failed with error: {stderr.decode()}")

        # No need to manually stop the power monitoring as it should terminate once the benchmark completes
        # However, if needed, you can terminate it as follows:
        # monitor_process.terminate()
        print(f"Completed benchmark: {benchmark}")

if __name__ == "__main__":
    main()

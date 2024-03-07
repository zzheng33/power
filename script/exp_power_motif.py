import os
import subprocess
import time
import signal
import argparse


# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
read_cpu_power = "./power_util/read_cpu_power.py"
read_gpu_power = "./power_util/read_gpu_power.py"

# scritps for running various benchmarks
run_altis = "./run_benchmark/run_altis.py"
run_ecp = "./run_benchmark/run_ecp.py"

# Define your benchmarks, for testing replace the list with just ['FT'] for example
ecp_benchmarks = ['FT', 'CG', 'LULESH', 'Nekbone', 'AMG2013', 'miniFE']
altis_benchmarks_0 = ['busspeeddownload','busspeedreadback','maxflops']
altis_benchmarks_1 = ['bfs','gemm','gups','pathfinder','sort']
altis_benchmarks_2 = ['cfd','cfd_double','fdtd2d','kmeans','lavamd',
                      'nw','particlefilter_float','particlefilter_naive','raytracing',
                      'srad','where']




# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)


def run_benchmark(benchmark_dir,benchmark,test):
    if not test:
        output_cpu = f"../data/altis_power_res/{benchmark}_power_cpu.csv"
        output_gpu = f"../data/altis_power_res/{benchmark}_power_gpu.csv"
    else:
        output_cpu = f"../data/altis_test/{benchmark}_power_cpu.csv"
        output_gpu = f"../data/altis_test/{benchmark}_power_gpu.csv"
    
    # Execute the benchmark and get its PID
    run_benchmark_command = f"{python_executable} {run_altis} --benchmark {benchmark} --benchmark_dir {os.path.join(home_dir, benchmark_dir)}"
    benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
    benchmark_pid = benchmark_process.pid

    # Start CPU power monitoring, passing the PID of the benchmark process
    monitor_command_cpu = f"echo 9900 | sudo -S {python_executable} {read_cpu_power}  --output_csv {output_cpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)

    # Start GPU power monitoring, passing the PID of the benchmark process
    monitor_command_gpu = f"echo 9900 | sudo -S {python_executable} {read_gpu_power}  --output_csv {output_gpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_gpu, shell=True, stdin=subprocess.PIPE, text=True)

    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()

    if benchmark_exit_code != 0:
        print(f"Benchmark {benchmark} failed")
    else:
        print(f"Completed benchmark: {benchmark}")


def run_benchmark_ecp(benchmark, home_dir):
    output_cpu = f"../data/ecp_power_res/{benchmark}_power_cpu.csv"
    
    # Execute the benchmark and get its PID
    run_benchmark_command = f"{python_executable} {run_ecp} --benchmark {benchmark} --home_dir {home_dir}"
    benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
    benchmark_pid = benchmark_process.pid

    # Start CPU power monitoring, passing the PID of the benchmark process
    monitor_command_cpu = f"echo 9900 | sudo -S {python_executable} {read_cpu_power}  --output_csv {output_cpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)

    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()


if __name__ == "__main__":
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run benchmarks and monitor power consumption.')
    parser.add_argument('--benchmark', type=str, help='Optional name of the benchmark to run', default=None)
    parser.add_argument('--test', type=int, help='whether it is a test run', default=None)

    args = parser.parse_args()
    benchmark = args.benchmark
    test = args.test


    
    # # run ecp benchmarks
    # for app in ecp_benchmarks:
    #     run_benchmark_ecp(app, home_dir)
    
    # Map of benchmarks to their paths
    benchmark_paths = {
        "level0": altis_benchmarks_0,
        "level1": altis_benchmarks_1,
        "level2": altis_benchmarks_2
    }

    if benchmark:
        # Find which level the input benchmark belongs to
        found = False
        for level, benchmarks in benchmark_paths.items():
            if benchmark in benchmarks:
                path = f"power/script/altis_script/{level}"
                run_benchmark(path, benchmark,test)
                found = True
                break
    else:
        # # No benchmark specified, run all
        # for level, benchmarks in benchmark_paths.items():
        #     path = f"power/script/altis_script/{level}"
        #     for bm in benchmarks:
        #         run_benchmark(path, bm)

        for benchmark in altis_benchmarks_0:
            path = "power/script/altis_script/level0"
            run_benchmark(path, benchmark,test)
        
        
        for benchmark in altis_benchmarks_1:
            path = "power/script/altis_script/level1"
            run_benchmark(path, benchmark,test)
        
        
        for benchmark in altis_benchmarks_2:
            path = "power/script/altis_script/level2"
            run_benchmark(path, benchmark,test)




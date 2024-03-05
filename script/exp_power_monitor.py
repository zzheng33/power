import os
import subprocess
import time
import signal



# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
monitor_CPU_power = "./monitor_cpu_power.py"
monitor_GPU_power = "./monitor_gpu_power.py"

# scritps for running various benchmarks
run_altis = "./run_altis.py"
run_ecp = "./run_ecp.py"

# Define your benchmarks, for testing replace the list with just ['FT'] for example
# ecp_benchmarks = ['FT', 'CG', 'LULESH', 'Nekbone', 'AMG2013', 'miniFE']
altis_benchmarks_0 = ['busspeeddownload','busspeedreadback','maxflops']
altis_benchmarks_1 = ['bfs','gemm','gups','pathfinder','sort']
altis_benchmarks_2 = ['cfd','cfd_double','dwt2d','fdtd2d','kmeans','lavamd','mandelbrot',
                      'nw','particlefilter_float','particlefilter_naive','raytracing',
                      'srad','where']

altis_benchmarks_2 = ['kmeans']

# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)


def run_benchmark(benchmark_dir,benchmark):
    output = f"../data/altis_power_res/{benchmark}_power.csv"
    # Execute the benchmark and get its PID

    run_benchmark_command = f"{python_executable} {run_altis} --benchmark {benchmark} --home_dir {os.path.join(home_dir, benchmark_dir)}"
    benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)

    benchmark_pid = benchmark_process.pid

    # Start CPU power monitoring, passing the PID of the benchmark process
    monitor_command = f"echo 9900 | sudo -S {python_executable} {monitor_CPU_power} --home_dir {home_dir} --output_csv {output} --pid {benchmark_pid}"
    

    monitor_process = subprocess.Popen(monitor_command, shell=True, stdin=subprocess.PIPE, text=True)

    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()

    if benchmark_exit_code != 0:
        print(f"Benchmark {benchmark} failed")
    else:
        print(f"Completed benchmark: {benchmark}")



## run ALTIS benchmark
for benchmark in altis_benchmarks_2:
    path = "benchmark/altis/build/bin/level2/"
    run_benchmark(path, benchmark)
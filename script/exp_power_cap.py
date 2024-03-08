import os
import subprocess
import time
import signal
import argparse
import csv

# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
read_cpu_power = "./power_monitor_util/read_cpu_power.py"
read_gpu_power = "./power_monitor_util/read_gpu_power.py"

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
altis_benchmarks_1 = ['gemm','gups','pathfinder','sort']


cpu_caps = [65,70,75,80,85,90,95,100,105,110,115,120,125]

gpu_caps = [100,120,140,160,180,200,220,240,260]



# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)



def run_benchmark_altis(benchmark_dir, benchmark, test):
    output_base = "../data/altis_power_cap_res" if not test else "../data/altis_test"

    # only cap CPU
    output_file = os.path.join(output_base, f"{benchmark}_cap.csv")
    file_exists = os.path.isfile(output_file)
    for cpu_cap in cpu_caps:
        for gpu_cap in gpu_caps:
            subprocess.run([f"./power_util/cpu_cap.sh {cpu_cap}"], shell=True)
            subprocess.run([f"./power_util/gpu_cap.sh {gpu_cap}"], shell=True)
    
            time.sleep(2)
            start = time.time()
            run_benchmark_command = f"{python_executable} {run_altis} --benchmark {benchmark} --benchmark_dir {os.path.join(home_dir, benchmark_dir)}"
            benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
            benchmark_exit_code = benchmark_process.wait()
            end = time.time()
            
            # Calculate and log the runtime
            runtime = end - start
            with open(output_file, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['CPU Cap (W)', 'GPU Cap (W)', 'Runtime (s)'])
                    file_exists = True
                writer.writerow([cpu_cap, gpu_cap, runtime])





if __name__ == "__main__":
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run benchmarks and monitor power consumption.')
    parser.add_argument('--benchmark', type=str, help='Optional name of the benchmark to run', default=None)
    parser.add_argument('--test', type=int, help='whether it is a test run', default=0)
   
    args = parser.parse_args()
    benchmark = args.benchmark
    test = args.test
    # Map of benchmarks to their paths
    benchmark_paths = {
        "level0": altis_benchmarks_0,
        "level1": altis_benchmarks_1,
        "level2": altis_benchmarks_2
    }

    # run given single benchmark 
    if benchmark:
        # Find which level the input benchmark belongs to
        found = False
        for level, benchmarks in benchmark_paths.items():
            if benchmark in benchmarks:
                path = f"power/script/altis_script/{level}"
                run_benchmark_altis(path, benchmark,test)
                found = True
                break
                
    # run all benchmarks
    else:
        # for benchmark in altis_benchmarks_0:
        #     path = "power/script/altis_script/level0"
        #     run_benchmark_altis(path, benchmark,test)
        
        
        for benchmark in altis_benchmarks_1:
            path = "power/script/altis_script/level1"
            run_benchmark_altis(path, benchmark,test)
        
        
        for benchmark in altis_benchmarks_2:
            path = "power/script/altis_script/level2"
            run_benchmark_altis(path, benchmark,test)







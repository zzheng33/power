import os
import subprocess
import time
import signal
import argparse
import psutil


# Define paths and executables
home_dir = os.path.expanduser('~')
python_executable = subprocess.getoutput('which python3')  # Adjust based on your Python version

# scripts for CPU, GPU power monitoring
read_cpu_power = "./power_util/read_cpu_power.py"
read_gpu_power = "./power_util/read_gpu_power.py"
read_uncore_frequency = "./power_util/read_uncore_freq.py"
# read_memory = "./power_util/read_memory_throughput.py"

# scritps for running various benchmarks
run_altis = "./run_benchmark/run_altis.py"
run_ecp = "./run_benchmark/run_ecp.py"
run_npb = "./run_benchmark/run_npb.py"

read_memory = "/home/cc/power/tools/pcm/build/bin/pcm-memory"


# gpu power threshold for trigger the dynamic uncore frequency scaling
gpu_power_ts = 70
pcm = 0
uncore_0 = 0.8
uncore_1 = 0.8

# Define your benchmarks, for testing replace the list with just ['FT'] for example
# ecp_benchmarks = ['FT', 'CG', 'LULESH', 'Nekbone', 'AMG2013', 'miniFE']

npb_benchmarks = ['bt','cg','ep','ft','is','lu','mg','sp','ua','miniFE']

altis_benchmarks_0 = ['busspeeddownload','busspeedreadback','maxflops']
altis_benchmarks_1 = ['bfs','gemm','gups','pathfinder','sort']
altis_benchmarks_2 = ['cfd','cfd_double','fdtd2d','kmeans','lavamd',
                      'nw','particlefilter_float','particlefilter_naive','raytracing',
                      'srad','where']

ecp_benchmarks = ['XSBench','miniGAN','CRADL','sw4lite','Laghos']

# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"
pm_command = "sudo nvidia-smi -i 0 -pm ENABLED"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)
subprocess.run(pm_command, shell=True)

dynamic_uncore_fs = 1


def run_benchmark(benchmark_script_dir,benchmark, suite, test):
    if not test:
        output_cpu = f"../data/{suite}_power_res/{benchmark}_power_cpu.csv"
        output_gpu = f"../data/{suite}_power_res/{benchmark}_power_gpu.csv"
        output_uncore = f"../data/{suite}_power_res/uncore_freq/{benchmark}_uncore_freq.csv"
    else:
        output_cpu = f"../data/{suite}_test/{benchmark}_power_cpu.csv"
        output_gpu = f"../data/{suite}_test/{benchmark}_power_gpu.csv"
        output_uncore = f"../data/{suite}_test/{benchmark}_uncore_freq.csv"

    if pcm:
        # start pcm-memory
        monitor_command_memory = f"echo 9900 | sudo -S taskset -c 5 {read_memory} 0.1 --suite {suite} --benchmark {benchmark} --uncore_0 {uncore_0} --uncore_1 {uncore_1}"
        monitor_process_memory = subprocess.Popen(monitor_command_memory, shell=True, stdin=subprocess.PIPE, text=True)
    
    # Execute the benchmark and get its PID
    if suite == "altis":
        run_benchmark_command = f" taskset -c 0 {python_executable} {run_altis} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"

    elif suite == "ecp":
        run_benchmark_command = f"taskset -c 0 {python_executable} {run_ecp} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"

    elif suite == "npb":
        run_benchmark_command = f"{python_executable} {run_npb} --benchmark {benchmark} --benchmark_script_dir {os.path.join(home_dir, benchmark_script_dir)}"
        
    start = time.time()
    benchmark_process = subprocess.Popen(run_benchmark_command, shell=True)
    benchmark_pid = benchmark_process.pid



    # Start CPU power monitoring, passing the PID of the benchmark process
    monitor_command_cpu = f"echo 9900 | sudo -S taskset -c 1 {python_executable} {read_cpu_power}  --output_csv {output_cpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)
    
    if suite == "altis" or suite == "ecp": 
        # Start GPU power monitoring, passing the PID of the benchmark process
        monitor_command_gpu = f"echo 9900 | sudo -S taskset -c 3 {python_executable} {read_gpu_power}  --output_csv {output_gpu} --pid {benchmark_pid} --dynamic_uncore {dynamic_uncore_fs} --gpu_power_ts {gpu_power_ts}"
        monitor_process = subprocess.Popen(monitor_command_gpu, shell=True, stdin=subprocess.PIPE, text=True)

    # start CPU uncore frequency monitoring
    monitor_command_cpu = f"echo 9900 | sudo -S {python_executable} {read_uncore_frequency}  --output_csv {output_uncore} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)




    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()


    if pcm:
        # kill pcm-memory
        if monitor_process_memory.poll() is None:  # Check if it's still running
            parent_pid = monitor_process_memory.pid
                # Get the parent process
            parent = psutil.Process(parent_pid)
            # Find and kill child processes
            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()  # Or child.kill() for a forceful kill
                except:
                    pass
            

    

    end = time.time()
    runtime = end - start
    print("Runtime: ",runtime)
    if benchmark_exit_code != 0:
        print(f"Benchmark {benchmark} failed")
    else:
        print(f"Completed benchmark: {benchmark}")





if __name__ == "__main__":
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run benchmarks and monitor power consumption.')
    parser.add_argument('--benchmark', type=str, help='Optional name of the benchmark to run', default=None)
    parser.add_argument('--test', type=int, help='whether it is a test run', default=None)
    parser.add_argument('--suite', type=int, help='0 for ECP, 1 for ALTIS, 2 for NPB, 3 for all', default=1)
    parser.add_argument('--benchmark_size', type=int, help='0 for big, 1 for small', default=0)
    parser.add_argument('--uncore_0', type=float, default=2.4)
    parser.add_argument('--uncore_1', type=float, default=2.4)
    parser.add_argument('--dynamic_uncore_fs', type=int, help='0 for no, 1 for yes', default=0)
    parser.add_argument('--pcm', type=int, help='0 for no, 1 for yes', default=0)
    
    


    args = parser.parse_args()
    benchmark = args.benchmark
 
    test = args.test
    suite = args.suite
    benchmark_size = args.benchmark_size
    dynamic_uncore_fs = args.dynamic_uncore_fs
    pcm = args.pcm
    uncore_0 = args.uncore_0
    uncore_1 = args.uncore_1

    script_dir = "/home/cc/power/GPGPU/script/power_util/"

    # if not args.dynamic_uncore_fs:
    # set initial uncore frequency
    subprocess.run([script_dir + "/set_uncore_freq.sh", str(args.uncore_0), str(args.uncore_1)]) 


    if suite == 0 or suite ==3:
        benchmark_script_dir = f"power/GPGPU/script/run_benchmark/ecp_script"
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
        # run all ecp benchmarks
        else:
            for benchmark in ecp_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"ecp",test)
    

    if suite == 1 or suite ==3:
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
                    benchmark_script_dir = f"power/GPGPU/script/run_benchmark/altis_script/{level}"
                    run_benchmark(benchmark_script_dir, benchmark,"altis",test)
                    found = True
                    break
        else:
    
            for benchmark in altis_benchmarks_0:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level0"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_1:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level1"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)
            
            
            for benchmark in altis_benchmarks_2:
                benchmark_script_dir = "power/GPGPU/script/run_benchmark/altis_script/level2"
                run_benchmark(benchmark_script_dir, benchmark,"altis",test)


    if suite == 2 or suite == 3:
        benchmark_script_dir = f"power/GPGPU/script/run_benchmark/npb_script/big/"
        if benchmark_size ==1:
            benchmark_script_dir = f"power/GPGPU/script/run_benchmark/npb_script/small/"
        
        # single test
        if benchmark:
            run_benchmark(benchmark_script_dir, benchmark,"npb",test)
        # run all ecp benchmarks
        else:
            for benchmark in npb_benchmarks:
                run_benchmark(benchmark_script_dir, benchmark,"npb",test)
    


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


train = './train_model/train.py'

# Setup environment
modprobe_command = "sudo modprobe msr"
sysctl_command = "sudo sysctl -n kernel.perf_event_paranoid=-1"
pm_command = "sudo nvidia-smi -i 0 -pm ENABLED"

subprocess.run(modprobe_command, shell=True)
subprocess.run(sysctl_command, shell=True)
subprocess.run(pm_command, shell=True)


def run_benchmark(model, test):
    if not test:
        output_cpu = f"../data/{model}/{model}_power_cpu.csv"
        output_gpu = f"../data/{model}/{model}_power_gpu.csv"
    else:
        output_cpu = f"../data/test/{model}_power_cpu.csv"
        output_gpu = f"../data/test/{model}_power_gpu.csv"
    
    # run_benchmark_command = f"{python_executable} {train} --model {model}"
    train_model_command = f"{python_executable} {train}"
        

    benchmark_process = subprocess.Popen(train_model_command, shell=True)
    benchmark_pid = benchmark_process.pid

    monitor_command_cpu = f"echo 9900 | sudo -S {python_executable} {read_cpu_power}  --output_csv {output_cpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_cpu, shell=True, stdin=subprocess.PIPE, text=True)
    
    # Start GPU power monitoring, passing the PID of the benchmark process
    monitor_command_gpu = f"echo 9900 | sudo -S {python_executable} {read_gpu_power}  --output_csv {output_gpu} --pid {benchmark_pid}"
    monitor_process = subprocess.Popen(monitor_command_gpu, shell=True, stdin=subprocess.PIPE, text=True)

    
    # Wait for the benchmark process to complete
    benchmark_exit_code = benchmark_process.wait()




if __name__ == "__main__":
   # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Run ML models and monitor power consumption.')
    parser.add_argument('--model', type=str, help='Optional name of the model to train', default="resnet50")
    parser.add_argument('--test', type=int, help='whether it is a test run', default=0)

    args = parser.parse_args()
    model = args.model
    test = args.test


    run_benchmark(model, test)











   
    


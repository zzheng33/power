import subprocess
import time
import csv

def set_gpu_clock(memory_clock, gpu_clock):
    command = f"sudo nvidia-smi -ac {memory_clock},{gpu_clock}"
    subprocess.run(command, shell=True, check=True)

def get_gpu_power():
    command = "nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return float(result.stdout.strip())

def run_gpu_workload():
    # Start the benchmark script in the background
    command = "/home/cc/power/script/run_benchmark/altis_script/level2/fdtd2d.sh"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Allow the script to run while we capture the power consumption
    max_power = 0
    for _ in range(8):
        # Capture the current power consumption
        current_power = get_gpu_power()
        max_power = max(max_power, current_power)
        time.sleep(0.5)  # Adjust the sleep time as needed for more precise measurement

    # After capturing the power data, terminate the process if it is still running
    if process.poll() is None:
        process.terminate()
        process.wait()

    # Print the output and errors (if any) after capturing power data
    stdout, stderr = process.communicate()
    print("Benchmark script output:")
    print(stdout.decode())
    
    if stderr:
        print("Benchmark script errors:")
        print(stderr.decode())

    return max_power

def test_gpu_power(memory_clock, gpu_clocks):
    results = []
    
    for clock in gpu_clocks:
        print(f"Setting GPU clock to {clock} MHz")
        set_gpu_clock(memory_clock, clock)
        
        # Allow some time for the GPU to stabilize at the new clock
        time.sleep(2)
        
        # Run the GPU workload and capture max power
        print("Running benchmark to stress GPU and capturing power...")
        max_power = run_gpu_workload()
        
        print(f"Max Power at {clock} MHz: {max_power} W")
        results.append((clock, max_power))
        
        # Sleep between tests to ensure system stability
        time.sleep(2)
    
    return results

def main():
    memory_clock = 1215  # Set to your desired memory clock
    gpu_clocks = [
        1410, 1395, 1380, 1365, 1350, 1335, 1320, 1305, 1290, 1275,
        1260, 1245, 1230, 1215, 1200, 1185, 1170, 1155, 1140, 1125,
        1110, 1095, 1080, 1065, 1050, 1035, 1020, 1005, 990, 975,
        960, 945, 930, 915, 900, 885, 870, 855, 840, 825, 810, 795,
        780, 765, 750, 735, 720, 705, 690, 675, 660, 645, 630, 615,
        600, 585, 570, 555, 540, 525, 510, 495, 480, 465, 450, 435,
        420, 405, 390, 375, 360, 345, 330, 315, 300, 285, 270, 255,
        240, 225, 210
    ] 
    
    results = test_gpu_power(memory_clock, gpu_clocks)
    
    # Output results to CSV
    with open('gpu_power_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GPU Clock (MHz)", "Max Power (W)"])
        writer.writerows(results)
    
    print("\nGPU Clock Frequency vs Max Power Consumption data has been saved to 'gpu_power_results.csv'.")
    
    # Reset the GPU clock to a safe default
    set_gpu_clock(1215, 1410)

if __name__ == "__main__":
    main()

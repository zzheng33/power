import time
from pynvml import *

# Initialize NVML
nvmlInit()

# Get the first GPU
handle = nvmlDeviceGetHandleByIndex(0)

# Output file where the results will be saved
output_file = "gpu_usage_log.txt"

# Open the file in write mode
with open(output_file, "w") as f:
    f.write("Timestamp, GPU Utilization (%), Memory Utilization (%)\n")
    while True:
        # Get the current date and time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Query GPU utilization and memory utilization
        utilization = nvmlDeviceGetUtilizationRates(handle)
        gpu_util = utilization.gpu
        mem_util = utilization.memory

        # Write the results to the file
        f.write(f"{timestamp}, {gpu_util}, {mem_util}\n")

        # Flush the output to ensure it's written
        f.flush()

        # Wait for 0.1 seconds before the next iteration
        time.sleep(0.1)

# Shutdown NVML
nvmlShutdown()

import time
from pynvml import *

# Initialize NVML
nvmlInit()

# Get handle for the first GPU (assuming single GPU system; modify index for multi-GPU)
handle = nvmlDeviceGetHandleByIndex(0)

# Output file to save clock speeds
output_file = "gpu_clock_speeds.txt"

# Clear the output file if it exists
with open(output_file, "w") as f:
    f.write("Timestamp, Graphics Clock (MHz), SM Clock (MHz), Memory Clock (MHz)\n")

print("Starting GPU clock speed monitoring. Press Ctrl+C to stop.")

try:
    while True:
        # Get the current date and time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Get current clock speeds
        graphics_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_GRAPHICS)
        sm_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_SM)
        mem_clock = nvmlDeviceGetClockInfo(handle, NVML_CLOCK_MEM)

        # Print the results to the console
        # print(f"{timestamp} | Graphics Clock: {graphics_clock} MHz, SM Clock: {sm_clock} MHz, Memory Clock: {mem_clock} MHz")

        # Save the results to a file
        with open(output_file, "a") as f:
            f.write(f"{timestamp}, {graphics_clock}, {sm_clock}, {mem_clock}\n")

        # Wait for the specified interval before repeating
        time.sleep(0.1)  # Adjust the interval as needed (e.g., 0.1 for 0.1 seconds)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user.")

finally:
    # Shutdown NVML
    nvmlShutdown()

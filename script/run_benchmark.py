import argparse
import os
import subprocess
import time

# Parse command-line arguments for a specific benchmark
parser = argparse.ArgumentParser(description='Run specific benchmark.')
parser.add_argument('--benchmark', type=str, help='Name of the benchmark to run', required=True)
args = parser.parse_args()

# Function to run the specified benchmark
def run_benchmark(benchmark):
    home_directory = os.path.expanduser('~')  # Get user's home directory
    
    # Define commands for your benchmarks
    benchmarks = {
        'LULESH': f"cd {os.path.join(home_directory, 'LULESH', './')} && ./lulesh2.0 -s 40",
        'miniFE': f"cd {os.path.join(home_directory, 'miniFE', 'ref/src')} && ./miniFE.x -nx 128 -ny 128 -nz 128",
        'Nekbone': f"cd {os.path.join(home_directory, 'Nekbone', 'test/example1')} && ./nekbone",
        'AMG2013': f"cd {os.path.join(home_directory, 'AMG2013', 'test')} && mpirun -n 8 amg2013 -pooldist 1 -r 12 12 12",
        'FT':      f"cd {os.path.join(home_directory, 'NPB3.4.2/NPB3.4-OMP', 'bin')} && ./ft.C.x",
        'CG':      f"cd {os.path.join(home_directory, 'NPB3.4.2/NPB3.4-OMP', 'bin')} && ./cg.C.x",
        'MG':      f"cd {os.path.join(home_directory, 'NPB3.4.2/NPB3.4-OMP', 'bin')} && ./mg.C.x",
    }

    benchmark_command = benchmarks.get(args.benchmark)
    if benchmark_command:
        print(f"Running {args.benchmark} benchmark...")
        subprocess.run(benchmark_command, shell=True, check=True)
        print(f"{args.benchmark} benchmark completed.")
    else:
        print(f"Benchmark {args.benchmark} is not defined.")

if __name__ == "__main__":
    # time.sleep(1)
    run_benchmark(args.benchmark)

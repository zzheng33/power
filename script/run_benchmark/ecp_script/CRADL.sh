#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/CRADL/"

cd ${benchmark_dir}
mpirun -n 16 python cradl_benchmarking.py --inference_dir ./data
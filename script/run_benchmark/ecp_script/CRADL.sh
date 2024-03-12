#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/CRADL/"

cd ${benchmark_dir}
source CRADL_env/bin/activate

mpirun -n 8 python cradl_benchmarking.py --inference_dir ./data

deactivate
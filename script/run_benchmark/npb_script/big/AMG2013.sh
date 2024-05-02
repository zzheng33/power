#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/CPU-only/AMG2013/test/"
benchmark_dir="/home/cc/benchmark/CPU-only/AMG2013/test/"
cd ${benchmark_dir}
mpirun -n 8 ./amg2013 -pooldist 1 -r 2 2 2
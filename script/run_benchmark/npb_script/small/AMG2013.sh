#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/CPU-only/AMG2013/test/"

cd ${benchmark_dir}
mpirun -n 8 ./amg2013 -pooldist 0 -r 6 6 6
#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/sw4lite/optimize_cuda"

cd ${benchmark_dir}
mpirun -n 8 sw4lite ../tests/cartesian/uni.in
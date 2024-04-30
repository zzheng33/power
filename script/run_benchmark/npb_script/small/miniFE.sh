#!/bin/bash

home_dir=$HOME
# benchmark_dir="${home_dir}/benchmark/CPU-only/miniFE/openmp/src/"
benchmark_dir="${home_dir}/benchmark/CPU-only/miniFE/ref/src/"

cd ${benchmark_dir}
mpirun -n 16 --use-hwthread-cpus ./miniFE.x  -nx 132 -ny 128 -nz 128
# mpirun -n 48 --use-hwthread-cpus ./miniFE.x  -nx 528 -ny 512 -nz 512
# ./miniFE.x  -nx 300 -ny 300 -nz 300
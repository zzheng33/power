#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/CPU-only/miniFE/ref/src/"

cd ${benchmark_dir}
./miniFE.x -nx 200 -ny 200 -nz 200 
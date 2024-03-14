#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/XSBench/cuda"


mpirun -n 2 "$benchmark_dir/XSBench" -m event -s large

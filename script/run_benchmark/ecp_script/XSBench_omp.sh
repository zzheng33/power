#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/XSBench/openmp-threading"
cd "$benchmark_dir"
make


"$benchmark_dir/XSBench"  -s XL

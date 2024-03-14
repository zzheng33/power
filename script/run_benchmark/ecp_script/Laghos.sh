#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/Laghos/"

cd ${benchmark_dir}


./laghos -p 3 -m data/rectangle01_quad.mesh -rs 2 -tf 3.0 -pa -d cuda

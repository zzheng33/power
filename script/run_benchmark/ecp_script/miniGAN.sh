#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/miniGAN/pytorch"

cd ${benchmark_dir}
python minigan_driver.py --num-threads 40 --epoch 20

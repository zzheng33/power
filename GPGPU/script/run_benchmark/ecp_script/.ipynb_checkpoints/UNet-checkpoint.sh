#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/UNet/"

cd ${benchmark_dir}
source UNet_env/bin/activate
python train.py --amp -e 1

deactivate

#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb



python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.4 --uncore_1 2.4 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --benchmark Resnet50

sleep 10


sudo mv /home/cc/power/GPGPU/data/ecp_power_res/*.csv /home/cc/power/GPGPU/data/ecp_power_res/max_uncore 
sudo mv /home/cc/power/GPGPU/data/ecp_power_res/mem_throughput/*.csv /home/cc/power/GPGPU/data/ecp_power_res/mem_throughput/max_uncore






TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;
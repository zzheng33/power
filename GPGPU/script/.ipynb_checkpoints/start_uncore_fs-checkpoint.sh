#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb


# test
# ./power_util/cpu_cap.sh 250
# ./power_util/gpu_cap.sh 260


# this is for altis, gpu-power based ufs. also need to use taskset
# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 1 --dynamic_ufs_mem 0 --uncore_0 2.4 --uncore_1 0.8 --pcm 1

# for altis, mem based ufs, single socket cap for both CPU & GPU non-intensive
# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --benchmark nw




# CARDL: 200, 500, 3
# UNet:  200, 500, 5
# miniGAN 200, 500, 5
# sw4lite 200, 500, 5
# Laghos 200, 500, 5
# XSBench 200, 500, 5

python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.4 --uncore_1 2.4 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --benchmark bert_large

sleep 10


sudo mv /home/cc/power/GPGPU/data/ecp_power_res/*.csv /home/cc/power/GPGPU/data/ecp_power_res/max_uncore 
sudo mv /home/cc/power/GPGPU/data/ecp_power_res/mem_throughput/*.csv /home/cc/power/GPGPU/data/ecp_power_res/mem_throughput/max_uncore


python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --benchmark bert_large

sleep 10

sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/min_uncore 
sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/mem_throughput/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/mem_throughput/min_uncore




python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --benchmark bert_large

sleep 10

sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/dynamic_uncore 
sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/mem_throughput/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/mem_throughput/dynamic_uncore


./power_util/set_uncore_freq.sh 2.4 2.4





TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;
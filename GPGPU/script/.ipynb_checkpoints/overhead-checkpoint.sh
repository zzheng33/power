#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb

# CARDL: 200, 500, 3
# UNet:  200, 500, 5
# miniGAN 200, 500, 5
# sw4lite 200, 500, 5
# Laghos 200, 500, 5
# XSBench 200, 500, 5
#lammps 200,500,5








################### ALTIS overhead Starts ###################


# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 0 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 0 --benchmark srad

# sleep 3

# sudo mv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/base 


# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 0 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 1 --benchmark fdtd2d

# sleep 3

# sudo mv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/ups_overhead

# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 0 --benchmark cfd_double

# sleep 3

# sudo mv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/altis_power_res/no_power_shift/magus_overhead




################### ALTIS overhead Ends ###################







################### ECP overhead Starts ###################


python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 0 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 0 --benchmark CRADL

sleep 5

sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/base

# python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 0 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 1 --benchmark UNet

# sleep 5

# sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/ups_overhead 


# python3 exp_power_motif.py --suite 0 --test 0  --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 0 --uncore_0 2.2 --uncore_1 2.2 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 1 --burst_up 0.4 --burst_low 0.2 --ups 0 --benchmark CRADL

# sleep 5

# sudo mv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/*.csv /home/cc/power/GPGPU/data/ecp_power_res/no_power_shift/magus_overhead 




################### ECP overhead Ends ###################






./power_util/set_uncore_freq.sh 2.4 2.4





TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;
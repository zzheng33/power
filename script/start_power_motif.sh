#!/bin/bash


# test
./power_util/cpu_cap.sh 170
./power_util/gpu_cap.sh 130

#python3 exp_power_motif.py  --test 1 --suite 1



# python3 exp_power_motif.py --suite 0 --benchmark CRADL --test 1

python3 exp_power_motif.py --suite 0 --benchmark sw4lite --test 1
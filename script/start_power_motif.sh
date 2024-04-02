#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS

# test
./power_util/cpu_cap.sh 250
./power_util/gpu_cap.sh 260

#python3 exp_power_motif.py  --test 1 --suite 1



# python3 exp_power_motif.py --suite 0 --benchmark CRADL --test 1

python3 exp_power_motif.py --suite 1 --benchmark raytracing --test 1
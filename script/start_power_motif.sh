#!/bin/bash

# run all benchamrks
#python3 exp_power_motif.py

# test
./power_util/cpu_cap.sh 250
./power_util/gpu_cap.sh 260
python3 exp_power_motif.py  --test 1 --suite 0 


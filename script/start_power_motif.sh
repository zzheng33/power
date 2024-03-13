#!/bin/bash


# test
./power_util/cpu_cap.sh 200
./power_util/gpu_cap.sh 250

#python3 exp_power_motif.py  --test 1 --suite 1

# run all benchamrks
python3 exp_power_motif.py --suite 0 --benchmark XSBench
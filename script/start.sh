#!/bin/bash

# run all benchamrks
#python3 exp_power_motif.py

# test
./cpu_cap.sh
./gpu_cap.sh
python3 exp_power_motif.py --benchmark raytracing --test 1
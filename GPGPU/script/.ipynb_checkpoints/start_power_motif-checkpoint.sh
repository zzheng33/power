#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb


# test
# ./power_util/cpu_cap.sh 250
# ./power_util/gpu_cap.sh 260

# python3 exp_power_motif.py --suite 1 --test 0  --dynamic_uncore_fs 0 --uncore_0 2.4 --uncore_1 0.8 --benchmark nw --pcm 1

python3 exp_power_motif.py --suite 1 --test 0  --dynamic_uncore_fs 1 --uncore_0 2.4 --uncore_1 0.8 --benchmark nw --pcm 0

./power_util/set_uncore_freq.sh 2.4 2.4

# python3 exp_power_motif.py --suite 0 --benchmark CRADL --test 1

# python3 exp_power_motif.py --suite 1 --benchmark raytracing --test 1
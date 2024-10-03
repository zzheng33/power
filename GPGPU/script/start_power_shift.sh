#!/bin/bash

# suite 0: ECP 
# suite 1: ALTIS
# suite 2: npb


suite=1  
power_shift=1

# Set suite_dir based on suite value
if [ $suite -eq 0 ]; then
    suite_dir="ecp_power_res"
elif [ $suite -eq 1 ]; then
    suite_dir="altis_power_res"
elif [ $suite -eq 2 ]; then
    suite_dir="npb_power_res"
else
    echo "Invalid suite value"
    exit 1
fi

# Set shift_dir based on power_shift value
if [ $power_shift -eq 0 ]; then
    shift_dir="no_power_shift"
else
    shift_dir="power_shift"
fi

################################ max_uncore ################################ 
python3 exp_power_motif.py --suite $suite --test 0 --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --power_shift $power_shift --benchmark cfd_double


sleep 10
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/max_uncore
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/max_uncore


################################ min_uncore ################################ 
python3 exp_power_motif.py --suite $suite --test 0 --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --power_shift $power_shift --benchmark cfd_double


sleep 10
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/min_uncore
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/min_uncore



################################ dynamic_uncore ################################ 
python3 exp_power_motif.py --suite $suite --test 0 --dynamic_ufs_gpuP 0 --dynamic_ufs_mem 1 --uncore_0 0.8 --uncore_1 0.8 --pcm 1 --inc_ts 200 --dec_ts 500 --history 5 --dual_cap 0 --burst_up 0.4 --burst_low 0.2 --power_shift $power_shift --benchmark cfd_double


sleep 10
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/dynamic_uncore
sudo mv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/*.csv /home/cc/power/GPGPU/data/$suite_dir/$shift_dir/mem_throughput/dynamic_uncore



TARGET_DIR="../data/"

# Find all .csv files under the target directory and make them writable
sudo find "$TARGET_DIR" -type f -name "*.csv" -exec chown $(whoami):$(whoami) {} \;
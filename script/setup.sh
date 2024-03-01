#!/bin/bash

home_dir="/home/cc"

sudo apt-get update
sudo apt-get --assume-yes install gfortran
sudo apt-get --assume-yes install libopenmpi-dev
sudo apt-get --assume-yes install mpich
sudo apt --assume-yes install cmake


# git clone https://github.com/zzheng33/pcm.git
# mv -r ./pcm ../tools/ 

cd "${home_dir}/power/tools/pcm"
mkdir build
cd build
cmake ..
cmake --build . --parallel

cd "${home_dir}/power/tools/RAPL"
make clean
make

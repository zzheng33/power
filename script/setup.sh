#!/bin/bash

home_dir="/home/cc"

func install_dependence {

    sudo apt-get update
    sudo apt-get --assume-yes install gfortran
    sudo apt-get --assume-yes install libopenmpi-dev
    sudo apt-get --assume-yes install mpich
    sudo apt --assume-yes install cmake
}


func setup_rapl {
    cd "${home_dir}/power/tools/RAPL"
    make clean
    make
}


func setup_pcm {
    # git clone https://github.com/zzheng33/pcm.git
    # mv -r ./pcm ../tools/ 

    cd "${home_dir}/power/tools/pcm"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
}

# func setup_cpu_benchmark {}


# func setup_rodinia {}


# func setup_altis {}


# install_dependence
setup_pcm

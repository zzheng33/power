#!/bin/bash

home_dir=$(eval echo ~$USER)

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
    cd "${home_dir}/power/tools"
    # git clone https://github.com/zzheng33/pcm.git
    # mv -r ./pcm ../tools/ 
    git clone https://github.com/zzheng33/pcm.git
    cd "${home_dir}/power/tools/pcm"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
}

func load_benchmark {
    cd "${home_dir}"
    git clone https://github.com/zzheng33/benchmark.git
}


func setup_rodinia {
    cd "${home_dir}/benchmark/rodinia"
    make
}


func setup_altis {
    cd "${home_dir}/benchmark/altis"
    ./setup.sh
}

# NPB, AMG2013...
# func setup_other_benchmark {

# }

install_dependence
setup_altis
setup_rodinia

# setup_pcm

#!/bin/bash

home_dir="/home/cc"

install_dependence() {
    sudo apt-get update
    sudo apt-get --assume-yes install gfortran
    sudo apt-get --assume-yes install libopenmpi-dev
    sudo apt-get --assume-yes install mpich
    sudo apt --assume-yes install cmake
}

setup_rapl() {
    cd "${home_dir}/power/tools/RAPL"
    make clean
    make
}

download_rodinia_data(){
    cd "${home_dir}"
    wget https://dl.dropbox.com/s/cc6cozpboht3mtu/rodinia-3.1-data.tar.gz
    tar -xzf rodinia-3.1-data.tar.gz
    cd rodinia-data
    mv * "${home_dir}/benchmark/rodinia/data"

}


# setup_pcm() {
#     cd "${home_dir}/power/tools"
#     git clone https://github.com/zzheng33/pcm.git
#     cd "${home_dir}/power/tools/pcm"
#     mkdir build
#     cd build
#     cmake ..
#     cmake --build . --parallel
# }

load_benchmark() {
    cd "${home_dir}"
    git clone https://github.com/zzheng33/benchmark.git
}

# setup_rodinia() {
#     cd "${home_dir}/benchmark/rodinia"
#     sudo make
# }

setup_altis() {
    cd "${home_dir}/benchmark/altis"
    sudo ./setup.sh
}

# setup_other_benchmark() {
#     # Define other benchmark setup steps here
# }


install_dependence
load_benchmark
setup_altis
# setup_rodinia
# setup_pcm

#download_rodinia_data
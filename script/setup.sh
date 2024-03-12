#!/bin/bash

home_dir="/home/cc"

install_dependence() {
    sudo apt-get update
    sudo apt-get --assume-yes install gfortran
    sudo apt-get --assume-yes install libopenmpi-dev
    sudo apt-get --assume-yes install mpich
    sudo apt --assume-yes install cmake
    sudo pip install psutil
    sudo apt-get --assume-yes install liblapack-dev
    sudo pip install jupyterlab
    sudo pip install numpy matplotlib pandas
}

setup_rapl() {
    cd "${home_dir}/power/tools/RAPL"
    make clean
    make
}

# download_rodinia_data(){
#     cd "${home_dir}"
#     wget https://dl.dropbox.com/s/cc6cozpboht3mtu/rodinia-3.1-data.tar.gz
#     tar -xzf rodinia-3.1-data.tar.gz
#     cd rodinia-data
#     mv * "${home_dir}/benchmark/rodinia/data"

# }


setup_pcm() {
    cd "${home_dir}/power/tools"
    git clone https://github.com/zzheng33/pcm.git
    cd "${home_dir}/power/tools/pcm"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
}

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

generate_altis_data() {
    cd "${home_dir}/benchmark/altis/data/kmeans"
    python3 datagen.py -n 8388608 -f

    
}

setup_miniGAN_env() {
    cd "${home_dir}/benchmark/ECP/miniGAN/data"
    python generate_bird_images.py

    cd "${home_dir}/benchmark/ECP/miniGAN/pytorch"

    python -m venv minigan_env
    source minigan_env/bin/activate
    pip install torch==1.4.0
    pip install torchvision==0.5.0
    pip install wheel
    pip install numpy
    pip install horovod==0.18.2

    deactivate


}


install_dependence
load_benchmark
setup_altis
setup_pcm
generate_altis_data
setup_miniGAN_env

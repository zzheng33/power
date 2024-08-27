#!/bin/bash

home_dir="/home/cc"

install_dependence() {
    sudo apt-get update
    sudo apt-get --assume-yes install gfortran
    sudo apt-get --assume-yes install libopenmpi-dev
    sudo apt-get --assume-yes install linux-intel-iotg-5.15-tools-common
    sudo apt --assume-yes install linux-tools-5.4.0-174-generic
    sudo apt-get --assume-yes install mpich
    sudo apt --assume-yes install cmake
    sudo apt --assume-yes install python3-pip
    sudo pip install psutil
    sudo apt-get --assume-yes install liblapack-dev
    sudo pip install jupyterlab
    sudo pip install numpy matplotlib pandas
    sudo pip install scipy
    sudo pip install plotly
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
    git clone --recursive https://github.com/zzheng33/pcm.git
    cd "${home_dir}/power/tools/pcm"
    mkdir build
    cd build
    cmake ..
    cmake --build . --parallel
    sudo modprobe msr
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
    python3 datagen.py -n 1048576 -f

    
}

setup_miniGAN_env() {
    cd "${home_dir}/benchmark/ECP/miniGAN/data"
    python3 generate_bird_images.py --dim-mode 3 --num-images 128 --image-dim 64 --num-channels 3

    cd "${home_dir}/benchmark/ECP/miniGAN/"

    bash ./setup_python_env.sh
}

setup_CRADL() {
    cd "${home_dir}/benchmark/ECP/CRADL/"
    python3 -m venv CRADL_env
    source CRADL_env/bin/activate
    bash INSTALL
    deactivate
    cd ./data
    bash ./filter.sh
}

setup_XSBench() {
     cd "${home_dir}/benchmark/ECP/XSBench/cuda"
     make
     cd "${home_dir}/benchmark/ECP/XSBench/openmp-threading"
  
     make
}

setup_RSBench() {
     cd "${home_dir}/benchmark/ECP/RSBench/cuda"
     make
     cd "${home_dir}/benchmark/ECP/RSBench/openmp-threading"
    
     make
}

setup_Laghos() {
    cd "${home_dir}/benchmark/ECP/hypre-2.11.2/src/"
    ./configure --with-cuda --with-gpu-arch="80" --disable-fortran
    make -j
    cd ../..
    ln -s hypre-2.11.2 hypre

    cd metis-4.0.3/
    make
    cd ..
    ln -s metis-4.0.3 metis-4.0

    cd mfem/
    make pcuda CUDA_ARCH=sm_80 -j
    cd ..

    cd Laghos/
    make -j 
    

}

setup_ecp_cpu() {
    cd "${home_dir}/benchmark/ECP/miniFE/openmp/src/"
    
    make

    cd "${home_dir}/benchmark/ECP/AMG2013/"
  
    make
}

setup_npb() {
    cd "${home_dir}/benchmark/NPB/NPB3.4-OMP/"
    
    make suite

}


install_dependence
load_benchmark
setup_altis
setup_pcm
generate_altis_data
setup_miniGAN_env
setup_CRADL
setup_Laghos
setup_XSBench
setup_RSBench
setup_ecp_cpu
setup_npb


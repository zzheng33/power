#!/bin/bash

home_dir=$HOME
benchmark_dir="${home_dir}/benchmark/ECP/lammps/build/"

cd ${benchmark_dir}

mpirun -np 1 lmp -sf gpu -pk gpu 1 -in in.lj
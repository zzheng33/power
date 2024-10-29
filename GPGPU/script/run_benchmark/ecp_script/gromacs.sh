#!/bin/bash

cd /home/cc/tmp

export PATH=$HOME/benchmark/ECP/gromacs/build/bin:$PATH

mpirun -np 1 gmx_mpi mdrun -v -deffnm em


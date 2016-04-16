#!/bin/bash
#$ -V
#$ -cwd
#$ -S /bin/bash
#$ -N compute_xis

### Use Parallel Environment mpi,1320 CPUs:
#$ -pe openmpi 20
#$ -q normal
#$ -R yes


##mpirun ./mpitest
python 160416.compute_xis.py

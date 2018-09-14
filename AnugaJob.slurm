#!/bin/bash
#----------------------------------------------------
# Example SLURM job script to run MPI applications
#----------------------------------------------------
#SBATCH -J Anuga_1       # Job name
#SBATCH -o Anuga_1.o%j   # Name of stdout output file
#SBATCH -e Anuga_1.o%j   # Name of stdout output file
#SBATCH -p normal        # Queue name
#SBATCH -N 2             # Total number of nodes requested
#SBATCH -n 48            # Total number of mpi tasks requested
#SBATCH -t 05:00:00      # Run time (hh:mm:ss) - 1.5 hours


#SBATCH --mail-user=ps29626@tacc.utexas.edu
#SBATCH --mail-type=begin   # email me when the job starts
#SBATCH --mail-type=end     # email me when the job finishes

# Launch the MPI application using ibrun
ibrun python 11_FBE_20CMS_NoMan_1m.py

#Note:  ibrun does not bind tasks or threads by default
#       To bind task/threads to sockets or cores, you must use
#       ibrun with tacc_affinity or use the "srun" command directly
#       with the "--cpu_bind" option.
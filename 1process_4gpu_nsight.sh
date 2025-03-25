#!/bin/bash
#SBATCH --output=/home/horace/data/code/test_optim_gpu/toy-example-gpu/_logs/log.out
#SBATCH --job-name=gpu_optim_job
#SBATCH --partition=unpreemptible
#SBATCH --nodes=1
#SBATCH --ntasks=1                   
#SBATCH --gpus-per-task=4              
#SBATCH --cpus-per-gpu=12      
#SBATCH --mem=32G

# Define output file for profiling results
PROFILE_OUTPUT="/home/horace/data/code/test_optim_gpu/toy-example-gpu/_logs/profile_result"

# Start profiling using cudaProfilerApi (triggered by cudaProfilerStart/Stop in the application)
nsys profile -c none --output=$PROFILE_OUTPUT srun uv run /home/horace/data/code/test_optim_gpu/toy-example-gpu/examplegpu/src/main.py

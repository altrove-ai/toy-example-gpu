#!/bin/bash
#SBATCH --output=/home/horace/toy-example-gpu/_logs/log.out
#SBATCH --job-name=gpu_optim_job
#SBATCH --partition=unpreemptible
#SBATCH --nodes=1
#SBATCH --ntasks=1                   
#SBATCH --gpus-per-task=4              
#SBATCH --cpus-per-gpu=12      
#SBATCH --mem=32G

srun uv run /home/horace/toy-example-gpu/examplegpu/src/main.py
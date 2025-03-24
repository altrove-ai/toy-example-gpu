#!/bin/bash
#SBATCH --output=/home/ubuntu/aless/xrd_to_crystal/outputs/log.out
#SBATCH --job-name=my_multi_gpu_job
#SBATCH --partition=unpreemptible
#SBATCH --nodes=1
#SBATCH --ntasks=1                   
#SBATCH --gpus-per-task=4              
#SBATCH --cpus-per-gpu=12      
#SBATCH --mem=256G                  

srun uv run /examplegpu/src/main.py
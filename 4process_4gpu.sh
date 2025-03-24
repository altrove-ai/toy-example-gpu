#!/bin/bash
#SBATCH --job-name=gpu_optim_job
#SBATCH --partition=unpreemptible
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gpus-per-task=1
#SBATCH --cpus-per-gpu=4
#SBATCH --mem=32G
#SBATCH --output=/home/horace/data/code/test_optim_gpu/toy-example-gpu/_logs/log_%A_%a.out

srun uv run /home/horace/data/code/test_optim_gpu/toy-example-gpu/examplegpu/src/main.py
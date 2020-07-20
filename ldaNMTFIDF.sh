#!/bin/bash
#SBATCH -p normal
#SBATCH -J LDANMallTFIDF
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -t 48:00:00
#SBATCH --mail-user=ishankarora1100@utexas.edu
#SBATCH --mail-type=all
#SBATCH -o %joutput.txt
#SBATCH -e %jerror.txt

python LDANMtfidf.py

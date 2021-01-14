#!/bin/bash                
#PBS -N extract_swotsim        
#PBS -l select=1:ncpus=1:mem=5000mb      
#PBS -l walltime=168:00:00

# on se deplace dans le repertoire de travail
# TMPDIR correspond au répertoire de travail temporaire (local au noeud de calcul)
cd /home/ad/alberta/git/extract-swot-simulator

module load conda
conda activate perf-pangeo
python 2021-01-13-AA-script-extract-region-swot-simulator-generic.py --reg REG --phase PHASE --data DATA


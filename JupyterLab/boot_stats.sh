#!/bin/bash

# Usage: 
# ./boot_stats.sh

# Purpose: 
# The purpose of this script is to automatically boot up
# a jupyterlab session easy peesy.

cd "/mnt/c/Users/mkozubov/OneDrive - Tenaya Therapeutics/Desktop/Intuitions/"
eval "$(conda shell.bash hook)"
conda activate stats
jupyter lab --NotebookApp.password='' --allow-root --NotebookApp.token=''

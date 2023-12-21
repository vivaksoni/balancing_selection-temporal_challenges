# Temporal challenges in detecting balancing selection from population genomic data

Vivak Soni and Jeffrey D. Jensen.

Contact: vsoni11@asu.edu

Repository contains scripts to generate simulated data and run balancing selection inference on SLiM output, as per Soni and Jensen 2024.

Scripts folder contains SLiM simulation scripts, as well as python scripts to generate input files for downstream inference. Jupyter scripts to reproduce plots are contained in scripts/plotting folder. BalLeRMix+_v1.py
script is required to run B2 method, and is from Cheng and DeGiorgio 2020.

Mutation and recombination rate maps are contained in zip folders. Script to generate maps is included in scripts/variable rates.

Within Scripts folder see:
SIMULATION_README.txt for instructions on running SLiM simulations.
B2_README.txt for instructions on generating B2 input files and running balancing selection inference.
iHS_README.txt for instructions on generating iHS input files and running balancing selection inference.
SUMMARY_STATS_README.txt for instructions on generating summary stats from SLiM outputs.
balancing_selection_plot_results.ipynb for juupyter script to plot all figures.

#script takes .ms file and creates allele frequency file
#python3  get_aff.py -msFile "balancing_selection/results/stationary/rr_fixed_mu_fixed/DFE_only/1N/hSap_DFE3_rep" \
#-fixedFile "sweep_detection/results/stationary/benProp_0.05_2Nes_10/1Mb_rep1.fixed" \
#-outFile  "sweep_detection/scripts/SF_inputFiles/results/stationary/benProp_0.05_2Nes_10/1Mb_rep1.aff" \
#-ro 1.1e-8 -regionLen 6956 -samples 100 

from __future__ import print_function
import sys
import pandas as pd
import math
import os
import argparse
import numpy as np


#parsing user given constants
parser = argparse.ArgumentParser(description='Information about length of region and sample size')
parser.add_argument('-inFile', dest = 'inFile', action='store', nargs = 1, type = str, help = 'path to gen file (.gen format)')
parser.add_argument('-outFile', dest = 'outFile', action='store', nargs = 1, type = str, help = 'path to output file')
parser.add_argument('-ro', dest = 'ro', action='store', nargs = 1, type = float, help = 'recombination rate')
parser.add_argument('-samples', dest = 'samples', action='store', nargs = 1, type = int, help = 'no. of samples in .ms file')

args = parser.parse_args()
ro =  args.ro[0]
inFile = args.inFile[0]
out_file = args.outFile[0]
samples = args.samples[0]

#Load in fsc output
df = pd.read_csv(inFile, sep='\t', header=0, index_col=False)
#Subset df to include only columns of data from population 1
df2 = df.filter(regex='A_')
#Get positions from df
pos = list(df.Pos)
#Get genetic positions from df
genPos = [x*ro for x in pos]
#Get counts from df2
freqs = list(df2.T.sum())
#Create list of samples
samples = [samples for x in pos]

#Create df from lists and rename columns
rdf = pd.DataFrame([pos,genPos,freqs,samples]).T
rdf.columns = ['physPos','genPos','x','n']
#Convert appropriate columns to integers
for x in ['physPos', 'x', 'n']:
    rdf[x] = [int(x) for x in rdf[x]]
#Remove sites with 0 polymorphic sites
rdf = rdf[rdf.x > 0]
#Output file
rdf.to_csv(out_file, sep='\t', header=True, index=False)

print ("BM input file output to " + out_file)


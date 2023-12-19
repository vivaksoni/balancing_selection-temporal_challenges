#Create input files for selscan, from .ms file

from __future__ import print_function
import sys
import pandas as pd
import math
import os
import numpy as np
import argparse


#parsing user given constants
parser = argparse.ArgumentParser(description='Information about length of region and sample size')
parser.add_argument('-inFile', dest = 'inFile', action='store', nargs = 1, type = str, help = 'path to gen file (.gen format)')
parser.add_argument('-outFile', dest = 'outFile', action='store', nargs = 1, type = str, help = 'path to output files (suffixes will be added)')
parser.add_argument('-samples', dest = 'samples', action='store', nargs = 1, type = int, help = 'no. of samples in .ms file')
parser.add_argument('-ro', dest = 'ro', action='store', nargs = 1, type = float, help = 'recombination rate')

args = parser.parse_args()
samples = args.samples[0]
inFile = args.inFile[0]
out_file = args.outFile[0]
ro =  args.ro[0]

df = pd.read_csv(inFile, sep='\t', header=0, index_col=False)
pos = list(df.Pos)
loc_names = ['locus_' + str(x) for x in pos]
genPos = [x*1e-8 for x in pos]
chrom = [1 for x in pos]
rdf = pd.DataFrame([chrom,loc_names,genPos,pos]).T
rdf.to_csv(out_file + ".map", sep=' ', header=False, index=False)

df2 = df.filter(regex='A_')
df2 = df2.T
df2.to_csv(out_file + ".hap", sep=' ', header=False, index=False)

print ("Files output to " + out_file)
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
parser.add_argument('-msFile', dest = 'msFile', action='store', nargs = 1, type = str, help = 'path to ms file (.ms format)')
parser.add_argument('-outFile', dest = 'outFile', action='store', nargs = 1, type = str, help = 'path to output files (suffixes will be added)')
parser.add_argument('-regionLen', dest = 'regionLen', action='store', nargs = 1, type = int, help = 'size of simulated region')
parser.add_argument('-samples', dest = 'samples', action='store', nargs = 1, type = int, help = 'no. of samples in .ms file')
parser.add_argument('-ro', dest = 'ro', action='store', nargs = 1, type = float, help = 'recombination rate')

args = parser.parse_args()
chr_len =  args.regionLen[0]
samples = args.samples[0]
ms_file = args.msFile[0]
out_file = args.outFile[0]
ro =  args.ro[0]

#Function to parse .ms file data into nested list of positions and genotypes
#Function takes as input open reading file object and no. of samples
def get_nested_data_list(f_ms, samples):
    l_Pos = [] #list of positions of SNPs
    l_Genos = [] #list of alleles
    d_tmp = {} #dict to store individual allele info for each individual (values) at each site (keys)

    #positions on line 2
    pos_lines = [2]
    for position, line in enumerate(f_ms):
        if position in pos_lines:
            #store positions in list
            pos_list  = line.split()
    #Set file pointer to start of file
    f_ms.seek(0)

    i = 0
    #Loop through positions, storing in list
    for pos in pos_list[1:]:
        #Append position to l_Pos (after converting to float)
        l_Pos.append(float(pos))
        #Add dictionary key for each position, with empty value
        d_tmp[str(i)] = ""
        i += 1 
        
    
    #genotypes on line 3 onwards (use samples argument to determine length of file)
    g_lines = [x for x in range(3, samples + 4)]
    #Loop through lines (ie individuals)
    for position, line in enumerate(f_ms):
        if position in g_lines:
            #Remove newline character
            line1 = line.strip('\n')
            i = 0
            #For each individual, loop through each site, appending allele information for that individual to 
            #the site number in dict
            while i < len(line1):
                d_tmp[str(i)] = d_tmp[str(i)] + line1[i]
                i = i + 1

    f_ms.seek(0)

    #Create nested list of positions and genotypes
    l_data = [[j, d_tmp[str(i)]] for i,j in enumerate(l_Pos)]
    return(l_data)



f_ms = open(ms_file, 'r')
l_data = get_nested_data_list(f_ms, samples)
df = pd.DataFrame(l_data, columns= ['physPos', 'genotype'])
df = df.drop_duplicates('physPos')
l_geno = np.array(df.genotype)
df1 = pd.DataFrame(np.array([list(x) for x in l_geno])).T

df2 = pd.DataFrame([int(np.round(float(x)*chr_len,0)) for x in df.physPos], columns=['physPos'])
df2['genPos'] = df2.physPos * ro
df2['variant'] = ['locus_' + str(x) for x in df2.physPos]
df2['1'] = 1
df2 = df2[['1', 'variant', 'genPos', 'physPos']]

df1.to_csv(out_file + ".hap", sep=' ', header=False, index=False)

df2.to_csv(out_file + ".map", sep=' ', header=False, index=False)
print ("Files output to " + out_file)
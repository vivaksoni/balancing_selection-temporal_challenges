#script takes .ms file and calculates summary statistics across sliding windows using libsequence

#for d in "${demog[@]}"; do for m in "${model[@]}"; do for s in $(seq 1 6); do for n in "${N[@]}"; do for i in $(seq 1 200); do \
#python3 stats_sliding_window.py -msFile ../results/"$d"/"$m"/demog_DFE/100/hSap_DFE"$s"_rep"$i"_"$n".ms \
#-fixedFile ../results/"$d"/"$m"/demog_DFE/100/hSap_DFE"$s"_rep"$i"_"$n".fixed \
#-outFile ../summary_stats/"$d"/"$m"/demog_DFE/100/hSap_DFE \
#"$s"_rep"$i"_"$n".stats -winSize 2000 -stepSize 1000 -regionLen 85005 -samples 100 -N 10000 -burnIn 10; done; done; done; done; done

from __future__ import print_function
import libsequence
import sys
import pandas as pd
import math
import argparse
import numpy as np


#parsing user given constants
parser = argparse.ArgumentParser(description='Information about length of region and sample size')
parser.add_argument('-inFile', dest = 'inFile', action='store', nargs = 1, type = str, help = 'path to gen file (.gen format)')
parser.add_argument('-outFile', dest = 'outFile', action='store', nargs = 1, type = str, help = 'path to output file')
parser.add_argument('-winSize', dest = 'winSize', action='store', nargs = 1, type = int, help = 'size of sliding windows')
parser.add_argument('-stepSize', dest = 'stepSize', action='store', nargs = 1, type = int, help = 'step size for sliding windows')
parser.add_argument('-regionLen', dest = 'regionLen', action='store', nargs = 1, type = int, help = 'size of simulated region')
parser.add_argument('-samples', dest = 'samples', action='store', nargs = 1, type = int, help = 'no. of samples in .ms file')

args = parser.parse_args()
chr_len =  args.regionLen[0]
win_size = args.winSize[0]/float(chr_len)
step_size = args.stepSize[0]/float(chr_len)
samples = args.samples[0]
inFile = args.inFile[0]
out_file = args.outFile[0]


#Get number of segregating sites from .ms file
def get_S(f_ms):
    #Return no. of segregating sites (line 1 of .ms file)
    pos_lines = [1]
    for position, line in enumerate(f_ms):
        if position in pos_lines:
            S = line.split()[1]
    #Set file pointer to start of file
    f_ms.seek(0)
    return S



#Function to create dictionary of polySIM summary statistics. Returns dictionary of summary stats
def get_polySIM_stats(sd):
    #Create polysim object
    ps = libsequence.PolySIM(sd)
    #Create list of methods (ie polySIM summaryStats)
    a = [method for method in dir(ps) if callable(getattr(ps, method)) if not method.startswith('_')]
    #Loop through methods, storing names as keys, and estimates as values in dict
    ss_dict = {}
    for method in a:
        ss_dict[method] = getattr(ps, method)()
        
    return(ss_dict)



#Function to create dictionary of LD stats. Returns dictionary.
def get_LD_stats(sd):
    ld = libsequence.ld(sd)
    df = pd.DataFrame(ld)
    ss_dict = {}
    ss_dict['meanrsq'] = sum(df['rsq'])/len(df['rsq'])
    ss_dict['meanD'] = sum(df['D'])/len(df['D'])
    ss_dict['meanDprime'] = sum(df['Dprime'])/len(df['Dprime'])
    return(ss_dict)



#Read in .ms file, create sd object for libsequence
df = pd.read_csv(inFile, sep='\t', header=0, index_col=False)
#Subset df to include only columns of data from population 1
df2 = df.filter(regex='A_')
arr = np.array(df2)
lst = [[str(x) for x in y] for y in arr]
res = [[''.join(x)] for x in lst]
pos = list(df.Pos / chr_len)
l_data = [[j,res[i][0]] for i,j in enumerate(pos)]
sd = libsequence.SimData(l_data)

#define sliding windows
wins = libsequence.Windows(sd,window_size=win_size,step_len=step_size,starting_pos=0.0,ending_pos=1.0)
num_wins = len(wins)

#Loop through windows
for i, win in enumerate(wins):
	#Create empty dictionary, add replicate number
	d = {}
	d['window'] = i

	#Combine dict output of functions with global dict
	d = {**d, **get_polySIM_stats(win)}
	if len(win.pos()) >= 20: #LD stats are pairwise. If only 1 site exists, it'll show an error.
		d = {**d, **get_LD_stats(win)}
	else:
		d['meanrsq'] = 'NA'
		d['meanD'] = 'NA'
		d['meanDprime'] = 'NA'

	#Convert dict to dataframe and append to file
	df = pd.DataFrame.from_dict(d, orient='index').T
	#Only include header for first window
	if(i==0):
		df.to_csv(out_file, sep='\t', index=False, header=True, mode='a')
	else:
		df.to_csv(out_file, sep='\t', index=False, header=False, mode='a')

	print ("Stats for window " + str(i) + " output to " + out_file)





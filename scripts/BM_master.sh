#!/bin/bash

#Example input
#N=(0.01N 0.1N 1N 2N 10N)
#for n in "${N[@]}"; do ./BM_master.sh 1 100 \
#../results/stationary/rr_fixed_mu_fixed/demog_only/100/hSap \
#BM_inputFiles/inputFiles/stationary/rr_fixed_mu_fixed/demog_only/100/hSap 1e-8 50000 100 "$n"; done


#Display help
Help() { 
   echo "Script to generate BallerMix files from SLIM simulation output (fixed ro only)" 
   echo
   echo "Arguments:"
   echo "1     First replicate number (Will generate range from this number to next argument)."
   echo "2     Max replicate number."
   echo "3     Path to slim output files such that script will affix _rep...ms or fixed"
   echo "4     Path to store BM files created by script will add only the affix to this."
   echo "5     Ro (recombination rate)."
   echo "6     Length of simulated region in bp."
   echo "7     Number of samples."
   echo "8     Sampling time."
   echo
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done

minRep=$1
maxRep=$2
resPath=$3
BMinputPath=$4
ro=$5
regionLen=$6
samples=$7
sampling_time=$8

#####LOOP THROUGH REPLICATES AND PRODUCE BM INPUT FILES#####

echo "Generating BM output files. Output to $BMinputPath"
for i in $(seq $minRep $maxRep); do
    python3 get_BM_input.py \
	-msFile "$resPath"_rep"$i"_"$sampling_time".ms \
        -fixedFile "$resPath"_rep"$i"_"$sampling_time".fixed \
	-outFile "$BMinputPath"_rep"$i"_"$sampling_time".input \
	-ro "$ro" \
	-regionLen "$regionLen" \
	-samples "$samples";
done
echo "completed"


#####CONCATENATE INPUT FILES#####
echo "Concatenating input files"
#Get header row#
head -n1 "$BMinputPath"_rep"$minRep"_"$sampling_time".input > "$BMinputPath"_"$sampling_time".input
#Loop through reps, concatenating to file, whilst skipping header line#
for i in $(seq $minRep $maxRep); do
    tail -n+2 "$BMinputPath"_rep"$i"_"$sampling_time".input >> "$BMinputPath"_"$sampling_time".input;
done
echo "completed"


#####GENERATE SFS FILES#####
echo "Generating sfs files. Output to $BMinputPath"

#B2
python3 BalLeRMix+_v1.py -i "$BMinputPath"_"$sampling_time".input --getSpect --spect "$BMinputPath"_"$sampling_time"_B2.sfs

echo "completed."

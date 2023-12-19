#GENERATE INPUT FILES FOR iHS ANALYSIS FROM SLIM OUTPUTS
python3 get_ihs_input.py \
msFile \
outFile \ 
85005 \
100 \
1e-8

#GENERATE INPUT FILES FOR iHS ANALYSIS FROM FSC2 OUTPUTS
python3 get_ihs_input.py \
inFile \
outFile \ 
100 \
1e-8

#RUN iHS ANALYSIS USING SELSCAN SOFTWARE
Selscan --ihs --hap hapFile --map mapFile --out outPath --trunc-ok --keep-low-freq
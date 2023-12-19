#GENERATE INPUT FILES FOR B2 ANALYSIS FROM SLIM OUTPUT (SEE BM_master.sh HELP FOR MORE INFORMATION)
N=(0.01N 0.1N 1N 10N 25N 50N 75N 100N)
for n in "${N[@]}"; do ./BM_master.sh \
1 200 \
pathToSlimOutputs \
pathToStoreB2InputFiles \ 
1e-8 \
50000 \
100 \
"$n"; done

#GENERATE INPUT FILES FOR B2 ANALYSIS FROM FSC2 OUTPUT (SEE BM_master.sh HELP FOR MORE INFORMATION)
python3 get_BM_input_from_fsc.py \
1 200 \
FSC2file \
outFile \ 
1e-8 \
100

#RUN B2
python3 BalLeRMix+_v1.py \
-i BM2_100/rep1.input \
--spect rep1_B2.sfs \
-o rep1.B2 \
--usePhysPos \
--rec 1e-8


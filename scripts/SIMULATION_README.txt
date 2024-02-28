#####ALL SIMULATIONS RUN IN SLiM4.0.1. SCRIPTS WILL NOT RUN IN SLiM VERSION 3 OR LOWER#####

#RUN EQUILIBRIUM POPULATION, NEUTRAL BACKGROUND SIMULATIONS
slim \
-d d_scale=1 \
-d d_Ncurrent=10000 \
-d "d_folder='results/'" \
-d "d_repID='1'" \
-d d_bp_Nes=100 \
-d "d_rr_map='fixed'" \
-d "d_mu_map='fixed'" \
scripts/demog_only.slim

#RUN DFE SIMULATIONS (EXAMPLE FOR DFE1; SAME INPUT APPLIES TO DFE_iHS.slim; AS WELL AS FOR DFE SIMULATIONS WITH POPULATION SIZE CHANGE: demog_DFE_B2.slim and demog_DFE_iHS.slim)
#FOR VARIABLE RATE SIMULATIONS PARAMETERS FOR d_rr_map AND/OR d_mu_map SHOULD SPECIFY THE LOCATION OF THE MAP FILES IN QUESTION.
slim \
-d d_scale=1 \
-d d_Ncurrent=10000 \
-d "d_folder='results/'" \
-d "d_DFE='1'" \
-d "d_repID='1'" \
-d d_bp_Nes=100 \
-d d_f0=0.1 \
-d d_f1=0.7 \
-d d_f2=0.1 \
-d d_f3=0.1 \
-d "d_rr_map='fixed'" \
-d "d_mu_map='fixed'" \
scripts/DFE_B2.slim

#RUN GRAVEL ET AL. (2011) MODEL OF HUMAN DEMOGRAPHY SIMULATIONS
slim \
-d d_Feq=0.5 \
-d "d_pop='AFR'" \
-d d_bp_gen=73105 \
-d "d_folder='results'" \
-d "d_repID='1'" \
-d "d_rr_map='rr_maps/1.txt'" \
-d "d_mu_map='mu_maps/1.txt'" \
scripts/gravel.slim

#RUN GRAVEL ET AL. (2011) MODEL OF HUMAN DEMOGRAPHY SIMULATIONS WITH NO BALANCING SELECTION
slim \
-d "d_folder='results'" \
-d "d_repID='1'" \
-d "d_rr_map='rr_maps/1.txt'" \
-d "d_mu_map='mu_maps/1.txt'" \
scripts/gravel_null.slim

#RUN HU ET AL. (2023) MODEL OF HUMAN DEMOGRAPHY SIMULATIONS
slim \
-d d_bp_gen=277610 \
-d d_Feq=0.5 \
-d "d_folder='results'" \
-d "d_repID='1'" \
-d "d_rr_map='rr_maps/1.txt'" \
-d "d_mu_map='mu_maps/1.txt'" \
scripts/human_ancestor.slim

#RUN STOCHASTIC LOSS SIMULATIONS WITH DFE
slim \
-d d_scale=1 \
-d "d_folder='results/'" \
-d "d_DFE='1'" \
-d "d_repID='1'" \
-d d_bp_Nes=100 \
-d d_f0=0.1 \
-d d_f1=0.7 \
-d d_f2=0.1 \
-d d_f3=0.1 \
-d "d_rr_map='fixed'" \
-d "d_mu_map='fixed'" \
scripts/stochastic_loss.slim


#RUN STOCHASTIC LOSS SIMULATIONS WITHOUT DFE
slim \
-d d_scale=1 \
-d "d_folder='results/'" \
-d "d_repID='1'" \
-d d_bp_Nes=100 \
-d "d_rr_map='fixed'" \
-d "d_mu_map='fixed'" \
scripts/stochastic_loss_neutral.slim


#RUN PARTIAL SWEEP SIMULATIONS 
slim \
-d "d_folder='results/'" \
-d "d_repID='1'" \
-d d_bp_Nes=100 \
scripts/demog_only_partial_sweep.slim

#RUN FSC2 COALESCENT SIMULATIONS
fsc2702 -i 3pop_admixture.par -n 1000 #ADMIXTURE SIMS
fsc2702 -i 2pop_im.par -n 1000 #MIGRATION SIMS
fsc2702 -i 3pop_2sample.par -n 1000 #HIDDEN STRUCTURE SIMS






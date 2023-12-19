#GET SUMMARY STATS FROM SLIM OUTPUT
python3 stats_sliding_window.py \
-msFile rep1.ms \
-fixedFile rep1.fixed \
-outFile rep1.stats \
-winSize 2000 \
-stepSize 1000 \
-regionLen 85005 \
-samples 100 \
-N 10000 \
-burnIn 10
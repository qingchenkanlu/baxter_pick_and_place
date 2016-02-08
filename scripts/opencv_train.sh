opencv_traincascade \
-data /home/baxter/ros_ws/src/baxter_pick_and_place/data/sdd/ \
-vec /home/baxter/ros_ws/src/baxter_pick_and_place/data/sdd/bin_20_20.vec \
-bg /home/baxter/ros_ws/src/baxter_pick_and_place/data/sdd/bg.txt \
-numPos 120 \
-numNeg 75 \
-numStages 14 \
-precalcValBufSize 256 \
-precalcIdxBufSize 256 \
-acceptanceRationBreakValue 10e-5 \
-featureType HAAR \
-w 20 \
-h 20 \
-bt GAB \
-minHitRate 0.999 \
-weightTrimRate 0.95 \
-maxDepth 1 \
-mode ALL

mv \
/home/baxter/ros_ws/src/baxter_pick_and_place/data/sdd/cascade.xml \
/home/baxter/ros_ws/src/baxter_pick_and_place/data/sdd/bin_cascade.xml

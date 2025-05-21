#!/bin/bash

greedy=/Applications/ITK-SNAP.app/Contents/bin/greedy \

# This resamples the moving image just to confirm it reads the warp in the same way as ANTs

for i in flip identity oblique spacing; do
  $greedy \
    -d 3 \
    -r ${i}/movingToFixed0Warp.nii.gz \
    -ri NN \
    -rf ${i}/fixed.nii.gz \
    -rm ${i}/moving.nii.gz ${i}/movingToFixedDeformed_greedy.nii.gz \
    -rj ${i}/greedy_jacobian_determinant.nii.gz
done

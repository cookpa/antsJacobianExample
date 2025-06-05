#!/bin/bash

greedy=/Applications/ITK-SNAP.app/Contents/bin/greedy

data_dir=$1

if [ -z "$data_dir" ]; then
  echo "Usage: $0 <data_directory>"
  exit 1
fi

# This resamples the moving image just to confirm it reads the warp in the same way as ANTs

$greedy \
    -d 3 \
    -r ${data_dir}/movingToFixed0Warp.nii.gz \
    -ri NN \
    -rf ${data_dir}/fixed.nii.gz \
    -rm ${data_dir}/moving.nii.gz ${data_dir}/movingToFixedDeformed_greedy.nii.gz \
    -rj ${data_dir}/greedy_jacobian_determinant.nii.gz

export ANTS_RANDOM_SEED=25810

inputDir=$1

if [[ -z "$inputDir" ]]; then
  echo "Usage: $0 <input_directory>"
  exit 1
fi

antsRegistration -d 3 -m Demons[ ${inputDir}/fixed.nii.gz , ${inputDir}/moving.nii.gz, 1 , 2 ] -t SyN[0.25, 2, 0] -f 2x1 -s 1x0vox -u 0 -c [10x5] -o [${inputDir}/movingToFixed,${inputDir}/movingToFixedDeformed.nii.gz] -v 1 -n NearestNeighbor

# the antsCorticalThickness way is geometric
CreateJacobianDeterminantImage 3 ${inputDir}/movingToFixed0Warp.nii.gz ${inputDir}/jacobian_geom.nii.gz 0 1
CreateJacobianDeterminantImage 3 ${inputDir}/movingToFixed0Warp.nii.gz ${inputDir}/logJacobian_geom.nii.gz 1 1

# Other way - may have coordinate system issues
CreateJacobianDeterminantImage 3 ${inputDir}/movingToFixed0Warp.nii.gz ${inputDir}/jacobian_fd.nii.gz 0 0
CreateJacobianDeterminantImage 3 ${inputDir}/movingToFixed0Warp.nii.gz ${inputDir}/logJacobian_fd.nii.gz 1 0

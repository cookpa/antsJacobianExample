antsRegistration -d 3 -m Demons[ fixed.nii.gz , moving.nii.gz, 1 , 2 ] -t SyN[0.25, 2, 0] -f 2x1 -s 1x0vox -u 0 -c [10x5] -o [movingToFixed,movingToFixedDeformed.nii.gz] -v 1

CreateJacobianDeterminantImage 3 movingToFixed0Warp.nii.gz jacobian.nii.gz 0 1
CreateJacobianDeterminantImage 3 movingToFixed0Warp.nii.gz logJacobian.nii.gz 1 1

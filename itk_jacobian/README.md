# ITK jacobian

Program here computes the Jacobian matrix using the itkDisplacementFieldTransform method.

It also computes determinant using the dedicated itkDisplacementFieldJacobianDeterminantFilter.

Requires ITKv5, tested with ITK 5.4.3

To build:

```
mkdir ../build
cd ../build
ccmake ../itk_jacobian
make
```

Usage:

```
./itk_compute_jacobian ../identity/movingToFixed0Warp.nii.gz ../identity/
```

Will make


itk_detfilter_jacobian_determinant.nii.gz - determinant from itkDisplacementFieldJacobianDeterminantFilter

itk_transform_local_jacobian.nii.gz - iterates over warp voxels calling
itkDisplacementFieldTransform.ComputeJacobianWithRespectToPosition, outputs
vector image with 9 components for 9 matrix entries in row order

itk_transform_local_jacobian_determinant - determinant of the local matrix above

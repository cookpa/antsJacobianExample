# antsJacobianExample

Example Jacobian computation from a simple test case using ANTs CreateJacobianDeterminantImage

## Generating the warps and Jacobians

Run:

```
  ./reg.sh
```

You must have ANTs installed and on your PATH.


## Viewing results

Example here with [ITK-SNAP](http://itksnap.org)

```
  itksnap -g fixed.nii.gz -o movingToFixedDeformed.nii.gz movingToFixed0Warp.nii.gz jacobian.nii.gz
```

You can customize the display to aid visualization, for example by viewing the deformation
field as a grid.


## Intepretation

The Jacobian is computed in the fixed (template) space using the forward warps. This is what you
want if you need to compare deformations using VBM or other methods in the template space.

The Jacobian determinant is > 1 where the template is expanding to match the moving image. 
In other words, where the moving image volume is greater than the fixed image volume. 

The Jacobian determinant is < 1 where the template is contracting to match the moving image. 
In other words, where the moving image volume is less than the fixed image volume.

In this example there is no global (affine) scaling. These are usually not included in Jacobian
studies as we are usually more interested in local deformations. 

In `antsCorticalThickness.sh`, the registration has affine and deformable stages, but the Jacobian
is similarly calculated on the deformable stage only. It captures local volume differences after
correcting for overall head size and shape. 

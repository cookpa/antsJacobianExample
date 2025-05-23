# antsJacobianExample

Example Jacobian computation from a simple test case using ANTs
CreateJacobianDeterminantImage

Updated to test different header direction matrices.

## Generating the warps and Jacobians

The script runs each example case in a separate directory. You can add more, just add
fixed.nii.gz and moving.nii.gz.

Examples

```
  ./reg.sh identity
  ./reg.sh oblique
```
You must have ANTs installed and on your PATH.


## Viewing results

Example here with [ITK-SNAP](http://itksnap.org)

```
  itksnap -g fixed.nii.gz -o movingToFixedDeformed.nii.gz movingToFixed0Warp.nii.gz jacobian.nii.gz
```

You can customize the display to aid visualization, for example by viewing the deformation
field as a grid.


## Alternative computation methods

ITK has a method to estimate the jacobian at a point, from the transform object.
There's also a filter that produces a determinant image from a displacement
transform. Both of these are implemented in the code in `itkJacobian/`, see the
README in there.

`You can also calculate the determinant with greedy:

```
/Applications/ITK-SNAP.app/Contents/bin/greedy \
  -d 3 \
  -r movingToFixed0Warp.nii.gz \
  -ri NN \
  -rf fixed.nii.gz \
  -rm moving.nii.gz movingToFixedDeformed_greedy.nii.gz \
  -rj greedy_jacobian_determinant.nii.gz
```

This will resample the moving image (to check transforms are correctly
interpreted) and the jacobian determinant.


## Numerical evaluation (requires SimpleITK)

Run

```
  ./evaluate.py .
```

This compares the predicted volume of each label in the moving image from the Jacobian in
the fixed space and the fixed labels. It also compares the deformed moving image volume to
the fixed image volume.


## Intepretation

The Jacobian is computed in the fixed (template) space using the forward warps.

The Jacobian determinant is > 1 where the template is expanding to match the moving image.
In other words, where the moving image volume is greater than the fixed image volume.

The Jacobian determinant is < 1 where the template is contracting to match the moving image.
In other words, where the moving image volume is less than the fixed image volume.

In this example there is no global (affine) scaling. These are usually not included in Jacobian
studies as we are usually more interested in local deformations.

In `antsCorticalThickness.sh`, the registration has affine and deformable stages, but the Jacobian
is similarly calculated on the deformable stage only. It captures local volume differences after
correcting for overall head size and shape.

# antsJacobianExample

Example Jacobian computation from a simple test case using ANTs
CreateJacobianDeterminantImage.

Updated to test different header direction matrices.

If you're here from the ANTs documentation and looking for a simple example of how
Jacobians work, please run
```
./reg.sh identity
```
and look at the results in `identity/`. If you have SimpleITK, you can also get summary
stats with
```
./evaluate.py identity
```

## Jacobian vs Jacobian determinant
The Jacobian is a matrix that approximates the deformation in a small volume around a
point: stretching, scaling, and/or shearing. The Jacobian determinant is a scalar value
that describes the local volume change at a point in the image. It is the determinant of
the Jacobian matrix.

The term "Jacobian" and "Jacobian determinant" are often used interchangeably, but
they are not the same thing. However, for brevity we will refer to the
Jacobian determinant as the Jacobian. If we really mean the matrix, we will call it the
"gradient matrix" as it is called in CreateJacobianDeterminantImage.


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

You can also calculate the determinant with greedy, eg
```
./greedy.sh identity
```

This will resample the moving image (to check transforms are correctly
interpreted) and compute the jacobian determinant.


## Numerical evaluation (requires SimpleITK)

Run

```
  ./evaluate.py identity
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


## Jacobian vs log Jacobian

The Jacobian determinant is a scalar value that describes the local volume change at a
point in the image. It is therefore bounded to be positive, as volumes cannot be zero or
negative under a diffeomorphic transform. It's also not about thhe "middle" where det(J) =
1, meaning no change in volume.

Taking the logarithm of the determinant centers the values around zero and makes the
distribution symmetric, which is often desirable for statistical analysis. If you are
looking at the log jacobian, then 0 means no volume change, > 0 means expansion, and < 0
means contraction. For example, if det(J) = 1.5, indicating expansion of the template,
then log(det(J)) = log(1.5) = 0.405. The corresponding contraction, det(J) = 1/1.5, gives
log(det(J)) = log(1/1.5) = -0.405.


## Volume changes under affine transforms

In this example there is no global (affine) scaling. These are usually not included in Jacobian
studies as we are usually more interested in local deformations. However, the global
volume change is often interesting. This can be computed from the affine transform
determinant, which you can see with `antsTransformInfo`.

In `antsCorticalThickness.sh`, the registration has affine and deformable stages, but the Jacobian
is similarly calculated on the deformable stage only. It captures local volume differences after
correcting for overall head size and shape.

While the scripts here compute the Jacobian in different ways for testing, the method used in `antsCorticalThickness.sh` is `CreateJacobianDeterminantImage`
with the `geometric` option set to 1. If you have ants prior to 2.6.1, there is
a bug affecting the non-geometric jacobians for oblique and non-axial images.
The geometric calculation is not affected.

## The gradient matrix
The full gradient matrix can be computed with
```
CreateJacobianDeterminantImage gradient_matrix.nii.gz movingToFixed0Warp.nii.gz 0 0 1
```
This was also unreliable prior to ANTs 2.6.1 for the reasons [documented
here](https://github.com/ANTsX/ANTs/issues/1884#issuecomment-2920581849). It has not yet
been fully validated. As of June 2025 I am mostly confident it is correct, but need
confirmation using tensor reorientation and tractogaphy to be sure. Use with caution and
please report any issues on the ANTsX GitHub issues page.
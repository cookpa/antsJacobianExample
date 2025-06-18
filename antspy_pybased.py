#!/usr/bin/env python

import ants
import numpy as np
import sys


if len(sys.argv) < 2:
    print("Usage: python antspy_pybased.py <input_dir>")
    sys.exit(1)

input_dir = sys.argv[1]

warp_field = ants.image_read(f"{input_dir}/movingToFixed0Warp.nii.gz")

deformation_gradient = ants.deformation_gradient(warp_field, py_based=True)

ants.image_write(deformation_gradient, f"{input_dir}/antspy_jacobian_pybased.nii.gz")

det_np = np.zeros(deformation_gradient.shape, dtype=np.float32)
logdet_np = np.zeros(deformation_gradient.shape, dtype=np.float32)


# iterate over the deformation gradient and compute the determinant
it = np.ndindex( det_np.shape )

dg_np = deformation_gradient.numpy()

for idx in it:
    def_grad_mat = np.reshape(dg_np[idx], [3,3])
    det_np[idx] = np.linalg.det(def_grad_mat)
    logdet_np[idx] = np.log(det_np[idx])

det_image = ants.from_numpy(det_np, origin=deformation_gradient.origin, spacing=deformation_gradient.spacing,
                            direction=deformation_gradient.direction)

logdet_image = ants.from_numpy(logdet_np, origin=deformation_gradient.origin, spacing=deformation_gradient.spacing,
                            direction=deformation_gradient.direction)

ants.image_write(det_image, f"{input_dir}/antspy_jacobian_det_pybased.nii.gz")
ants.image_write(logdet_image, f"{input_dir}/antspy_jacobian_logdet_pybased.nii.gz")

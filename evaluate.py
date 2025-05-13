#!/usr/bin/env python

import SimpleITK as sitk
import numpy as np
import sys

# File paths
workdir=sys.argv[1]
fixed_path = f"{workdir}/fixed.nii.gz"
moving_path = f"{workdir}/moving.nii.gz"
deformed_path = f"{workdir}/movingToFixedDeformed.nii.gz"

jacobian_paths = [f"{workdir}/jacobian_fd.nii.gz", f"{workdir}/jacobian_geom.nii.gz"]

# Load images
fixed_img = sitk.ReadImage(fixed_path)
moving_img = sitk.ReadImage(moving_path)
deformed_img = sitk.ReadImage(deformed_path)

# Convert to numpy
fixed = sitk.GetArrayFromImage(fixed_img)
moving = sitk.GetArrayFromImage(moving_img)
deformed = sitk.GetArrayFromImage(deformed_img)

# Voxel volume
voxel_volume = np.prod(fixed_img.GetSpacing())

# Evaluate for all non-zero labels
labels = [int(i) for i in np.unique(fixed) if i > 0]

for jac_path in jacobian_paths:

    jacobian_img = sitk.ReadImage(jac_path)
    jacobian = sitk.GetArrayFromImage(jacobian_img)

    for label in labels:
        fixed_mask = fixed == label
        moving_mask = moving == label
        deformed_mask = deformed == label

        jac_predicted_vol = np.sum(jacobian[fixed_mask]) * voxel_volume
        deformed_vol = np.sum(deformed_mask) * voxel_volume
        ground_truth_vol = np.sum(moving_mask) * voxel_volume
        fixed_vol = np.sum(fixed_mask) * voxel_volume

        err_pred_truth = 100 * abs(jac_predicted_vol - ground_truth_vol) / ground_truth_vol if ground_truth_vol else 100
        err_deformed_truth = 100 * abs(deformed_vol - fixed_vol) / fixed_vol if fixed_vol else 100

        results = {
            "Jacobian File": jac_path,
            "Label": label,
            "Fixed Volume (mm^3)": fixed_vol,
            "Moving Volume (mm^3)": ground_truth_vol,
            "Deformed Volume (mm^3)": deformed_vol,
            "Jacobian Predicted Moving Volume (mm^3)": jac_predicted_vol,
            "% Error (Jac vs Truth)": err_pred_truth,
            "% Error (Deformed vs Truth)": err_deformed_truth
        }

        # Print results separated by newline
        print("\n".join([f"{key}: {value}" for key, value in results.items()]))
        print("")
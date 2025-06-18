#!/usr/bin/env python

import SimpleITK as sitk
import numpy as np
import os
import sys
import csv
import pandas as pd

# File paths
workdir = sys.argv[1]
fixed_path = f"{workdir}/fixed.nii.gz"
moving_path = f"{workdir}/moving.nii.gz"
deformed_path = f"{workdir}/movingToFixedDeformed.nii.gz"

jacobian_paths = [
    f"{workdir}/ants_jacobian_det_fd.nii.gz",
    f"{workdir}/ants_jacobian_det_geom.nii.gz",
    f"{workdir}/itk_transform_local_jacobian_determinant.nii.gz",
    f"{workdir}/itk_detfilter_jacobian_determinant.nii.gz",
    f"{workdir}/greedy_jacobian_determinant.nii.gz",
    f"{workdir}/antspy_jacobian_det_pybased.nii.gz"
]

# Load images
fixed_img = sitk.ReadImage(fixed_path)
moving_img = sitk.ReadImage(moving_path)
deformed_img = sitk.ReadImage(deformed_path)

# Convert to numpy
fixed = sitk.GetArrayFromImage(fixed_img)
moving = sitk.GetArrayFromImage(moving_img)
deformed = sitk.GetArrayFromImage(deformed_img)

# Voxel volume
fixed_voxel_volume = np.prod(fixed_img.GetSpacing())
moving_voxel_volume = np.prod(moving_img.GetSpacing())

# Evaluate for all non-zero labels
labels = [int(i) for i in np.unique(fixed) if i > 0]

# Store results
rows = []

for jac_path in jacobian_paths:
    if not os.path.exists(jac_path):
        print(f"Warning: {jac_path} does not exist. Skipping.")
        continue

    jacobian_img = sitk.ReadImage(jac_path)
    jacobian = sitk.GetArrayFromImage(jacobian_img)

    for label in labels:
        fixed_mask = fixed == label
        moving_mask = moving == label
        deformed_mask = deformed == label

        jac_predicted_vol = np.sum(jacobian[fixed_mask]) * fixed_voxel_volume
        deformed_vol = np.sum(deformed_mask) * fixed_voxel_volume
        ground_truth_vol = np.sum(moving_mask) * moving_voxel_volume
        fixed_vol = np.sum(fixed_mask) * fixed_voxel_volume

        err_pred_truth = 100 * abs(jac_predicted_vol - ground_truth_vol) / ground_truth_vol if ground_truth_vol else 100
        err_deformed_truth = 100 * abs(deformed_vol - fixed_vol) / fixed_vol if fixed_vol else 100

        result = {
            "Jacobian File": os.path.basename(jac_path),
            "Label": label,
            "Fixed Volume (mm^3)": fixed_vol,
            "Moving Volume (mm^3)": ground_truth_vol,
            "Deformed Volume (mm^3)": deformed_vol,
            "Jacobian Predicted Moving Volume (mm^3)": jac_predicted_vol,
            "% Error (Jac vs Truth)": err_pred_truth,
            "% Error (Deformed vs Truth)": err_deformed_truth
        }

        rows.append(result)

        # Print
        print("\n".join([f"{k}: {v}" for k, v in result.items()]))
        print("")

# Write CSV
df = pd.DataFrame(rows)
csv_path = os.path.join(workdir, "jacobian_volume_comparison.csv")
df.to_csv(csv_path, index=False)
print(f"Results written to {csv_path}")


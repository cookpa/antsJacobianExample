#!/usr/bin/env python

import SimpleITK as sitk
import numpy as np
import os
import sys
import pandas as pd
import re


def compute_ssd(reference, test):
    """Compute per-component SSD between two Jacobian vector images."""
    assert reference.shape == test.shape
    assert reference.shape[-1] == 9, "Expected last dimension to be 9 (3x3 Jacobian)"
    ssd = np.sum((reference - test) ** 2, axis=tuple(range(reference.ndim - 1)))
    return np.sum((reference - test) ** 2, axis=tuple(range(reference.ndim - 1)))  # shape (9,)

# Input
workdir = sys.argv[1]

# Reference full Jacobian
ref_path = os.path.join(workdir, "itk_transform_local_jacobian.nii.gz")
ref_img = sitk.ReadImage(ref_path)
ref_arr = sitk.GetArrayFromImage(ref_img)
ref_vecs = ref_arr.reshape(-1, 9)  # flatten spatial, keep last dim

# Target Jacobian files
jacobian_paths = [
    os.path.join(workdir, name)
    for name in [
        "ants_jacobian_fd.nii.gz",
        "itk_transform_local_jacobian.nii.gz",
        "antspy_jacobian_pybased.nii.gz"
    ]
]

rows = []

for full_path in jacobian_paths:
    if not os.path.exists(full_path):
        print(f"Missing full Jacobian for {full_path}")
        continue

    test_img = sitk.ReadImage(full_path)
    test_arr = sitk.GetArrayFromImage(test_img)
    try:
        test_vecs = test_arr.reshape(-1, 9)
    except:
        print(f"Invalid shape in {full_path}, skipping.")
        continue

    if test_vecs.shape != ref_vecs.shape:
        print(f"Shape mismatch for {full_path}, skipping.")
        continue

    diffs = (ref_vecs - test_vecs) ** 2
    ssd_components = np.sum(diffs, axis=0)
    ssd_total = np.sum(ssd_components)

    row = {
        "File": os.path.basename(full_path),
        **{f"SSD_{i}": ssd_components[i] for i in range(9)},
        "SSD_total": ssd_total
    }
    rows.append(row)

# Save CSV
df = pd.DataFrame(rows)
out_csv = os.path.join(workdir, "jacobian_ssd_comparison.csv")
df.to_csv(out_csv, index=False)
print(f"Saved SSD results to {out_csv}")

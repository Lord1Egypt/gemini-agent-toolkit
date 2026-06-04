---
name: neuroscience-imaging
description: Neuroimaging data analysis with nilearn, nibabel, and fMRIPrep outputs. Use for fMRI/MRI data loading, brain atlas parcellation, functional connectivity analysis, GLM-based task fMRI, resting-state network analysis, and publication-quality brain visualizations. Covers structural MRI, task fMRI, and rs-fMRI workflows.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Neuroscience Imaging

## Overview

Neuroimaging analysis encompasses structural MRI (morphometry, volumetrics), task fMRI (GLM-based activation), and resting-state fMRI (functional connectivity, ICA) workflows. This skill uses nilearn and nibabel for analysis and visualization, compatible with fMRIPrep-preprocessed data and BIDS-formatted datasets.

## When to Use This Skill

- Loading and visualizing NIfTI (.nii/.nii.gz) brain images
- Extracting time series from ROIs using brain atlases (Schaefer, AAL, Harvard-Oxford)
- Computing functional connectivity matrices and networks
- Running GLM-based task fMRI analysis
- Independent Component Analysis (ICA) for resting-state networks
- Brain parcellation and morphometric analysis
- Whole-brain searchlight and mass-univariate analysis
- Visualizing brain maps, glass brains, and surface plots

## Quick Start

### Loading NIfTI Data

```python
import nibabel as nib
import numpy as np

# Load NIfTI image
img = nib.load("sub-01_task-rest_bold.nii.gz")
data = img.get_fdata()
affine = img.affine
header = img.header

print(f"Image shape: {data.shape}")  # (x, y, z, time)
print(f"Voxel size: {header.get_zooms()}")
print(f"TR: {header.get_zooms()[3]:.2f} s")
print(f"# timepoints: {data.shape[3]}")
```

### Brain Visualization

```python
from nilearn import plotting, image
import matplotlib.pyplot as plt

# Glass brain plot (activation map)
stat_img = "sub-01_contrast-faces_stat.nii.gz"
plotting.plot_glass_brain(
    stat_img,
    threshold=3.5,
    colorbar=True,
    plot_abs=False,
    display_mode="lyrz",
    title="Face vs. Object Contrast",
    output_file="glass_brain.png",
)

# Anatomical underlay
plotting.plot_stat_map(
    stat_img,
    bg_img="sub-01_T1w_MNI.nii.gz",
    threshold=3.5,
    display_mode="z",
    cut_coords=8,
    colorbar=True,
    title="Face activation (z-score)",
    output_file="stat_map_slices.png",
)
print("Brain plots saved.")
```

### Functional Connectivity (ROI-to-ROI)

```python
from nilearn import datasets, input_data
from nilearn.connectome import ConnectivityMeasure
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load atlas
atlas = datasets.fetch_atlas_schaefer_2018(n_rois=200, yeo_networks=7)
atlas_img = atlas.maps
labels = atlas.labels

# Extract time series from ROIs
masker = input_data.NiftiLabelsMasker(
    labels_img=atlas_img,
    standardize=True,
    detrend=True,
    high_pass=0.01,
    low_pass=0.1,
    t_r=2.0,  # TR in seconds
    resampling_target="labels",
)

# Load preprocessed fMRI (fMRIPrep output)
fmri_img = "sub-01_task-rest_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz"
time_series = masker.fit_transform(fmri_img)
print(f"Time series shape: {time_series.shape}")  # (timepoints, n_ROIs)

# Compute correlation matrix
correlation_measure = ConnectivityMeasure(kind="correlation")
corr_matrix = correlation_measure.fit_transform([time_series])[0]
np.fill_diagonal(corr_matrix, 0)  # Zero diagonal

# Plot connectivity matrix
fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(
    corr_matrix,
    cmap="RdBu_r",
    center=0,
    vmin=-0.8,
    vmax=0.8,
    xticklabels=False,
    yticklabels=False,
    ax=ax,
)
ax.set_title("Functional Connectivity Matrix (Schaefer 200 ROIs)", fontsize=13)
plt.tight_layout()
plt.savefig("connectivity_matrix.png", dpi=150)
```

### Task fMRI GLM

```python
from nilearn.glm.first_level import FirstLevelModel
from nilearn import plotting
import pandas as pd
import numpy as np

# Design matrix
frame_times = np.arange(150) * 2.0  # 150 TRs, TR=2s
events = pd.DataFrame({
    "trial_type": ["faces", "objects"] * 10,
    "onset": np.linspace(0, 290, 20),
    "duration": [5.0] * 20,
})

# First-level GLM
fmri_glm = FirstLevelModel(
    t_r=2.0,
    hrf_model="spm",
    standardize=False,
    signal_scaling=0,
    smoothing_fwhm=6.0,
    noise_model="ar1",
)

fmri_img = "sub-01_task-localizer_bold.nii.gz"
fmri_glm = fmri_glm.fit(fmri_img, events=events)

# Compute contrast: faces > objects
z_map = fmri_glm.compute_contrast(
    "faces - objects",
    output_type="z_score",
)
z_map.to_filename("contrast_faces_vs_objects.nii.gz")

# Visualize
plotting.plot_glass_brain(
    z_map,
    threshold=3.0,
    colorbar=True,
    plot_abs=False,
    title="Faces > Objects (z-score)",
    output_file="faces_vs_objects.png",
)
print("GLM analysis complete.")
```

### Resting-State ICA

```python
from nilearn.decomposition import CanICA
from nilearn import plotting
import numpy as np

# Run CanICA (Group ICA)
canica = CanICA(
    n_components=20,
    memory="nilearn_cache",
    memory_level=2,
    random_state=0,
    smoothing_fwhm=6.0,
    threshold=3.0,
    verbose=10,
)

fmri_files = [
    "sub-01_task-rest_bold.nii.gz",
    "sub-02_task-rest_bold.nii.gz",
    "sub-03_task-rest_bold.nii.gz",
]

canica.fit(fmri_files)
components_img = canica.components_img_

# Plot RSN components
plotting.plot_prob_atlas(
    components_img,
    view_type="filled_contours",
    title="Resting-State Networks (ICA)",
    output_file="resting_state_networks.png",
)
print(f"ICA components shape: {components_img.shape}")
```

### Brain Parcellation and Volume Extraction

```python
import nibabel as nib
import numpy as np
import pandas as pd
from nilearn import datasets, input_data

def extract_region_volumes(t1_img_path: str, atlas: str = "aal") -> pd.DataFrame:
    """Extract grey matter volumes per atlas region."""
    if atlas == "aal":
        aal = datasets.fetch_atlas_aal()
        atlas_img = aal.maps
        labels = aal.labels
    elif atlas == "destrieux":
        destrieux = datasets.fetch_atlas_destrieux_2009()
        atlas_img = destrieux.maps
        labels = destrieux.labels

    t1_img = nib.load(t1_img_path)
    atlas_resampled = image.resample_to_img(
        atlas_img, t1_img, interpolation="nearest"
    )
    atlas_data = atlas_resampled.get_fdata().astype(int)

    voxel_volume = np.prod(t1_img.header.get_zooms()[:3]) / 1000  # cc

    volumes = []
    unique_labels = np.unique(atlas_data[atlas_data > 0])
    for label_id in unique_labels:
        voxel_count = (atlas_data == label_id).sum()
        region_name = labels[label_id - 1] if label_id <= len(labels) else f"Region_{label_id}"
        volumes.append({
            "region_id": label_id,
            "region_name": region_name,
            "volume_cc": voxel_count * voxel_volume,
        })

    return pd.DataFrame(volumes)
```

### Seed-Based Connectivity

```python
from nilearn import input_data, plotting
import numpy as np

# PCC seed (default mode network)
pcc_coords = [(0, -52, 18)]  # MNI coordinates

seed_masker = input_data.NiftiSpheresMasker(
    pcc_coords,
    radius=8,
    standardize=True,
    detrend=True,
    high_pass=0.01,
    low_pass=0.1,
    t_r=2.0,
)

brain_masker = input_data.NiftiMasker(
    standardize=True,
    detrend=True,
    high_pass=0.01,
    low_pass=0.1,
    t_r=2.0,
    smoothing_fwhm=6.0,
    memory_level=1,
)

fmri_img = "sub-01_task-rest_bold.nii.gz"
seed_ts = seed_masker.fit_transform(fmri_img)
brain_ts = brain_masker.fit_transform(fmri_img)

# Pearson correlation
seed_corr = np.dot(brain_ts.T, seed_ts) / seed_ts.shape[0]
seed_map = brain_masker.inverse_transform(seed_corr.T)

plotting.plot_stat_map(
    seed_map,
    threshold=0.3,
    vmax=0.8,
    cut_coords=pcc_coords,
    title="PCC Seed-Based Connectivity (Default Mode Network)",
    output_file="pcc_connectivity.png",
)
```

## Key Resources

| Resource | Description |
|----------|-------------|
| fMRIPrep | Preprocessing pipeline (BIDS-compatible) |
| nilearn | Python neuroimaging ML library |
| nibabel | NIfTI/CIFTI file I/O |
| FreeSurfer | Structural MRI cortical parcellation |
| AFNI/FSL | Preprocessing and statistics |
| OpenNeuro | Public fMRI datasets |

## Dependencies

```bash
pip install nilearn nibabel numpy pandas matplotlib seaborn scipy
conda install -c conda-forge nilearn
# For surface analysis:
pip install surfplot brainspace
```

---
name: spatial-transcriptomics
description: Spatial transcriptomics data analysis with Squidpy, SpatialDE, and MERFISH/Visium/Xenium workflows. Use for spatial gene expression analysis, neighborhood enrichment, spatial variable gene detection, cell-cell communication with spatial context, and tissue domain identification. Complements Scanpy for spatially-resolved single-cell data.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Spatial Transcriptomics

## Overview

Spatial transcriptomics combines gene expression profiling with spatial coordinates, enabling study of tissue architecture, cell-cell communication, and spatially variable gene expression. This skill covers analysis of major platforms: 10X Visium, 10X Xenium, MERFISH, seqFISH+, Slide-seq, and Stereo-seq.

## When to Use This Skill

- Analyzing 10X Visium, Xenium, or MERFISH spatial data
- Identifying spatially variable genes (SVGs)
- Computing spatial neighborhood enrichment and interaction scores
- Detecting tissue domains and spatial domains
- Studying cell-cell communication with spatial context
- Integrating spatial data with single-cell reference atlases
- Visualizing gene expression on tissue images

## Quick Start

### Loading Visium Data with Squidpy

```python
import scanpy as sc
import squidpy as sq
import numpy as np

# Load 10X Visium dataset
adata = sq.datasets.visium_fluo_adata()
# Or load your own:
# adata = sc.read_visium("path/to/spaceranger/output/")

print(adata)
print(f"Spots: {adata.n_obs}, Genes: {adata.n_vars}")
print(f"Spatial coords shape: {adata.obsm['spatial'].shape}")

# Basic QC
sc.pp.calculate_qc_metrics(adata, inplace=True)
sc.pl.violin(adata, ["n_genes_by_counts", "total_counts"], jitter=0.4, multi_panel=True)
```

### Standard Preprocessing Pipeline

```python
import scanpy as sc
import squidpy as sq

# Load data
adata = sc.read_visium("spaceranger_output/")

# QC filtering
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)

# Normalize and log transform
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
adata.raw = adata  # Store raw counts

# Highly variable genes
sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)

# PCA, neighbors, UMAP
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=10, n_pcs=40)
sc.tl.umap(adata)

# Clustering
sc.tl.leiden(adata, resolution=0.5)

# Visualize on tissue
sq.pl.spatial_scatter(adata, color="leiden", size=1.5)
```

### Spatially Variable Genes (SpatialDE)

```python
import NaiveDE
import SpatialDE
import pandas as pd
import scanpy as sc

adata = sc.read_visium("spaceranger_output/")
sc.pp.normalize_total(adata, target_sum=1e4)

# Prepare data for SpatialDE
counts = pd.DataFrame(
    adata.X.toarray() if hasattr(adata.X, "toarray") else adata.X,
    columns=adata.var_names,
    index=adata.obs_names,
)
coords = pd.DataFrame(
    adata.obsm["spatial"],
    columns=["x", "y"],
    index=adata.obs_names,
)

# Variance-stabilizing normalization
sample_info = coords.copy()
sample_info["total_counts"] = counts.sum(axis=1)
norm_expr = NaiveDE.stabilize(counts.T).T
resid_expr = NaiveDE.regress_out(sample_info, norm_expr.T, "np.log(total_counts)").T

# Run SpatialDE
results = SpatialDE.run(coords, resid_expr)
results_sorted = results.sort_values("qvalue").head(20)
print("Top spatially variable genes:")
print(results_sorted[["g", "l", "qvalue", "FSV"]].to_string())
```

### Neighborhood Enrichment Analysis

```python
import squidpy as sq
import scanpy as sc

adata = sq.datasets.visium_fluo_adata()
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.leiden(adata)

# Build spatial graph
sq.gr.spatial_neighbors(adata, coord_type="grid", n_rings=2)

# Neighborhood enrichment: which cell types co-localize?
sq.gr.nhood_enrichment(adata, cluster_key="leiden")
sq.pl.nhood_enrichment(
    adata,
    cluster_key="leiden",
    method="average",
    cmap="inferno",
    vmin=-50,
    vmax=100,
)

# Co-occurrence probability
sq.gr.co_occurrence(adata, cluster_key="leiden")
sq.pl.co_occurrence(adata, cluster_key="leiden", clusters="3")
```

### Cell-Cell Interaction with CellChat (spatial mode)

```python
# Using liana for spatial cell-cell interaction
import liana as li
import squidpy as sq
import scanpy as sc

adata = sc.read_h5ad("visium_annotated.h5ad")

# Spatial neighbors graph
sq.gr.spatial_neighbors(adata, coord_type="generic", spatial_key="spatial")

# Run LIANA with spatial awareness
li.mt.rank_aggregate(
    adata,
    groupby="cell_type",
    use_raw=False,
    verbose=True,
)

# Filter spatially co-localized interactions
li.pl.dotplot(
    adata,
    colour="magnitude_rank",
    size="specificity_rank",
    inverse_size=True,
    source_labels=["Tumor", "Fibroblast"],
    target_labels=["T cell", "NK cell"],
    top_n=20,
)
```

### Deconvolution with Cell2Location

```python
import cell2location
import scanpy as sc
import anndata as ad

# Load Visium data
adata_vis = sc.read_visium("spaceranger_output/")
sc.pp.normalize_total(adata_vis, target_sum=1e4)
sc.pp.log1p(adata_vis)

# Load single-cell reference
adata_ref = sc.read_h5ad("reference_scrnaseq.h5ad")

# Train reference signature model
cell2location.models.RegressionModel.setup_anndata(
    adata_ref,
    layer="counts",
    labels_key="cell_type",
    batch_key="sample",
)
mod = cell2location.models.RegressionModel(adata_ref)
mod.train(max_epochs=250, use_gpu=True)

# Export signatures
adata_ref = mod.export_posterior(adata_ref)
inf_aver = adata_ref.varm["means_per_cluster_mu_fg"].T

# Spatial mapping
cell2location.models.Cell2location.setup_anndata(
    adata_vis,
    layer="counts",
    batch_key="sample",
)
mod = cell2location.models.Cell2location(
    adata_vis,
    cell_state_df=inf_aver,
    N_cells_per_location=8,
    detection_alpha=20,
)
mod.train(max_epochs=30000, use_gpu=True)
adata_vis = mod.export_posterior(adata_vis)
print("Deconvolution complete.")
```

### Tissue Domain Detection (GraphST)

```python
import GraphST
import scanpy as sc
import squidpy as sq

adata = sc.read_visium("spaceranger_output/")
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=3000)
adata = adata[:, adata.var.highly_variable]
sc.pp.scale(adata)

# Build spatial graph
sq.gr.spatial_neighbors(adata, coord_type="grid")

# Run GraphST
model = GraphST.GraphST(adata, device="cuda")
adata = model.train()

# Clustering of spatial domains
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=7, n_init=10)
adata.obs["domain"] = kmeans.fit_predict(adata.obsm["emb_pca"]).astype(str)

# Visualize domains
sc.pl.spatial(adata, img_key="hires", color="domain", size=1.5)
```

## Platform Comparison

| Platform | Resolution | Genes | Key Use Case |
|----------|-----------|-------|-------------|
| 10X Visium | 55 µm spots | Whole transcriptome | Tissue architecture |
| 10X Xenium | Single cell | 400-5000 panel | Cell type mapping |
| MERFISH | Single cell | 1000+ | Subcellular resolution |
| seqFISH+ | Single cell | 10,000+ | High-plex, fixed tissue |
| Slide-seq | ~10 µm beads | Whole transcriptome | High spatial resolution |

## Dependencies

```bash
pip install squidpy scanpy anndata SpatialDE NaiveDE
pip install cell2location  # For deconvolution
pip install liana  # For cell-cell interaction
pip install GraphST  # For domain detection
```

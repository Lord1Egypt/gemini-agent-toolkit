---
name: omics-integration
description: Multi-omics data integration using MOFA+, DIABLO, and MixOmics for combining genomics, transcriptomics, proteomics, metabolomics, and epigenomics datasets. Use for identifying shared variation across omics layers, building integrative biomarker models, and discovering cross-modal biological patterns. Best for paired multi-omics cohort studies.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Multi-Omics Integration

## Overview

Multi-omics integration combines data from multiple molecular measurement platforms (RNA-seq, proteomics, ATAC-seq, metabolomics, methylation) to identify shared biological variation and cross-modal regulatory relationships. This skill covers MOFA+ for unsupervised factor analysis, MixOmics/DIABLO for supervised integration, and network-based approaches.

## When to Use This Skill

- Integrating paired multi-omics datasets (same samples across platforms)
- Identifying latent factors that explain variation across omics layers
- Building multi-omics classifiers or biomarker panels
- Finding correlated features across genomics, transcriptomics, and proteomics
- Studying regulatory cascades (DNA → RNA → protein → metabolite)
- Visualizing multi-omics data in low-dimensional space
- Performing network-based multi-omics enrichment

## Quick Start

### MOFA+ (Multi-Omics Factor Analysis)

```python
from mofapy2.run.entry_point import entry_point
import pandas as pd
import numpy as np

# Prepare multi-omics data as list of DataFrames
# Each DataFrame: samples × features, one per omics layer
rna_data = pd.read_csv("rna_normalized.csv", index_col=0)      # 100 samples × 20000 genes
protein_data = pd.read_csv("protein_lfq.csv", index_col=0)     # 100 samples × 5000 proteins
metabolite_data = pd.read_csv("metabolites.csv", index_col=0)  # 100 samples × 1000 metabolites

# Align samples
common_samples = rna_data.index.intersection(protein_data.index).intersection(metabolite_data.index)
rna_data = rna_data.loc[common_samples]
protein_data = protein_data.loc[common_samples]
metabolite_data = metabolite_data.loc[common_samples]

print(f"Shared samples: {len(common_samples)}")
print(f"RNA: {rna_data.shape[1]} features")
print(f"Protein: {protein_data.shape[1]} features")
print(f"Metabolite: {metabolite_data.shape[1]} features")

# Prepare MOFA+ input
ent = entry_point()
ent.set_data_options(scale_groups=False, scale_views=False)
ent.set_data_df(
    pd.concat([rna_data.T, protein_data.T, metabolite_data.T]),
    likelihoods=["gaussian", "gaussian", "gaussian"],
)
ent.set_model_options(factors=15, spikeslab_weights=True, ard_factors=True, ard_weights=True)
ent.set_train_options(iter=1000, convergence_mode="fast", seed=42, gpu_mode=False)

ent.build()
ent.run()
ent.save("mofa_model.hdf5")
print("MOFA+ training complete.")
```

### Loading and Interpreting MOFA+ Results

```python
import mofapy2
from mofapy2.core.entry_point import entry_point
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model
model = entry_point()
model.load_hdf5("mofa_model.hdf5")

# Variance explained per factor per view
r2 = model.calculate_variance_explained()
for view_name, r2_vals in zip(model.data_opts["views"], r2["r2_per_factor"]):
    print(f"\n{view_name} — variance explained per factor:")
    for i, r2_val in enumerate(r2_vals):
        print(f"  Factor {i+1}: {r2_val*100:.1f}%")

# Extract factor values (latent space)
Z = model.nodes["Z"].getExpectation()  # samples × factors
factors_df = pd.DataFrame(Z, index=common_samples, columns=[f"Factor{i+1}" for i in range(Z.shape[1])])

# Visualize factor 1 vs factor 2 colored by clinical variable
sample_meta = pd.read_csv("sample_metadata.csv", index_col=0)
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    factors_df["Factor1"],
    factors_df["Factor2"],
    c=pd.Categorical(sample_meta.loc[common_samples, "condition"]).codes,
    cmap="Set1",
    s=60,
    alpha=0.8,
)
ax.set_xlabel("Factor 1", fontsize=12)
ax.set_ylabel("Factor 2", fontsize=12)
ax.set_title("MOFA+ Latent Space", fontsize=14)
plt.tight_layout()
plt.savefig("mofa_factors.png", dpi=150)
```

### DIABLO (Supervised Multi-Omics Integration)

```python
# DIABLO via mixOmics (R-based, called from Python)
import subprocess
import pandas as pd
import numpy as np

# Write data files for R
rna_data.to_csv("rna_for_diablo.csv")
protein_data.to_csv("protein_for_diablo.csv")
metabolite_data.to_csv("metabolite_for_diablo.csv")
sample_meta[["condition"]].to_csv("labels_for_diablo.csv")

# R script for DIABLO
r_script = """
library(mixOmics)

# Load data
X_rna <- as.matrix(read.csv("rna_for_diablo.csv", row.names=1))
X_protein <- as.matrix(read.csv("protein_for_diablo.csv", row.names=1))
X_metabolite <- as.matrix(read.csv("metabolite_for_diablo.csv", row.names=1))
Y <- read.csv("labels_for_diablo.csv", row.names=1)[,1]

X <- list(RNA = X_rna, Protein = X_protein, Metabolite = X_metabolite)

# Design matrix (strength of connection between data blocks)
design <- matrix(0.1, nrow=3, ncol=3, dimnames=list(names(X), names(X)))
diag(design) <- 0

# Run DIABLO
diablo_res <- block.splsda(X, Y, ncomp=2, design=design)

# Save results
write.csv(diablo_res$variates$RNA, "diablo_rna_components.csv")
write.csv(diablo_res$variates$Protein, "diablo_protein_components.csv")
saveRDS(diablo_res, "diablo_model.rds")
cat("DIABLO complete\\n")
"""

with open("run_diablo.R", "w") as f:
    f.write(r_script)

result = subprocess.run(["Rscript", "run_diablo.R"], capture_output=True, text=True)
print(result.stdout)
```

### Correlation Network (WGCNA-style)

```python
import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import pearsonr, spearmanr
from statsmodels.stats.multitest import multipletests

def build_cross_omics_network(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    correlation_threshold: float = 0.6,
    fdr_threshold: float = 0.05,
    corr_method: str = "spearman",
) -> nx.Graph:
    """Build cross-omics correlation network between two feature matrices."""
    assert df1.index.equals(df2.index), "Samples must be aligned"

    edges = []
    for feat1 in df1.columns[:500]:  # Limit for performance
        for feat2 in df2.columns[:500]:
            if corr_method == "spearman":
                r, p = spearmanr(df1[feat1], df2[feat2])
            else:
                r, p = pearsonr(df1[feat1], df2[feat2])
            if abs(r) > correlation_threshold:
                edges.append({"feat1": feat1, "feat2": feat2, "r": r, "p": p})

    edges_df = pd.DataFrame(edges)
    if len(edges_df) == 0:
        print("No edges found above threshold.")
        return nx.Graph()

    _, fdr, _, _ = multipletests(edges_df["p"], method="fdr_bh")
    edges_df["fdr"] = fdr
    sig_edges = edges_df[edges_df["fdr"] < fdr_threshold]

    G = nx.Graph()
    for _, row in sig_edges.iterrows():
        G.add_edge(row["feat1"], row["feat2"], weight=abs(row["r"]), r=row["r"])

    print(f"Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G

# Build RNA-Protein correlation network
rna_protein_net = build_cross_omics_network(
    rna_data.iloc[:, :200],
    protein_data.iloc[:, :200],
    correlation_threshold=0.7,
)
```

### SNF — Similarity Network Fusion

```python
# SNF for patient stratification across omics
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from scipy.stats import rankdata

def build_similarity_matrix(data: np.ndarray, K: int = 20, sigma: float = 0.5) -> np.ndarray:
    """Build patient similarity matrix from omics data."""
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    dist = pairwise_distances(data_scaled, metric="euclidean")
    # Scaled exponential similarity kernel
    return np.exp(-dist**2 / (sigma * np.median(dist[dist > 0])))

def snf_fuse(*matrices, K: int = 20, t: int = 20) -> np.ndarray:
    """Simple Similarity Network Fusion."""
    n = matrices[0].shape[0]
    W_list = list(matrices)

    # Normalize similarity matrices
    for i in range(len(W_list)):
        row_sums = W_list[i].sum(axis=1, keepdims=True)
        W_list[i] = W_list[i] / (row_sums + 1e-10)

    # Iterative fusion
    for _ in range(t):
        W_new = []
        for i in range(len(W_list)):
            others = [W_list[j] for j in range(len(W_list)) if j != i]
            avg_others = np.mean(others, axis=0)
            W_new.append(W_list[i] @ avg_others @ W_list[i].T)
        W_list = W_new

    return np.mean(W_list, axis=0)

# Build similarity matrices
W_rna = build_similarity_matrix(rna_data.values)
W_protein = build_similarity_matrix(protein_data.values)
W_metabolite = build_similarity_matrix(metabolite_data.values)

# Fuse
fused_matrix = snf_fuse(W_rna, W_protein, W_metabolite, K=20, t=20)
print(f"Fused similarity matrix: {fused_matrix.shape}")

# Cluster patients
from sklearn.cluster import SpectralClustering
clustering = SpectralClustering(n_clusters=3, affinity="precomputed", random_state=42)
patient_clusters = clustering.fit_predict(fused_matrix)
print(f"Patient clusters: {pd.Series(patient_clusters).value_counts().to_dict()}")
```

## Integration Strategy Guide

| Approach | Method | Use Case |
|----------|--------|----------|
| Unsupervised | MOFA+, SNF | Discovery, patient stratification |
| Supervised | DIABLO, LASSO | Biomarker selection, classification |
| Network | Correlation, WGCNA | Regulatory networks, hub genes |
| Dimensionality | UMAP on concatenated | Visualization, clustering |
| Causal | Mendelian randomization | Causal inference |

## Dependencies

```bash
pip install mofapy2 pandas numpy scipy networkx matplotlib seaborn
pip install scikit-learn statsmodels
# R for DIABLO/mixOmics:
# install.packages("BiocManager")
# BiocManager::install("mixOmics")
```

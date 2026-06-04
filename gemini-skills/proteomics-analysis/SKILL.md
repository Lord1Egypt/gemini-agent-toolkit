---
name: proteomics-analysis
description: Mass spectrometry-based proteomics data analysis with pyteomics, spectrum_utils, and MaxQuant/DIA-NN output processing. Use for peptide identification, protein quantification (LFQ, TMT, SILAC), differential expression, PTM analysis, and proteomics data visualization. Covers both DDA and DIA proteomics workflows.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Proteomics Analysis

## Overview

Mass spectrometry-based proteomics enables global identification and quantification of proteins in complex biological samples. This skill covers data processing from MaxQuant/DIA-NN output files, statistical analysis, differential expression, post-translational modification (PTM) analysis, and visualization of proteomic data.

## When to Use This Skill

- Processing MaxQuant proteinGroups.txt or peptides.txt output files
- Analyzing DIA-NN report files for data-independent acquisition experiments
- Statistical differential expression analysis between conditions
- Label-free quantification (LFQ), TMT, and SILAC analysis
- PTM analysis (phosphoproteomics, ubiquitination, acetylation)
- Protein-protein interaction network analysis from AP-MS data
- Visualizing protein abundance, volcano plots, and heatmaps
- Integration with transcriptomics data (multi-omics)

## Quick Start

### Processing MaxQuant Output

```python
import pandas as pd
import numpy as np

# Load MaxQuant proteinGroups
pg = pd.read_csv("proteinGroups.txt", sep="\t", low_memory=False)

# Basic filtering
pg_filtered = pg[
    (pg["Reverse"] != "+") &
    (pg["Potential contaminant"] != "+") &
    (pg["Only identified by site"] != "+")
].copy()

print(f"Proteins before filter: {len(pg)}")
print(f"Proteins after filter: {len(pg_filtered)}")

# Extract LFQ intensity columns
lfq_cols = [c for c in pg_filtered.columns if c.startswith("LFQ intensity")]
print(f"Samples: {len(lfq_cols)}")
print(lfq_cols)

# Replace 0 with NaN (missing values)
intensity_matrix = pg_filtered[lfq_cols].replace(0, np.nan)
intensity_matrix.index = pg_filtered["Gene names"].fillna(pg_filtered["Protein IDs"])

# Log2 transform
log2_matrix = np.log2(intensity_matrix)
print(f"\nLog2 intensity range: {log2_matrix.min().min():.1f} - {log2_matrix.max().max():.1f}")
```

### Missing Value Imputation

```python
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def impute_missing_values(df: pd.DataFrame, method: str = "knn") -> pd.DataFrame:
    """Impute missing values in proteomics matrix."""
    if method == "knn":
        imputer = KNNImputer(n_neighbors=5)
        imputed = imputer.fit_transform(df.T)
        return pd.DataFrame(imputed.T, index=df.index, columns=df.columns)
    elif method == "min_based":
        # MinProb: impute from left tail of distribution (for MNAR)
        result = df.copy()
        for col in df.columns:
            col_min = df[col].quantile(0.01)
            col_std = df[col].std() * 0.3
            n_missing = df[col].isna().sum()
            result.loc[df[col].isna(), col] = np.random.normal(
                col_min, col_std, n_missing
            )
        return result
    else:
        return df.fillna(df.median())

# Apply imputation
log2_imputed = impute_missing_values(log2_matrix, method="knn")
```

### Differential Expression with limma-equivalent (pydeseq2 / scipy)

```python
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

def differential_expression(
    matrix: pd.DataFrame,
    group1_cols: list,
    group2_cols: list,
    fdr_threshold: float = 0.05,
) -> pd.DataFrame:
    """T-test based differential expression for proteomics."""
    results = []
    for protein in matrix.index:
        g1 = matrix.loc[protein, group1_cols].dropna().values
        g2 = matrix.loc[protein, group2_cols].dropna().values

        if len(g1) < 2 or len(g2) < 2:
            continue

        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        lfc = np.mean(g2) - np.mean(g1)

        results.append({
            "protein": protein,
            "log2FC": lfc,
            "pvalue": p_val,
            "mean_g1": np.mean(g1),
            "mean_g2": np.mean(g2),
        })

    result_df = pd.DataFrame(results)
    _, fdr, _, _ = multipletests(result_df["pvalue"].fillna(1), method="fdr_bh")
    result_df["FDR"] = fdr
    result_df["significant"] = (result_df["FDR"] < fdr_threshold) & (abs(result_df["log2FC"]) > 1)

    return result_df.sort_values("FDR")

# Usage
control_cols = ["LFQ intensity ctrl_1", "LFQ intensity ctrl_2", "LFQ intensity ctrl_3"]
treatment_cols = ["LFQ intensity treat_1", "LFQ intensity treat_2", "LFQ intensity treat_3"]

de_results = differential_expression(log2_imputed, control_cols, treatment_cols)
print(f"Significant proteins (FDR<0.05, |LFC|>1): {de_results['significant'].sum()}")
print(de_results.head(15).to_string(index=False))
```

### Volcano Plot

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(10, 8))

# Color by significance and direction
colors = np.where(
    de_results["significant"] & (de_results["log2FC"] > 1), "firebrick",
    np.where(
        de_results["significant"] & (de_results["log2FC"] < -1), "steelblue",
        "lightgray",
    ),
)

ax.scatter(
    de_results["log2FC"],
    -np.log10(de_results["FDR"].clip(lower=1e-15)),
    c=colors,
    alpha=0.7,
    s=20,
    linewidths=0,
)

# Label top proteins
top20 = de_results[de_results["significant"]].head(20)
for _, row in top20.iterrows():
    ax.annotate(row["protein"].split(";")[0], xy=(row["log2FC"], -np.log10(row["FDR"] + 1e-15)),
                fontsize=7, ha="center", va="bottom")

ax.axhline(-np.log10(0.05), linestyle="--", color="gray", linewidth=1)
ax.axvline(1, linestyle="--", color="gray", linewidth=1)
ax.axvline(-1, linestyle="--", color="gray", linewidth=1)
ax.set_xlabel("Log2 Fold Change", fontsize=12)
ax.set_ylabel("-log10(FDR)", fontsize=12)
ax.set_title("Proteomics Differential Expression", fontsize=14)
plt.tight_layout()
plt.savefig("volcano_proteomics.png", dpi=200)
```

### Phosphoproteomics Analysis

```python
import pandas as pd
import numpy as np

# Load MaxQuant Phospho (STY) Sites
phospho = pd.read_csv("Phospho (STY)Sites.txt", sep="\t", low_memory=False)

# Filter contaminants and reverse hits
phospho = phospho[
    (phospho["Reverse"] != "+") &
    (phospho["Potential contaminant"] != "+")
].copy()

# Localization probability filter (class I: > 0.75)
phospho = phospho[phospho["Localization prob"] > 0.75].copy()

# Extract site information
phospho["site"] = (
    phospho["Gene names"].fillna("") + "_" +
    phospho["Amino acid"] + phospho["Position"].astype(str)
)
print(f"High-confidence phosphosites: {len(phospho)}")

# Kinase enrichment analysis
# Extract +/- 7 residue motifs for KinaseXplorer/KSEA
phospho_up = phospho[phospho["log2FC"] > 1]["site"].tolist()
phospho_down = phospho[phospho["log2FC"] < -1]["site"].tolist()
print(f"Upregulated phosphosites: {len(phospho_up)}")
print(f"Downregulated phosphosites: {len(phospho_down)}")
```

### Heatmap of Top Proteins

```python
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Select top significant proteins
top_proteins = de_results[de_results["significant"]].head(50)["protein"].tolist()
heatmap_data = log2_imputed.loc[top_proteins].dropna()

# Z-score normalize
scaler = StandardScaler()
heatmap_norm = pd.DataFrame(
    scaler.fit_transform(heatmap_data.T).T,
    index=heatmap_data.index,
    columns=heatmap_data.columns,
)

fig, ax = plt.subplots(figsize=(12, 14))
sns.clustermap(
    heatmap_norm,
    cmap="RdBu_r",
    center=0,
    row_cluster=True,
    col_cluster=True,
    yticklabels=True,
    figsize=(12, 14),
    vmin=-2,
    vmax=2,
)
plt.savefig("proteomics_heatmap.png", dpi=150, bbox_inches="tight")
```

### DIA-NN Output Processing

```python
import pandas as pd
import numpy as np

# Load DIA-NN main report
report = pd.read_csv("report.tsv", sep="\t")

# Filter by quality metrics
report_filtered = report[
    (report["Q.Value"] < 0.01) &  # Precursor FDR < 1%
    (report["Lib.Q.Value"] < 0.01) &
    (report["PG.Q.Value"] < 0.01)  # Protein group FDR < 1%
].copy()

# Pivot to protein × sample matrix
pg_matrix = report_filtered.pivot_table(
    index="Protein.Group",
    columns="File.Name",
    values="PG.MaxLFQ",
    aggfunc="first",
)
pg_matrix = np.log2(pg_matrix.replace(0, np.nan))
print(f"Protein groups quantified: {pg_matrix.shape[0]}")
print(f"Samples: {pg_matrix.shape[1]}")
```

## Workflow Overview

```
Raw MS files (.raw/.d)
        ↓
MaxQuant / DIA-NN (database search)
        ↓
proteinGroups.txt / report.tsv
        ↓
Filter (reverse, contaminants)
        ↓
Log2 transform → Normalization → Imputation
        ↓
Statistical testing (t-test / limma)
        ↓
FDR correction → Hit list
        ↓
Pathway enrichment + Visualization
```

## Dependencies

```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn
pip install scikit-learn  # For KNN imputation
pip install pyteomics  # MS data processing
pip install spectrum_utils  # Spectrum visualization
pip install gseapy  # Pathway enrichment
```

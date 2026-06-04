---
name: crispr-screen-analysis
description: CRISPR genetic screen analysis using MAGeCK, CRISPRclean, and crispy. Use for pooled CRISPR knockout/activation screens, sgRNA count normalization, gene essentiality scoring, hit calling, pathway enrichment, and QC of CRISPR screen data. Supports both positive and negative selection screens.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# CRISPR Screen Analysis

## Overview

Pooled CRISPR genetic screens (genome-wide KO, CRISPRa, CRISPRi) identify genes essential for cellular fitness, drug response, or phenotype acquisition. This skill covers the complete workflow from raw sequencing reads to validated hits, using MAGeCK for statistical testing, DepMap integration for validation, and pathway enrichment for biological interpretation.

## When to Use This Skill

- Analyzing MAGeCK count files from pooled CRISPR screens
- Computing gene-level essentiality scores (LFC, RRA, MLE)
- Calling hits in positive and negative selection screens
- Identifying synthetic lethal interactions
- QC of sgRNA representation and library dropout
- Pathway enrichment of CRISPR screen hits
- Integrating with DepMap data for cross-cell-line analysis
- Visualizing volcano plots, rank plots, and sgRNA distributions

## Quick Start

### MAGeCK Count (Read → Count Matrix)

```bash
# Count reads from FASTQ
mageck count \
    -l library.csv \
    -n screen_output \
    --sample-label "Day0,Day14_rep1,Day14_rep2" \
    --fastq Day0.fastq.gz Day14_rep1.fastq.gz Day14_rep2.fastq.gz \
    --sgrna-len 20 \
    --trim-5 ACCG \
    --pdf-report
```

### MAGeCK Test (Hit Calling - RRA)

```bash
# Negative selection: essential genes drop out
mageck test \
    -k screen_output.count.txt \
    -t Day14_rep1,Day14_rep2 \
    -c Day0 \
    -n neg_selection \
    --gene-lfc-method median \
    --remove-zero both \
    --remove-zero-threshold 0 \
    --pdf-report
```

### MAGeCK MLE (Maximum Likelihood Estimation)

```bash
# Design matrix for MLE
cat > design_matrix.txt << 'EOF'
Samples	baseline	treatment
Day0	1	0
Day14_rep1	0	1
Day14_rep2	0	1
EOF

mageck mle \
    -k screen_output.count.txt \
    -d design_matrix.txt \
    -n mle_output \
    --norm-method median
```

### Python Analysis of MAGeCK Results

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Load MAGeCK gene summary
gene_summary = pd.read_csv("neg_selection.gene_summary.txt", sep="\t")
print(gene_summary.head())
print(f"Total genes tested: {len(gene_summary)}")

# Separate positive and negative selection results
neg_score = gene_summary[["id", "neg|lfc", "neg|fdr", "neg|rank"]].copy()
neg_score.columns = ["gene", "lfc", "fdr", "rank"]
neg_score["hits"] = neg_score["fdr"] < 0.1

print(f"Negative selection hits (FDR < 0.1): {neg_score['hits'].sum()}")
print(f"\nTop 10 essential genes:")
print(neg_score.nsmallest(10, "fdr")[["gene", "lfc", "fdr"]].to_string(index=False))
```

### Volcano Plot

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gene_summary = pd.read_csv("neg_selection.gene_summary.txt", sep="\t")

fig, ax = plt.subplots(figsize=(10, 7))

# Color coding
colors = np.where(
    (gene_summary["neg|fdr"] < 0.05) & (gene_summary["neg|lfc"] < -0.5),
    "firebrick",
    np.where(gene_summary["neg|fdr"] < 0.05, "steelblue", "lightgray"),
)

ax.scatter(
    gene_summary["neg|lfc"],
    -np.log10(gene_summary["neg|fdr"].clip(lower=1e-10)),
    c=colors,
    alpha=0.6,
    s=15,
    linewidths=0,
)

# Label top hits
top_hits = gene_summary.nsmallest(15, "neg|fdr")
for _, row in top_hits.iterrows():
    ax.annotate(
        row["id"],
        xy=(row["neg|lfc"], -np.log10(row["neg|fdr"] + 1e-10)),
        fontsize=7,
        ha="center",
    )

ax.axhline(-np.log10(0.05), linestyle="--", color="gray", linewidth=1, label="FDR=0.05")
ax.axvline(-0.5, linestyle="--", color="gray", linewidth=1)
ax.set_xlabel("Log Fold Change", fontsize=12)
ax.set_ylabel("-log10(FDR)", fontsize=12)
ax.set_title("CRISPR Screen — Volcano Plot", fontsize=14)
plt.tight_layout()
plt.savefig("volcano_plot.png", dpi=200)
```

### sgRNA QC Analysis

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load count file
counts = pd.read_csv("screen_output.count.txt", sep="\t", index_col=0)

# 1. sgRNA representation (Gini index)
def gini(array):
    array = np.sort(array.astype(float) + 1)
    n = len(array)
    idx = np.arange(1, n + 1)
    return (2 * (idx * array).sum() / (n * array.sum())) - (n + 1) / n

for col in counts.columns[1:]:  # Skip 'Gene' column
    g = gini(counts[col].values)
    print(f"Gini index ({col}): {g:.3f}  ({'OK' if g < 0.2 else 'WARN: uneven'})")

# 2. Replicate correlation
rep1 = np.log2(counts["Day14_rep1"] + 1)
rep2 = np.log2(counts["Day14_rep2"] + 1)
r, p = pearsonr(rep1, rep2)
print(f"\nReplicate correlation: r={r:.3f}, p={p:.2e}")

# 3. Missing sgRNA detection
missing_threshold = 30
for col in counts.columns[1:]:
    missing = (counts[col] < missing_threshold).sum()
    pct = missing / len(counts) * 100
    print(f"sgRNAs < {missing_threshold} reads ({col}): {missing} ({pct:.1f}%)")

# 4. Cumulative distribution plot
fig, ax = plt.subplots(figsize=(8, 5))
for col in counts.columns[1:]:
    vals = np.sort(counts[col].values)
    ax.plot(np.linspace(0, 100, len(vals)), vals, label=col)
ax.set_yscale("log")
ax.set_xlabel("Percentile")
ax.set_ylabel("Read count (log scale)")
ax.set_title("sgRNA Coverage Distribution")
ax.legend()
plt.tight_layout()
plt.savefig("sgrna_distribution.png", dpi=150)
```

### Pathway Enrichment of Screen Hits

```python
import pandas as pd
import gseapy as gp

gene_summary = pd.read_csv("neg_selection.gene_summary.txt", sep="\t")

# Hit list (negative selection, FDR < 0.1)
hit_genes = gene_summary[gene_summary["neg|fdr"] < 0.1]["id"].tolist()
print(f"Hit genes for enrichment: {len(hit_genes)}")

# GSEA preranked
rnk = gene_summary.set_index("id")["neg|lfc"].sort_values()

prerank_res = gp.prerank(
    rnk=rnk,
    gene_sets=["KEGG_2021_Human", "Reactome_2022", "GO_Biological_Process_2023"],
    threads=4,
    min_size=15,
    max_size=500,
    permutation_num=1000,
    outdir="gsea_results",
    seed=42,
    verbose=True,
)

print(prerank_res.res2d.sort_values("fdr").head(10)[
    ["Term", "es", "nes", "pval", "fdr"]
].to_string(index=False))
```

### CRISPRclean — Off-target Correction

```python
# CRISPRclean corrects for sgRNA off-target effects
from crispy.CRISPRData import CRISPRDataSet

dataset = CRISPRDataSet("example_screen")
fc = dataset.crispr.foldchanges

# JACKS normalization
from crispy.Crispy import CrispyClass
cobj = CrispyClass(
    sgrna_fc=fc,
    library=dataset.library,
    gene_controls=dataset.controls,
)
gene_scores = cobj.fit_by_drug()
print(gene_scores.head(20))
```

## Screen Design Reference

| Screen Type | Selection | Goal | MAGeCK Mode |
|-------------|-----------|------|-------------|
| Genome KO (neg) | Dropout | Essential genes | `test` |
| Drug resistance | Enrichment | Resistance genes | `test` |
| CRISPRa | Context-dependent | Gain-of-function | `mle` |
| CRISPRi | Context-dependent | Functional screen | `mle` |
| Synthetic lethal | Dropout + context | Genetic interaction | `mle` |

## Dependencies

```bash
# MAGeCK (via conda)
conda install -c bioconda mageck

# Python packages
pip install pandas numpy matplotlib scipy
pip install gseapy  # GSEA pathway enrichment
pip install crispy  # CRISPRclean off-target correction
```

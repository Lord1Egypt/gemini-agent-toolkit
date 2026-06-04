---
name: metabolomics-analysis
description: Untargeted and targeted metabolomics data analysis using pyMZML, mzTab-M processing, and metabolite identification. Use for LC-MS/GC-MS feature detection, metabolite annotation, differential metabolite analysis, pathway mapping, and metabolic flux visualization. Covers XCMS-compatible workflows in Python.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Metabolomics Analysis

## Overview

Metabolomics is the large-scale study of small molecules (metabolites) within cells, tissues, or biofluids. This skill covers untargeted LC-MS and GC-MS metabolomics workflows including feature extraction, normalization, statistical analysis, metabolite identification, and pathway enrichment using Python-based tools.

## When to Use This Skill

- Processing LC-MS or GC-MS raw data for metabolite profiling
- Feature detection and alignment across samples
- Metabolite identification using MS2 matching (GNPS, mzCloud, HMDB)
- Statistical analysis: PCA, PLS-DA, ANOVA, fold-change
- Differential metabolite analysis between biological conditions
- Metabolic pathway mapping (KEGG, BioCyc, MetaCyc)
- Normalization methods for metabolomics data
- Multi-omics integration with proteomics and transcriptomics

## Quick Start

### Loading mzML Data with pyMZML

```python
from pyteomics import mzml
import numpy as np
import pandas as pd

# Load mzML file
spectra = []
with mzml.MzML("sample.mzML") as reader:
    for spectrum in reader:
        if spectrum["ms level"] == 1:
            spectra.append({
                "scan": spectrum["index"],
                "rt": spectrum["scanList"]["scan"][0]["scan start time"],
                "mz": spectrum["m/z array"],
                "intensity": spectrum["intensity array"],
            })

print(f"MS1 spectra loaded: {len(spectra)}")
print(f"RT range: {spectra[0]['rt']:.2f} - {spectra[-1]['rt']:.2f} min")
```

### Feature Detection and Peak Picking

```python
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy.ndimage import gaussian_filter1d

def extract_ion_chromatogram(spectra: list, mz_target: float, ppm: float = 10.0) -> pd.DataFrame:
    """Extract Extracted Ion Chromatogram (EIC) for a target m/z."""
    mz_tol = mz_target * ppm / 1e6
    eic = []
    for s in spectra:
        mask = np.abs(s["mz"] - mz_target) <= mz_tol
        intensity = s["intensity"][mask].sum() if mask.any() else 0.0
        eic.append({"rt": s["rt"], "intensity": intensity})
    return pd.DataFrame(eic)

def detect_peaks(eic: pd.DataFrame, min_intensity: float = 1000.0) -> list:
    """Detect chromatographic peaks in EIC."""
    smoothed = gaussian_filter1d(eic["intensity"].values, sigma=2)
    peaks, props = find_peaks(smoothed, height=min_intensity, prominence=500, width=3)
    return [
        {
            "rt": eic["rt"].iloc[p],
            "peak_intensity": smoothed[p],
            "width": props["widths"][i],
        }
        for i, p in enumerate(peaks)
    ]

# Example: extract glucose (M+H = 181.0708 Da)
eic = extract_ion_chromatogram(spectra, mz_target=181.0708, ppm=5.0)
peaks = detect_peaks(eic, min_intensity=5000.0)
print(f"Peaks found for m/z 181.0708: {len(peaks)}")
for p in peaks:
    print(f"  RT={p['rt']:.2f} min, Intensity={p['peak_intensity']:.0f}")
```

### HMDB Metabolite Search

```python
import requests
import xml.etree.ElementTree as ET

def search_hmdb_by_mz(mz: float, ppm_tolerance: float = 10.0) -> list:
    """Search HMDB for metabolites matching a given m/z value."""
    ppm_tol_da = mz * ppm_tolerance / 1e6
    url = f"https://hmdb.ca/metabolites/search?query={mz:.4f}&search_type=chemical_formula"
    # HMDB REST API (mass search)
    url = f"https://hmdb.ca/metabolites.xml?monisotopic_molecular_weight={mz:.4f}&ppm={int(ppm_tolerance)}"
    try:
        r = requests.get(url, timeout=30)
        root = ET.fromstring(r.text)
        hits = []
        for metabolite in root.findall(".//metabolite"):
            name = metabolite.findtext("name", "")
            accession = metabolite.findtext("accession", "")
            formula = metabolite.findtext("chemical_formula", "")
            mono_mw = metabolite.findtext("monisotopic_molecular_weight", "")
            hits.append({
                "name": name,
                "hmdb_id": accession,
                "formula": formula,
                "mono_mw": mono_mw,
            })
        return hits
    except Exception as e:
        return [{"error": str(e)}]

hits = search_hmdb_by_mz(181.0708, ppm_tolerance=5.0)
for h in hits[:5]:
    print(f"  {h['name']} ({h['hmdb_id']}) — {h['formula']}")
```

### Feature Matrix Normalization

```python
import pandas as pd
import numpy as np

def normalize_metabolomics(df: pd.DataFrame, method: str = "pqn") -> pd.DataFrame:
    """
    Normalize metabolomics feature matrix.
    methods: 'pqn' (probabilistic quotient), 'sum', 'median', 'zscore'
    Rows = samples, Columns = features
    """
    if method == "pqn":
        # Probabilistic Quotient Normalization
        reference = df.median(axis=0)
        quotients = df.divide(reference, axis=1)
        correction_factors = quotients.median(axis=1)
        return df.divide(correction_factors, axis=0)
    elif method == "sum":
        return df.divide(df.sum(axis=1), axis=0) * df.sum(axis=1).median()
    elif method == "median":
        return df.divide(df.median(axis=1), axis=0) * df.median(axis=1).median()
    elif method == "zscore":
        return (df - df.mean()) / df.std()
    else:
        raise ValueError(f"Unknown method: {method}")

# Log transform and normalize
feature_matrix = pd.read_csv("features.csv", index_col=0)
log_matrix = np.log2(feature_matrix.replace(0, np.nan).fillna(feature_matrix.min().min() / 2))
normalized = normalize_metabolomics(log_matrix, method="pqn")
```

### PCA and PLS-DA

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import cross_val_score

def run_pca(feature_matrix: pd.DataFrame, groups: pd.Series, title: str = "PCA"):
    """PCA with sample groups colored."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(feature_matrix.fillna(0))
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots(figsize=(8, 6))
    unique_groups = groups.unique()
    colors = plt.cm.Set1(np.linspace(0, 1, len(unique_groups)))

    for group, color in zip(unique_groups, colors):
        mask = groups == group
        ax.scatter(coords[mask, 0], coords[mask, 1], label=group, c=[color], s=80, alpha=0.8)

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)", fontsize=11)
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)", fontsize=11)
    ax.set_title(title, fontsize=13)
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png", dpi=150)
    return pca, coords

groups = pd.Series(["Control"] * 6 + ["Treatment"] * 6, index=feature_matrix.index)
pca, coords = run_pca(normalized, groups, "Metabolomics PCA")
```

### Differential Metabolite Analysis

```python
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests

def differential_metabolites(
    matrix: pd.DataFrame,
    group1: list,
    group2: list,
    fold_change_threshold: float = 1.5,
    fdr_threshold: float = 0.05,
) -> pd.DataFrame:
    """Mann-Whitney U test with FDR correction for metabolomics."""
    results = []
    for metabolite in matrix.columns:
        g1 = matrix.loc[group1, metabolite].dropna()
        g2 = matrix.loc[group2, metabolite].dropna()
        if len(g1) < 3 or len(g2) < 3:
            continue
        stat, pval = stats.mannwhitneyu(g1, g2, alternative="two-sided")
        fc = np.median(g2) - np.median(g1)  # Log2 FC
        results.append({"metabolite": metabolite, "log2FC": fc, "pvalue": pval})

    result_df = pd.DataFrame(results)
    _, fdr, _, _ = multipletests(result_df["pvalue"], method="fdr_bh")
    result_df["FDR"] = fdr
    result_df["significant"] = (
        (result_df["FDR"] < fdr_threshold) &
        (abs(result_df["log2FC"]) > np.log2(fold_change_threshold))
    )
    return result_df.sort_values("FDR")

ctrl_samples = [f"ctrl_{i}" for i in range(1, 7)]
treat_samples = [f"treat_{i}" for i in range(1, 7)]
diff_results = differential_metabolites(normalized.T, ctrl_samples, treat_samples)
print(f"Significant metabolites: {diff_results['significant'].sum()}")
```

### KEGG Pathway Mapping

```python
import requests
import pandas as pd

def get_kegg_pathways(hmdb_ids: list) -> pd.DataFrame:
    """Map metabolites to KEGG pathways using KEGG REST API."""
    pathway_data = []
    for hmdb_id in hmdb_ids[:50]:  # Respect rate limits
        try:
            # Convert HMDB ID to KEGG compound ID
            r = requests.get(f"https://hmdb.ca/metabolites/{hmdb_id}.xml", timeout=10)
            # Parse KEGG IDs from response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.text)
            for pathway in root.findall(".//pathway"):
                pathway_data.append({
                    "hmdb_id": hmdb_id,
                    "pathway_name": pathway.findtext("name", ""),
                    "kegg_map_id": pathway.findtext("kegg_map_id", ""),
                })
        except Exception:
            continue
    return pd.DataFrame(pathway_data)

# Get significant metabolite HMDB IDs
sig_metabolites = diff_results[diff_results["significant"]]["metabolite"].tolist()
pathway_map = get_kegg_pathways(sig_metabolites[:20])
print("\nEnriched KEGG pathways:")
print(pathway_map["pathway_name"].value_counts().head(10).to_string())
```

## Key Databases

| Database | Content | URL |
|----------|---------|-----|
| HMDB | Human metabolites | hmdb.ca |
| METLIN | MS2 library | metlin.scripps.edu |
| MassBank | MS spectral library | massbank.eu |
| GNPS | Molecular networking | gnps.ucsd.edu |
| KEGG | Metabolic pathways | kegg.jp |
| MetaboLights | Public datasets | ebi.ac.uk/metabolights |

## Dependencies

```bash
pip install pyteomics pandas numpy scipy matplotlib seaborn
pip install scikit-learn statsmodels
pip install requests lxml  # Database queries
pip install matchms  # Spectral similarity
pip install mzmine  # Feature detection (optional, Java-based)
```

---
name: protein-structure-prediction
description: Protein structure prediction and analysis using AlphaFold2, ESMFold, RoseTTAFold, and ColabFold. Use for 3D structure prediction from amino acid sequences, structure quality assessment, binding site identification, and structural comparison. Best for proteins without experimental structures.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Protein Structure Prediction

## Overview

Protein structure prediction enables researchers to computationally determine the 3D conformation of proteins directly from their amino acid sequences. This skill covers AlphaFold2, ESMFold, RoseTTAFold, and ColabFold for structure prediction, alongside tools for quality assessment, structural alignment, and downstream analysis.

## When to Use This Skill

- Predicting 3D structures of proteins with no experimental structure available
- Comparing predicted vs. experimental structures (PDB)
- Identifying binding sites and functional residues
- Modelling protein complexes (multimers) and protein-protein interactions
- Assessing model confidence using pLDDT scores and PAE maps
- Performing structural alignment and RMSD calculations
- Screening for druggable pockets in predicted structures

## Quick Start

### ESMFold (Fast, API-based)

```python
import requests

def predict_structure_esmfold(sequence: str) -> str:
    """Predict structure via ESMFold API, returns PDB string."""
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=sequence,
        timeout=120,
    )
    response.raise_for_status()
    return response.text

sequence = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL"

pdb_string = predict_structure_esmfold(sequence)
with open("predicted_structure.pdb", "w") as f:
    f.write(pdb_string)
print("Structure saved to predicted_structure.pdb")
```

### ColabFold (AlphaFold2 via MSA server)

```bash
# Install ColabFold
pip install colabfold[alphafold]

# Run prediction (single sequence)
colabfold_batch input.fasta output_dir/ --num-recycle 3 --num-models 5
```

```python
# Batch prediction from FASTA
from pathlib import Path

fasta_content = """>Protein_A
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQ
>Protein_B
ACDEFGHIKLMNPQRSTVWY
"""

Path("sequences.fasta").write_text(fasta_content)
# Then run: colabfold_batch sequences.fasta results/ --num-recycle 3
```

### Structure Analysis with Biopython

```python
from Bio.PDB import PDBParser, DSSP, NeighborSearch
from Bio.PDB.PDBIO import PDBIO
import numpy as np

parser = PDBParser(QUIET=True)
structure = parser.get_structure("predicted", "predicted_structure.pdb")

# Extract pLDDT scores (stored in B-factor column for AlphaFold models)
model = structure[0]
plddts = []
for residue in model.get_residues():
    for atom in residue.get_atoms():
        if atom.name == "CA":
            plddts.append(atom.bfactor)

print(f"Mean pLDDT: {np.mean(plddts):.2f}")
print(f"High-confidence residues (pLDDT > 70): {sum(p > 70 for p in plddts)}/{len(plddts)}")

# Confidence zones
zones = {
    "Very high (>90)": sum(p > 90 for p in plddts),
    "Confident (70-90)": sum(70 < p <= 90 for p in plddts),
    "Low (50-70)": sum(50 < p <= 70 for p in plddts),
    "Very low (<50)": sum(p <= 50 for p in plddts),
}
for zone, count in zones.items():
    print(f"  {zone}: {count} residues")
```

### Structural Alignment (RMSD)

```python
from Bio.PDB import PDBParser, Superimposer
import numpy as np

def calculate_rmsd(pdb1: str, pdb2: str) -> float:
    """Calculate backbone RMSD between two structures."""
    parser = PDBParser(QUIET=True)
    s1 = parser.get_structure("s1", pdb1)[0]
    s2 = parser.get_structure("s2", pdb2)[0]

    atoms1 = [a for r in s1.get_residues() for a in r.get_atoms() if a.name == "CA"]
    atoms2 = [a for r in s2.get_residues() for a in r.get_atoms() if a.name == "CA"]

    min_len = min(len(atoms1), len(atoms2))
    sup = Superimposer()
    sup.set_atoms(atoms1[:min_len], atoms2[:min_len])
    sup.apply(s2.get_atoms())
    return sup.rms

rmsd = calculate_rmsd("predicted_structure.pdb", "experimental_structure.pdb")
print(f"Backbone RMSD: {rmsd:.3f} Å")
```

### Binding Site Prediction with fpocket

```bash
# Install fpocket
conda install -c bioconda fpocket

# Run pocket detection
fpocket -f predicted_structure.pdb

# Parse results
python -c "
import glob, json
pockets = glob.glob('predicted_structure_out/pockets/*.pdb')
print(f'Found {len(pockets)} potential binding pockets')
"
```

## Interpreting AlphaFold pLDDT Scores

| pLDDT Range | Confidence | Interpretation |
|-------------|-----------|----------------|
| > 90 | Very high | Backbone reliable, side chains likely accurate |
| 70–90 | Confident | Good backbone, some side chain uncertainty |
| 50–70 | Low | Use with caution, likely disordered or flexible |
| < 50 | Very low | Likely intrinsically disordered, do not use for docking |

## PAE (Predicted Aligned Error) Analysis

```python
import json
import numpy as np
import matplotlib.pyplot as plt

# Load PAE from AlphaFold JSON output
with open("predicted_structure_predicted_aligned_error_v1.json") as f:
    pae_data = json.load(f)

pae_matrix = np.array(pae_data["predicted_aligned_error"])

fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(pae_matrix, cmap="Greens_r", vmin=0, vmax=30)
plt.colorbar(im, ax=ax, label="Expected Position Error (Å)")
ax.set_xlabel("Scored Residue")
ax.set_ylabel("Aligned Residue")
ax.set_title("Predicted Aligned Error (PAE)")
plt.tight_layout()
plt.savefig("pae_matrix.png", dpi=150)
print("PAE matrix saved.")
```

## Protein Complex Prediction (Multimer)

```bash
# AlphaFold multimer via ColabFold
colabfold_batch complex.fasta results/ \
    --model-type alphafold2_multimer_v3 \
    --num-recycle 6 \
    --num-models 5 \
    --rank iptm+ptm
```

```python
# FASTA format for complex (chains separated by :)
complex_fasta = """>Complex_ProteinA:ProteinB
MKTAYIAKQRQISFVKSHFSRQLE:ACDEFGHIKLMNPQRSTVWY
"""
```

## Common Workflows

### Full Prediction Pipeline

```python
import subprocess
from pathlib import Path
from Bio.PDB import PDBParser
import numpy as np

def run_full_prediction(sequence: str, name: str, output_dir: str = "structures"):
    """Complete structure prediction and analysis pipeline."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # 1. Quick ESMFold prediction
    import requests
    response = requests.post(
        "https://api.esmatlas.com/foldSequence/v1/pdb/",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=sequence,
        timeout=120,
    )
    pdb_file = output_path / f"{name}_esmfold.pdb"
    pdb_file.write_text(response.text)

    # 2. Assess confidence
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(name, str(pdb_file))[0]
    plddts = [a.bfactor for r in structure.get_residues() for a in r if a.name == "CA"]
    mean_plddt = np.mean(plddts)

    print(f"[{name}] ESMFold prediction complete")
    print(f"  Sequence length: {len(sequence)} aa")
    print(f"  Mean pLDDT: {mean_plddt:.1f}")
    print(f"  Confidence: {'High' if mean_plddt > 70 else 'Low'}")
    print(f"  Output: {pdb_file}")

    return str(pdb_file), mean_plddt
```

## Key Databases

- **AlphaFold DB**: `https://alphafold.ebi.ac.uk/` — 200M+ pre-computed structures
- **PDB**: `https://www.rcsb.org/` — experimental structures
- **ESM Atlas**: `https://esmatlas.com/` — ESMFold predictions for MGnify proteins
- **UniProt**: `https://www.uniprot.org/` — sequence + functional annotations

## Dependencies

```bash
pip install biopython requests numpy matplotlib
pip install colabfold[alphafold]  # For AlphaFold2 predictions
conda install -c bioconda fpocket  # For pocket detection
```

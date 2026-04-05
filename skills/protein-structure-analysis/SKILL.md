---
name: Protein Structure Analysis
description: "Expert skill for protein 3D structure analysis using Biotite. Covers PDB/mmCIF parsing, secondary structure assignment, contact maps, binding site detection, B-factor analysis, and structural alignment."
category: structural-biology
tags: protein, structure, biotite, pdb, mmcif, alphafold, secondary-structure, contact-map
source: custom
---

# Protein Structure Analysis

## Use this skill when

- Parsing and manipulating PDB/mmCIF protein structure files
- Analyzing protein secondary structure (DSSP algorithm)
- Computing contact maps and distance matrices
- Detecting and characterizing binding sites
- Performing structural alignment (RMSD calculation)
- Working with AlphaFold predicted structures (pLDDT confidence)
- B-factor analysis and flexibility assessment
- Extracting specific chains, residues, or atom selections

## Do not use this skill when

- Running MD simulations (use OpenMM/GROMACS skills)
- Predicting protein structures from sequence (use AlphaFold/ESMFold)
- Analyzing cryo-EM density maps

## Instructions

### Prerequisites

```bash
pip install biotite numpy matplotlib
# Optional for additional analyses
pip install biopython mdanalysis
```

### Quick Start — Load and Analyze a PDB Structure

```python
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
import biotite.structure.io.pdbx as pdbx
import biotite.database.rcsb as rcsb
import numpy as np

# Download structure from RCSB PDB
file_path = rcsb.fetch("1ATP", "pdb", target_path=".")
pdb_file = pdb.PDBFile.read(file_path)
structure = pdb_file.get_structure(model=1)

# Basic info
print(f"Atoms: {structure.array_length()}")
print(f"Chains: {set(structure.chain_id)}")
print(f"Residues: {struc.get_residue_count(structure)}")

# Filter protein atoms only
protein = structure[struc.filter_amino_acids(structure)]
print(f"Protein residues: {struc.get_residue_count(protein)}")
```

### Secondary Structure Assignment

```python
import biotite.structure as struc

# Assign secondary structure using DSSP-like algorithm
sse = struc.annotate_sse(protein)

# Count elements
from collections import Counter
sse_counts = Counter(sse)
print(f"Alpha helices (a): {sse_counts.get('a', 0)} residues")
print(f"Beta sheets (b): {sse_counts.get('b', 0)} residues")
print(f"Coil (c): {sse_counts.get('c', 0)} residues")

# Helix fraction
helix_fraction = sse_counts.get('a', 0) / len(sse)
print(f"Helix content: {helix_fraction:.1%}")
```

### Contact Map

```python
import biotite.structure as struc
import matplotlib.pyplot as plt
import numpy as np

# Get CA atoms for contact map
ca_atoms = protein[protein.atom_name == "CA"]

# Compute pairwise distances
coords = ca_atoms.coord
dist_matrix = np.sqrt(np.sum((coords[:, None] - coords[None, :]) ** 2, axis=-1))

# Contact map (threshold = 8 Angstroms)
contact_map = dist_matrix < 8.0

plt.figure(figsize=(10, 10))
plt.imshow(contact_map, cmap="binary", origin="lower")
plt.xlabel("Residue Index")
plt.ylabel("Residue Index")
plt.title("Contact Map (8Å threshold)")
plt.colorbar(label="Contact")
plt.savefig("contact_map.png", dpi=150, bbox_inches="tight")
```

### Binding Site Detection

```python
import biotite.structure as struc
import numpy as np

def find_binding_site(structure, ligand_resname: str, radius: float = 5.0):
    """Find residues within radius of a ligand."""
    ligand = structure[structure.res_name == ligand_resname]
    protein = structure[struc.filter_amino_acids(structure)]
    
    if len(ligand) == 0:
        raise ValueError(f"Ligand '{ligand_resname}' not found")
    
    # Calculate distances from each protein atom to nearest ligand atom
    binding_residues = set()
    for atom in protein:
        dists = np.linalg.norm(ligand.coord - atom.coord, axis=1)
        if dists.min() < radius:
            binding_residues.add((atom.chain_id, atom.res_id, atom.res_name))
    
    return sorted(binding_residues)

# Find binding site around ATP
site = find_binding_site(structure, "ATP", radius=5.0)
print(f"Binding site residues ({len(site)}):")
for chain, resid, resname in site:
    print(f"  {chain}:{resname}{resid}")
```

### Structural Alignment (RMSD)

```python
import biotite.structure as struc
import biotite.structure.io.pdb as pdb
import biotite.database.rcsb as rcsb

# Load two structures
struct1 = pdb.PDBFile.read(rcsb.fetch("1ATP", "pdb")).get_structure(model=1)
struct2 = pdb.PDBFile.read(rcsb.fetch("2CPK", "pdb")).get_structure(model=1)

# Get CA atoms from chain A
ca1 = struct1[(struct1.atom_name == "CA") & (struct1.chain_id == "A")]
ca2 = struct2[(struct2.atom_name == "CA") & (struct2.chain_id == "A")]

# Ensure same length (truncate to shorter)
n = min(len(ca1), len(ca2))
ca1, ca2 = ca1[:n], ca2[:n]

# Superimpose and calculate RMSD
fitted, transformation = struc.superimpose(ca1, ca2)
rmsd = struc.rmsd(ca1, fitted)
print(f"RMSD: {rmsd:.2f} Å ({n} CA atoms)")
```

### AlphaFold Confidence (pLDDT)

```python
import biotite.structure.io.pdbx as pdbx
import biotite.database.rcsb as rcsb
import numpy as np

def analyze_alphafold_confidence(structure):
    """Analyze AlphaFold pLDDT confidence scores from B-factors."""
    ca = structure[structure.atom_name == "CA"]
    plddt = ca.b_factor  # AlphaFold stores pLDDT in B-factor column
    
    high_conf = np.sum(plddt > 90) / len(plddt)
    medium_conf = np.sum((plddt > 70) & (plddt <= 90)) / len(plddt)
    low_conf = np.sum((plddt > 50) & (plddt <= 70)) / len(plddt)
    very_low = np.sum(plddt <= 50) / len(plddt)
    
    return {
        "mean_plddt": float(np.mean(plddt)),
        "high_confidence_pct": f"{high_conf:.1%}",
        "medium_confidence_pct": f"{medium_conf:.1%}",
        "low_confidence_pct": f"{low_conf:.1%}",
        "very_low_confidence_pct": f"{very_low:.1%}",
        "most_confident_region": f"residues {np.where(plddt > 90)[0][0]+1}-{np.where(plddt > 90)[0][-1]+1}",
    }
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Contact threshold | 8.0 Å | Standard for protein contact maps |
| Binding site radius | 5.0 Å | Distance cutoff for binding site residues |
| pLDDT high confidence | >90 | AlphaFold confident prediction |
| pLDDT low confidence | <50 | Likely disordered region |

### Version Compatibility

- Biotite: 0.40+
- NumPy: 1.24+
- Matplotlib: 3.7+

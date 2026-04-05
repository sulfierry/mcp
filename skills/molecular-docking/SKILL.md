---
name: Molecular Docking
description: "Expert skill for molecular docking simulations, virtual screening, and binding pose prediction. Covers AutoDock Vina, DiffDock, and DockTPrep integration for drug-target interaction studies."
category: structural-biology
tags: docking, autodock, vina, diffdock, virtual-screening, binding-affinity, drug-discovery
source: custom
---

# Molecular Docking

## Use this skill when

- Setting up molecular docking simulations with AutoDock Vina or DiffDock
- Preparing receptor and ligand structures for docking (DockTPrep pipeline)
- Running virtual screening campaigns against protein targets
- Analyzing docking results: binding poses, affinity scores, interaction fingerprints
- Converting between molecular file formats (PDB, PDBQT, MOL2, SDF)
- Validating docking protocols with known crystal structures (redocking)

## Do not use this skill when

- Performing molecular dynamics simulations (use MD-specific tools)
- Working with protein-protein docking (use HADDOCK or ClusPro)
- Doing quantum mechanics/molecular mechanics (QM/MM) calculations

## Instructions

### Prerequisites

```bash
# AutoDock Vina
pip install vina
# OR install via conda
conda install -c conda-forge autodock-vina

# For DiffDock (GPU recommended)
pip install diffdock

# Structure preparation
pip install biotite rdkit-pypi openbabel-wheel meeko
```

### Quick Start — AutoDock Vina

```python
from vina import Vina

# 1. Initialize
v = Vina(sf_name='vina')

# 2. Set receptor (PDBQT format)
v.set_receptor('receptor.pdbqt')

# 3. Set ligand
v.set_ligand_from_file('ligand.pdbqt')

# 4. Define search box (centered on binding site)
v.compute_vina_maps(
    center=[15.190, 53.903, 16.917],  # Active site coordinates
    box_size=[20, 20, 20]              # Box dimensions in Angstroms
)

# 5. Dock
v.dock(exhaustiveness=32, n_poses=10)

# 6. Get results
energies = v.energies()
print(f"Best binding affinity: {energies[0][0]:.2f} kcal/mol")

# 7. Write output poses
v.write_poses('docking_results.pdbqt', n_poses=5, overwrite=True)
```

### Structure Preparation with Biotite

```python
import biotite.structure.io.pdb as pdb
import biotite.structure as struc

# Load PDB structure
pdb_file = pdb.PDBFile.read("protein.pdb")
structure = pdb_file.get_structure(model=1)

# Remove water molecules and heteroatoms
protein = structure[struc.filter_amino_acids(structure)]

# Select binding site residues (within 5Å of known ligand)
ligand = structure[structure.res_name == "LIG"]
binding_site = structure[struc.distance(structure, ligand.coord.mean(axis=0)) < 5.0]

print(f"Binding site residues: {len(set(binding_site.res_id))}")
```

### Virtual Screening Pipeline

```python
import os
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors

def prepare_ligand_library(sdf_file: str, output_dir: str):
    """Filter and prepare ligands for docking."""
    supplier = Chem.SDMolSupplier(sdf_file, removeHs=False)
    prepared = 0
    
    for mol in supplier:
        if mol is None:
            continue
        
        # Lipinski filter
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        
        if mw > 500 or logp > 5 or hbd > 5 or hba > 10:
            continue
        
        # Generate 3D conformer
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Save as SDF
        name = mol.GetProp("_Name") if mol.HasProp("_Name") else f"lig_{prepared}"
        writer = Chem.SDWriter(f"{output_dir}/{name}.sdf")
        writer.write(mol)
        writer.close()
        prepared += 1
    
    return prepared

def batch_dock(receptor_pdbqt: str, ligand_dir: str, center: list, 
               box_size: list = [20, 20, 20], exhaustiveness: int = 16):
    """Run docking for all ligands in a directory."""
    from vina import Vina
    
    results = []
    v = Vina(sf_name='vina')
    v.set_receptor(receptor_pdbqt)
    v.compute_vina_maps(center=center, box_size=box_size)
    
    for lig_file in Path(ligand_dir).glob("*.pdbqt"):
        v.set_ligand_from_file(str(lig_file))
        v.dock(exhaustiveness=exhaustiveness, n_poses=3)
        
        energies = v.energies()
        results.append({
            "ligand": lig_file.stem,
            "best_affinity": energies[0][0],
            "poses": len(energies)
        })
    
    # Sort by affinity (most negative = best)
    results.sort(key=lambda x: x["best_affinity"])
    return results
```

### Key Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `exhaustiveness` | 8 | 1-128 | Search thoroughness. 32+ for publication |
| `n_poses` | 5 | 1-20 | Number of output poses |
| `box_size` | [20,20,20] | 10-40 Å | Search space dimensions |
| `energy_range` | 3 | 1-10 | Max energy diff from best (kcal/mol) |
| `seed` | random | any int | Reproducibility seed |

### Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No poses found | Box too small or misplaced | Increase box_size, verify center coords |
| Very positive energies | Steric clashes | Check ligand preparation, add hydrogens |
| PDBQT errors | Wrong format | Use `meeko` or `obabel` for conversion |
| Slow docking | High exhaustiveness | Reduce for screening, increase for validation |

### Version Compatibility

- AutoDock Vina: 1.2.5+
- RDKit: 2023.09+
- Biotite: 0.40+
- Meeko: 0.5+

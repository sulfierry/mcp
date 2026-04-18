---
name: chai-1-rosettafold
description: "Chai-1 (Chai Discovery 2024) and RoseTTAFold/RoseTTAFold2/RoseTTAFold All-Atom structure prediction alternatives to AlphaFold. Complex prediction with ligand/NA/modified residues, MSA-free mode, constraint-guided prediction. Triggers on Chai-1, Chai Discovery, RoseTTAFold, RF2, RFAA, structure prediction, MSA-free."
category: scientific-writing
tags: [chai, rosettafold, structure-prediction, msa-free]
---

# Chai-1 & RoseTTAFold

## Chai-1 (Chai Discovery, Sep 2024)
OSS weights + API. AF3-class: protein + NA + ligand + covalent modifications.

### Install
```bash
pip install chai_lab
# Or clone: github.com/chaidiscovery/chai-lab
```

### Minimal example
```python
from chai_lab.chai1 import run_inference

candidates = run_inference(
    fasta_file="complex.fasta",
    output_dir="out/",
    num_trunk_recycles=3,
    num_diffn_timesteps=200,
    seed=42,
    device="cuda",
    use_esm_embeddings=True,          # PLM-only mode (no MSA)
    constraints=[...],                 # optional distance/contact constraints
)
```

### FASTA schema (multi-entity)
```
>chain_1|protein
MENFKV...
>chain_2|protein
GSSHHHH...
>chain_3|ligand|smiles
CC(=O)Oc1ccccc1C(=O)O
>chain_4|ligand|ccd
ATP
>chain_5|rna
GUGACCC...
```

### Key advantage
- **PLM mode (no MSA) rivals MSA AF2** for many targets — useful for orphan proteins.
- Constraint-guided: inject user distance/contact restraints (XL-MS, SAXS, EM density).

## RoseTTAFold family

| Model | Purpose | Released |
|-------|---------|----------|
| RoseTTAFold (RF) | AF2-era 3-track model | 2021 |
| RoseTTAFold2 (RF2) | Improved complex prediction | 2023 |
| **RoseTTAFold All-Atom (RFAA)** | Protein + NA + metal + ligand | 2024 |
| **RoseTTAFold Diffusion** (RFdiffusion) | De novo design — see `rfdiffusion-design` | 2023+ |

### RFAA install
```bash
git clone https://github.com/baker-lab/RoseTTAFold-All-Atom
conda env create -f RFAA-linux.yml
conda activate RFAA
```

Requires: mmseqs2 DB, PDB templates, ~50GB disk.

### Usage
```bash
python -u rf2aa/run_inference.py \
  --config-path config/inference \
  --config-name base \
  input.pdb=receptor.pdb \
  small_molecule.input_file=ligand.sdf
```

## When Chai-1 vs RFAA

| Need | Use |
|------|-----|
| Fast, modern API | Chai-1 |
| MSA-free prediction | Chai-1 (PLM mode) |
| Metal-binding or complex metal clusters | RFAA |
| Constraint-guided (contacts, distances) | Chai-1 |
| Integration with RFdiffusion design pipeline | RFAA (same ecosystem) |

## Confidence / output

Chai-1:
- `.cif` structures (top-5 by default)
- `chains_info.json` — per-chain confidence
- `aggregate_score.json` — global

RFAA:
- `.pdb` + `.npz` with lDDT + pAE
- ptm / iptm tokens

## Integration

- Cross-validate: same input → AF3 + Boltz + Chai-1 + RFAA → consensus structure
- Top of ensemble → MD in OpenMM/GROMACS
- Ligand-bound Chai output → refine with Rosetta FastRelax

## Comparison table

| Feature | Boltz-1 | Chai-1 | AF3 | RFAA |
|---------|---------|--------|-----|------|
| License | MIT | Non-commercial weights + Apache code | Academic server only | Academic |
| Ligand | ✅ | ✅ | ✅ | ✅ |
| Nucleic acid | ✅ | ✅ | ✅ | ✅ |
| Metal cluster | partial | partial | ✅ | ✅ (strong) |
| MSA-free mode | ✅ (ESM PLM) | ✅ (ESM PLM) | ❌ | ❌ |
| Constraint-guided | partial | ✅ | ❌ | partial |
| API | — | Chai API | DeepMind server | — |

## Citations
- Chai Discovery — "Chai-1: Decoding the molecular interactions of life" (bioRxiv 2024)
- Baek et al. — RoseTTAFold (Science 2021)
- Krishna et al. — RFAA (Science 2024)

## Related
- `alphafold-suite` — AF2/AF3
- `boltz-structure-prediction` — OSS AF3 alternative
- `rfdiffusion-design` — RF-based generative design
- `proteinmpnn-suite` — sequence design on RF scaffolds

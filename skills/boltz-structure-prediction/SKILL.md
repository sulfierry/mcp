---
name: boltz-structure-prediction
description: "Boltz-1 and Boltz-2 open-source AlphaFold3-class structure prediction (MIT Jameel Clinic, 2024-2025). Protein + ligand + nucleic acid + modified residues complexes. Diffusion-based. Installation (uv/pip), YAML input schema, MSA handling, template injection, confidence (pLDDT/PAE/pTM/ipTM). Triggers on Boltz, Boltz-1, Boltz-2, structure prediction, AF3 alternative, protein-ligand complex."
category: scientific-writing
tags: [boltz, alphafold3, structure-prediction, diffusion, protein]
---

# Boltz-1 / Boltz-2

## When to use
- Need AlphaFold3-class prediction (protein + ligand + nucleic acid + modified residues)
- Want fully OSS / MIT-license AF3 alternative
- Predicting complexes where ligand/cofactor matters (AF2-multimer can't)
- Structure + affinity in one pass (Boltz-2)

## Models

| Model | Released | Capabilities | License |
|-------|----------|--------------|---------|
| **Boltz-1** | Oct 2024 | Protein+NA+ligand+mod-residue structure | MIT |
| **Boltz-2** | 2025 | Boltz-1 + binding-affinity prediction in one pass | MIT |

Source: `github.com/jwohlwend/boltz`.

## Install (uv or pip)

```bash
# Recommended: uv for reproducibility
uv pip install boltz
# Or pip
pip install boltz -U
```

Requires CUDA GPU (≥24 GB for long chains). CPU fallback for small systems.

## Input: YAML schema

```yaml
version: 1
sequences:
  - protein:
      id: [A]
      sequence: "MENFKV..."
      msa: default           # or path to a3m/stockholm
  - ligand:
      id: [B]
      ccd: ATP               # PDB Chemical Component Dictionary code
  - ligand:
      id: [C]
      smiles: "CC(=O)Oc1ccccc1C(=O)O"   # aspirin
  - rna:
      id: [D]
      sequence: "GUGACCC..."
constraints:
  - bond:                    # covalent modification
      atom1: [A, 42, NZ]
      atom2: [B, 1, C2]
templates:
  - cif: path/to/template.cif
    chain_id: A
properties:                  # Boltz-2 only
  - affinity:
      binder: B
```

Run:
```bash
boltz predict input.yaml --out_dir predictions/ --model boltz2
```

## MSA handling

- `msa: default` → Boltz generates via ColabFold-style databases
- Pre-computed MSA → path to `.a3m` or `.sto`
- No MSA (`msa: null`) → orphan prediction (lower accuracy)

Protein-language-model (PLM) embeddings generated internally (ESM-like).

## Output files

```
predictions/
├── ligand_protein_model_0.cif         # ranked structures
├── ligand_protein_model_[1-4].cif
├── confidence_ligand_protein.json     # pLDDT/pTM/ipTM/PAE
└── ligand_protein_affinity.json       # Boltz-2 only
```

## Confidence metrics

| Metric | Range | Meaning |
|--------|-------|---------|
| **pLDDT** | 0-100 | Per-residue local confidence |
| **pTM** | 0-1 | Global fold confidence |
| **ipTM** | 0-1 | Inter-chain confidence (complexes) |
| **PAE** | 0-30 Å | Pairwise aligned error |
| **affinity** (Boltz-2) | pKd | Predicted binding affinity |

Rules of thumb:
- pLDDT > 90: high confidence (near-X-ray quality)
- 70-90: generally correct fold
- 50-70: low confidence, likely wrong
- < 50: disordered

## Performance

| System | Boltz-1 runtime (H100) |
|--------|------------------------|
| 100 AA protein + ligand | ~1 min |
| 500 AA + ligand | ~5 min |
| 1000 AA complex + ligand | ~15 min |

Batch inference 4-10× faster via `--num_workers`.

## Comparison: Boltz / AlphaFold3 / Chai-1

| Feature | Boltz-2 | AF3 (server) | Chai-1 |
|---------|---------|--------------|--------|
| Open source | ✅ MIT | ❌ academic-only server | ✅ weights |
| Ligand | ✅ | ✅ | ✅ |
| Nucleic acid | ✅ | ✅ | ✅ |
| Modified residues | ✅ | ✅ | ✅ |
| Affinity | ✅ (Boltz-2) | ❌ | ❌ |
| Local install | ✅ | ❌ | ✅ |
| API | — | DeepMind server | Chai Discovery API |

## Integration with other tools

- **Receptor prep for docking**: export best `*.cif` → convert with openbabel/meeko
- **MD input**: Boltz predictions → OpenMM/GROMACS topology
- **Refinement**: Rosetta / FastRelax on Boltz output
- **Validation**: MolProbity score, Ramachandran analysis

## Common failure modes

- Empty MSA → low-confidence prediction (always provide MSA when possible)
- SMILES without explicit Hs → occasional tautomer issues (canonicalize with RDKit first)
- Long disordered regions → noisy pLDDT (expected; not a bug)
- Ligand covalent attachment → must use `constraints.bond` block

## Citation

- Wohlwend et al. — "Boltz-1: Democratizing Biomolecular Interaction Modeling" (bioRxiv 2024)
- Passaro et al. — "Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction" (bioRxiv 2025)

## Related skills

- `alphafold-suite` — AF2/AF3 comparison and combined use
- `chai-1-rosettafold` — alternative OSS AF3-class models
- `rfdiffusion-design` — generate new structures to feed Boltz
- `proteinmpnn-suite` — sequence design on Boltz-predicted scaffolds
- `modern-ai-docking` — DiffDock-L post-Boltz complex

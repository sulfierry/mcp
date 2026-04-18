---
name: proteinmpnn-suite
description: "ProteinMPNN, LigandMPNN, SolubleMPNN, ThermoMPNN for sequence design on fixed backbone. Inverse folding — designs sequences that fold into a given 3D structure. Use for de novo binder sequences after RFdiffusion, thermostabilization, solubility improvement. Triggers on ProteinMPNN, LigandMPNN, SolubleMPNN, ThermoMPNN, inverse folding, sequence design."
category: scientific-writing
tags: [proteinmpnn, sequence-design, inverse-folding, binder]
---

# ProteinMPNN Suite

## Models (Baker lab)

| Model | Adds to ProteinMPNN | Released |
|-------|---------------------|----------|
| **ProteinMPNN** | Base: sequence for protein backbone | 2022 |
| **LigandMPNN** | Ligand-aware context | 2023 |
| **SolubleMPNN** | Biased toward soluble sequences | 2023 |
| **ThermoMPNN** | Single-mutation ΔΔG prediction (not design) | 2024 |
| **MembraneMPNN** | Lipid-embedded proteins | 2023 |

## Install
```bash
git clone https://github.com/dauparas/ProteinMPNN
git clone https://github.com/dauparas/LigandMPNN
conda env create -f ProteinMPNN/env.yml
```

## Basic use — design sequence for given backbone

```bash
python ProteinMPNN/protein_mpnn_run.py \
  --pdb_path backbone.pdb \
  --out_folder designs/ \
  --num_seq_per_target 50 \
  --sampling_temp "0.1" \
  --seed 42 \
  --batch_size 10
```

Sampling temperature:
- `0.1`: conservative, high pLL — recommended for first-pass
- `0.3-0.5`: more diverse (~50% seq identity among outputs)
- `0.7+`: very diverse, may be less foldable

## Fix specific residues (epitope preservation)

```bash
python protein_mpnn_run.py \
  --pdb_path backbone.pdb \
  --fixed_positions_jsonl fix.jsonl \   # {"chain":"A", "fixed_positions":[15, 47, 92]}
  ...
```

## Bias amino-acid composition

```bash
# Example: discourage Cys (disulfide), Met (oxidation)
python protein_mpnn_run.py \
  --omit_AAs "CM" \
  --bias_AA_jsonl bias.jsonl \   # {"K": -0.5, "R": -0.5}  # reduce positive charge
  ...
```

## LigandMPNN

```bash
python LigandMPNN/run.py \
  --pdb_path protein_ligand.pdb \
  --ligand_mpnn_use_side_chain_context 1 \
  --out_folder designs/ \
  --number_of_batches 50
```

## SolubleMPNN (tweaked training data)

```bash
python protein_mpnn_run.py \
  --model_name v_48_020_soluble \
  ...
```

Use when designing sequences for soluble expression (E. coli periplasm, mammalian secretion).

## ThermoMPNN (stability prediction, not design)

```python
from thermompnn import ThermoMPNN
model = ThermoMPNN.from_pretrained()
ddG = model.predict(pdb="mutant.pdb", chain="A", position=42, mutation="L")  # returns kcal/mol
```

Use to rank single-point mutations before experimental expression.

## Canonical pipeline (binder design)

```
1. RFdiffusion → N scaffolds
2. ProteinMPNN → K sequences per scaffold (K = 4-8)
3. ESMFold / AF2 → predict structure of each
4. Filter: pLDDT > 80 AND RMSD to scaffold < 2 Å
5. Compute interface score (Rosetta / PatchDock)
6. Experimental synthesis of top 10-100
```

## Sampling considerations
- `--num_seq_per_target 8` gives reasonable diversity per scaffold
- For high-throughput: 100+ designs per backbone, filter heavily
- Use `--seed` for reproducibility (required in protocols)

## Output
```
designs/
├── seqs/*.fa            # FASTA sequences
└── scores/*.pkl         # per-residue pseudo-log-likelihood
```

## Integration
- Input from RFdiffusion: backbone PDBs → ProteinMPNN input
- Output feeds AF2/Boltz/Chai for validation
- Stability check: FoldX / ThermoMPNN / Rosetta ddg_monomer
- Developability: SAP score, humanness (for antibodies)

## Validation metrics
- **pLL** (pseudo log-likelihood): higher = more "protein-like"
- **pLDDT** (AF2 re-fold): > 80 typical threshold
- **RMSD to scaffold** (from ProteinMPNN): < 2 Å
- **Rosetta energy**: normalized per residue

## Common failure modes
- All cysteines → spurious disulfides → use `--omit_AAs "C"` if unneeded
- Designs don't refold in AF2 (low pLDDT): drop scaffold or try more sequences
- Too conservative (~90% identity to native): increase sampling temp
- Over-glycine loops: happens with short contigs; use `--bias_AA_jsonl` to discourage

## Citation
- Dauparas et al. — ProteinMPNN (Science 2022)
- Dauparas — LigandMPNN (2023)
- Goverde et al. — de novo binder design with RFdiffusion + PMPNN (Nature 2024)
- Dieckhaus — ThermoMPNN (PNAS 2024)

## Related
- `rfdiffusion-design` — backbone generation
- `alphafold-suite`, `boltz-structure-prediction`, `chai-1-rosettafold` — validate
- `foldx-rosetta-stability` — ddG refinement
- `modern-ai-docking` — post-design ligand docking

---
name: rfdiffusion-design
description: "RFdiffusion and RFdiffusion-All-Atom for de novo protein backbone design. Motif scaffolding, unconditional generation, binder design, symmetric oligomers, FrameFlow, Chroma, Genie, ProteinGenerator. Triggers on RFdiffusion, RFdiffusion-AA, de novo design, protein backbone generation, scaffold design, FrameFlow, Chroma."
category: scientific-writing
tags: [rfdiffusion, protein-design, diffusion, de-novo]
---

# RFdiffusion & Modern Protein Backbone Design

## Purpose
Generate novel protein backbones — de novo scaffolds, binders to target, symmetric oligomers, motif grafts. Baker lab pipeline: backbone (RFdiffusion) → sequence (ProteinMPNN) → structure validation (AF2/Boltz).

## Models (2023-2025)

| Model | Purpose | Released | License |
|-------|---------|----------|---------|
| **RFdiffusion** | Backbone diffusion (residue frames) | 2023 | OSS |
| **RFdiffusion-All-Atom** | + side chains + ligand constraints | 2024 | OSS |
| **FrameFlow** | Flow-matching alternative | 2023 | OSS |
| **Chroma** | Generative (Generate Biomedicines) | 2023 | OSS |
| **Genie** / **Genie 2** | Generative | 2023-2024 | OSS |
| **FoldingDiff** | Inner-coord diffusion | 2022 | OSS |
| **ProteinSGM** | Score-based | 2022 | OSS |

## Install RFdiffusion
```bash
git clone https://github.com/RosettaCommons/RFdiffusion
cd RFdiffusion && pip install -e .
# Download model weights (~5 GB)
./scripts/download_models.sh
```

Requires CUDA. ~16 GB VRAM typical.

## Use cases

### 1. Unconditional generation
```bash
./scripts/run_inference.py \
  'contigmap.contigs=[100-100]' \
  inference.num_designs=10 \
  inference.output_prefix=outputs/unconditional/uncond
```
Generates 100-AA backbone ×10 designs.

### 2. Motif scaffolding (graft functional motif)
```bash
./scripts/run_inference.py \
  'contigmap.contigs=[5-15/A25-40/5-15]' \
  inference.input_pdb=motif.pdb \
  inference.num_designs=20 \
  inference.output_prefix=outputs/motif/scaffold
```
Contigmap syntax:
- `[10-20/A25-40/10-20]` = 10-20 residues loop, then A25-40 from input, then 10-20 loop
- `[100-100:A]` = reconstruct chain A as 100 residues

### 3. Binder design
```bash
./scripts/run_inference.py \
  'contigmap.contigs=[A1-150/0 B60-90]' \
  inference.input_pdb=target.pdb \
  'ppi.hotspot_res=[A56,A115,A129]' \
  inference.num_designs=100 \
  inference.output_prefix=outputs/binder/bind
```
Designs 60-90 AA binder against hotspot residues on target.

### 4. Symmetric oligomers
```bash
./scripts/run_inference.py \
  'contigmap.contigs=[60-60]' \
  inference.symmetry=C3 \
  inference.num_designs=10
```
Generates C3-symmetric trimer.

## RFdiffusion-AA (2024)
Adds: ligand context, metal binding sites, membrane constraints.

```bash
./scripts/run_inference.py \
  --config-name aa \
  ligand_ccd=HEM \            # heme
  inference.input_pdb=site.pdb \
  inference.num_designs=50
```

## Output
PDB files with per-residue plddt-like confidence. Backbone only (Cα/N/C/O); side chains = Gly/Ala placeholders.

## Canonical pipeline

```
  Target / Motif
       │
       ▼
1. RFdiffusion (backbone)
       │  → N backbone scaffolds
       ▼
2. ProteinMPNN (sequence design)
       │  → M sequences per backbone
       ▼
3. AF2 / Boltz / ESMFold (validation)
       │  → filter by pLDDT > 80, RMSD < 2 Å
       ▼
4. Rosetta FastRelax / FoldX (stability)
       │  → ddG filter
       ▼
5. Expression + experimental testing
```

Filters applied typical:
- Backbone secondary structure diversity
- pLDDT ≥ 80 (AF2 re-fold)
- RMSD ≤ 2 Å between RFdiffusion scaffold and AF2 refold
- Rosetta energy / SAP / developability

## FrameFlow (alternative, faster)
- Flow-matching (not score-based)
- 3-5× faster than RFdiffusion
- Similar quality on standard benchmarks

## Chroma (Generate Biomedicines, 2023)
- Backbone + sequence in one model
- Conditional on programmable constraints
- Public API + weights

## Genie 2 (2024)
- Multi-chain, multi-motif
- Better on unconditional benchmarks than RFdiffusion

## Failure modes
- Unrealistic backbones (geometric checks fail) — filter
- Scaffolds that don't fold in AF2 (disagreement) — common, run large batch
- Over-designed interfaces (too many H-bonds) — check SAP score
- Short loops forced through tight spaces — adjust contigmap ranges

## Citation
- Watson et al. — RFdiffusion (Nature 2023)
- Krishna et al. — RFdiffusion-AA (Science 2024)
- Yim et al. — FrameFlow (NeurIPS 2023)
- Ingraham et al. — Chroma (Nature 2023)
- Lin et al. — Genie (ICML 2023) / Genie 2 (2024)

## Related skills
- `proteinmpnn-suite` — sequence design on RF scaffolds
- `alphafold-suite`, `boltz-structure-prediction` — validate designs
- `foldx-rosetta-stability` — ddG filtering
- `free-energy-calculations` — binder affinity post-design

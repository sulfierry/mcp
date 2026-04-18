---
name: alphafold-suite
description: "AlphaFold 2/3, AlphaFold-Multimer, ColabFold, OpenFold, AlphaFlow, AlphaMissense, AlphaPulldown. Running predictions (local, ColabFold, AF3 server), MSA strategies, template handling, confidence metrics (pLDDT/PAE/pTM/ipTM), ensemble workflows. Triggers on AlphaFold, AF2, AF3, AlphaFold-Multimer, ColabFold, OpenFold, AlphaMissense."
category: scientific-writing
tags: [alphafold, af2, af3, colabfold, structure-prediction, deepmind]
---

# AlphaFold Suite

## Model zoo (2021-2025)

| Model | Released | Purpose | Access |
|-------|----------|---------|--------|
| **AF2** | 2021 | Monomer structure | Free, local/Colab/server |
| **AF2-Multimer** | 2022 | Protein complexes (prot-prot) | Free, local |
| **AF3** | 2024 (Nature) | Protein + NA + ligand + PTM | AlphaFold server (academic free, no install) |
| **AlphaFold 3.0.1 OSS** | 2024 (Nov) | AF3 weights for academic use | Non-commercial |
| **ColabFold** | 2022+ | Fast AF2/3 via MMseqs2 MSA | Free, Colab or local |
| **OpenFold** | 2022+ | AF2-compatible PyTorch reimpl | Apache-2.0 |
| **OpenFold3** | 2025 | OSS AF3 reimplementation | Apache-2.0 |
| **AlphaFlow** | 2024 | Conformational ensemble (AF + diffusion) | OSS |
| **AlphaMissense** | 2023 | Missense variant pathogenicity | Free catalogue + per-request |
| **AlphaPulldown** | 2023 | High-throughput screening | OSS wrapper |

## When to use which

| Task | Tool |
|------|------|
| Single-chain structure | AF2 or ColabFold |
| Protein-protein complex | AF2-Multimer or AF3/Boltz/Chai |
| Protein-ligand / NA / PTM | AF3, Boltz-2, Chai-1 |
| Fast screening (hundreds of seqs) | ColabFold + MMseqs2 |
| Conformational ensemble | AlphaFlow or AF-Cluster |
| Mutation pathogenicity | AlphaMissense |
| Batch protein-protein screen | AlphaPulldown |
| Fully open-source AF3-class | Boltz / Chai / OpenFold3 |

## Install: local AF2 / OpenFold

```bash
# OpenFold (Apache-2.0, cleaner install)
git clone https://github.com/aqlaboratory/openfold
cd openfold && uv pip install -e .

# ColabFold CLI
uv pip install "colabfold[alphafold-minus-jax]"
pip install --upgrade "jax[cuda12_pip]"  # GPU
```

## ColabFold CLI (fastest path)

```bash
colabfold_batch input.fasta output/ \
  --model-type alphafold2_multimer_v3 \
  --num-recycle 3 \
  --num-models 5 \
  --rank iptm \
  --amber                    # Amber relaxation
```

Input FASTA for multimer (join chains with `:`):
```
>complex
MENFKV...:GSSHHHH...
```

## AF3 server workflow (no install)

- `alphafoldserver.com` (academic, free)
- Upload sequence + ligand SMILES / CCD codes / NA / modified residues
- Rate limit: 10 jobs/day per academic user
- Downloads: `.cif` + confidence JSON

No local install needed; downside: limited throughput.

## MSA strategies

| Strategy | Tool | Speed | Accuracy |
|----------|------|-------|----------|
| Full AF2 databases (BFD, UniRef90, MGnify) | native AF2 | slow (hours) | best |
| MMseqs2 clusters (ColabFold) | ColabFold | fast (min) | near-full |
| Single-sequence (no MSA) | --msa-mode single_sequence | instant | poor |
| Paired MSA (multimer) | colabfold pair-mode | med | better for complexes |
| Custom MSA | --custom-msa | variable | if you have orphan |

Shallow MSA → AF-Cluster / AlphaFlow for conformational diversity.

## Confidence metrics

- **pLDDT** (0-100): per-residue local confidence; >90 = high, 70-90 = ok, <70 = low.
- **pTM** (0-1): global fold confidence.
- **ipTM** (0-1): inter-chain confidence (multimer); >0.8 = reliable complex.
- **PAE** (Å): pairwise aligned error matrix — use for domain decomposition.
- **mean pLDDT > 90 AND ipTM > 0.8** = submit-quality complex.

Plot PAE as heatmap; block structure reveals domain organization.

## Outputs (AF2/ColabFold)

```
output/
├── <job>_unrelaxed_rank_00x_*.pdb
├── <job>_relaxed_rank_00x_*.pdb          # Amber relaxation
├── <job>_scores_rank_00x_*.json          # pLDDT, pTM, ipTM
├── <job>_coverage.png                    # MSA depth per residue
├── <job>_plddt.png
└── <job>_PAE.png
```

AF3 `.cif` + JSON confidence.

## AlphaFlow (conformational ensembles)

Diffusion-based ensemble sampling conditioned on AF2 structure:
```bash
git clone https://github.com/bjing2016/alphaflow
# Generate 100 conformers
python predict.py --pdb target.pdb --num_samples 100
```

Useful for kinase DFG-in/out, GPCR inactive/active, IDR ensemble.

## AlphaMissense (variant effect)

Pre-computed catalogue for human proteome:
- `alphafold.com/alphamissense` — download per-gene CSV
- API for on-demand non-human predictions

Score 0-1: pathogenicity likelihood.

## AlphaPulldown (HTP screening)

```bash
pip install alphapulldown
# Screen 1 bait vs 1000 preys for interaction
alphapulldown.run_multimer_jobs.py --mode all_vs_all ...
```

Ranks complexes by ipTM; triage for wet-lab validation.

## Integration

- **Docking prep**: AF2 → openbabel conversion → AutoDock/DiffDock-L
- **MD input**: relaxed PDB → openMM / GROMACS topology
- **Redesign**: AF2 scaffold → RFdiffusion → ProteinMPNN → AF2 validate
- **FEP prep**: AF2 receptor → Maestro / flare for FEP+

## Failure modes

- Orphan protein (no MSA) → low pLDDT throughout; try ESMFold (PLM-only)
- Large multimer (>2000 total AA) → memory issues; split or use AF2-Multimer batching
- Disordered regions → correctly flagged as low pLDDT (not a bug)
- Membrane protein without lipid bilayer → relaxation may distort; use Amber cutoff carefully

## Citation

- Jumper et al. — AlphaFold 2 (Nature 2021)
- Evans et al. — AF2-Multimer (bioRxiv 2022)
- Abramson et al. — AlphaFold 3 (Nature 2024)
- Mirdita et al. — ColabFold (Nat Methods 2022)
- Ahdritz et al. — OpenFold (Nat Methods 2024)
- Jing et al. — AlphaFlow (ICML 2024)
- Cheng et al. — AlphaMissense (Science 2023)

## Related

- `boltz-structure-prediction`, `chai-1-rosettafold` — AF3-class OSS alternatives
- `rfdiffusion-design`, `proteinmpnn-suite` — de novo design using AF-scaffolds
- `protein-language-models` — ESMFold comparison (faster, less accurate than AF2)
- `modern-ai-docking` — DiffDock-L uses AF-predicted receptors
- `free-energy-calculations` — FEP on AF2-refined structures

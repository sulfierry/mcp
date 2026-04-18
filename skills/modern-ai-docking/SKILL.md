---
name: modern-ai-docking
description: "AI-era molecular docking: DiffDock-L, Gnina, Uni-Mol Docking, UMol, NeuralPLexer. Plus GPU-accelerated classical: Vina-GPU, AutoDock-GPU, Smina. Virtual screening with deep-learning rescorers. Triggers on DiffDock, Gnina, Uni-Mol docking, UMol, NeuralPLexer, AI docking, GPU docking, deep learning docking."
category: scientific-writing
tags: [docking, diffdock, gnina, uni-mol, umol, virtual-screening, ai-docking]
---

# Modern AI Docking

## Model landscape (2023-2025)

| Tool | Approach | Year | License |
|------|----------|------|---------|
| **DiffDock-L** | Diffusion (score-based) | 2023 | MIT |
| **Gnina** | CNN rescorer on Vina poses | 2019+ | GPLv2 |
| **Uni-Mol Docking** | 3D transformer | 2023 | MIT |
| **UMol** | Unified pose + affinity | 2024 | academic |
| **NeuralPLexer** | Cofactor-aware co-folding | 2023 | MIT |
| **RosettaFoldAllAtom (RFAA)** | AF-era with ligand | 2024 | academic |
| **EquiBind** | Fast direct prediction | 2022 | MIT |
| **TankBind** | Trigonometry-aware | 2022 | MIT |
| **PoseBusters** | Validation (not docker) | 2023 | BSD |

Classical (GPU-accelerated):
- **AutoDock-GPU** — CUDA/OpenCL port of AutoDock4
- **Vina-GPU 2.0** — CUDA port of AutoDock Vina
- **Smina** — fork of Vina with optimized scoring
- **Gnina** — Smina + CNN rescorer (best balance of speed + accuracy)

## When to use which

| Scenario | Tool |
|----------|------|
| Fast screening 100k+ ligands | Vina-GPU + Gnina rescore |
| Top hits refinement (≤100 ligands) | DiffDock-L + Gnina + MD minimization |
| Structure-aware with confidence | Uni-Mol Docking, DiffDock-L |
| Blind pocket | DiffDock-L (no pocket spec) |
| Cofactor/metal-containing site | NeuralPLexer or RFAA |
| Need affinity too | UMol or FEP post-docking |
| Baseline / validation | AutoDock Vina 1.2 |

## DiffDock-L install + use

```bash
git clone https://github.com/gcorso/DiffDock
cd DiffDock && pip install -e .
```

Inference (blind):
```bash
python -m inference \
  --protein_path receptor.pdb \
  --ligand ligand.sdf \
  --out_dir predictions/ \
  --inference_steps 20 \
  --samples_per_complex 40 \
  --actual_steps 18 \
  --no_final_step_noise
```

- `samples_per_complex 40`: more = better but slower
- Output: N poses ranked by confidence
- Typical runtime: 2-10s per complex (H100)

## Gnina

```bash
# Install
wget https://github.com/gnina/gnina/releases/latest/download/gnina
chmod +x gnina
# Dock
./gnina -r receptor.pdbqt -l ligands.sdf -o out.sdf \
  --autobox_ligand ref.sdf --cnn_scoring refinement \
  --cpu 0  # GPU index or --cpu -1 for CPU
```

CNN scoring modes:
- `rescore`: Vina dock → CNN rescore (fast)
- `refinement`: CNN-guided local optimization (best accuracy)
- `metrics`: just score existing poses

## Uni-Mol Docking

```bash
pip install unimol-tools
```
```python
from unimol_tools import UniMolDock
dock = UniMolDock()
poses = dock.run(receptor_pdb='receptor.pdb',
                 ligand_sdf='ligand.sdf',
                 pocket_center=(x, y, z),
                 pocket_size=(20, 20, 20))
```

## UMol (2024)

Single-pass: structure + affinity.
```bash
git clone https://github.com/patrickbryant1/Umol
# Input: sequence + SMILES
python predict.py --sequence "MKVFLKQ..." --smiles "CC(=O)..."
```

## NeuralPLexer

Cofactor-aware (heme, metal clusters, NAD, etc.):
```bash
git clone https://github.com/zrqiao/NeuralPLexer
python neuralplexer_main.py \
  --task=single_sample_trajectory \
  --sample-id=test1 \
  --input-receptor receptor.pdb \
  --input-ligand ligand.sdf
```

## Pose validation (PoseBusters)

```bash
pip install posebusters
```
```python
from posebusters import PoseBusters
buster = PoseBusters(config='redock')
results = buster.bust(mol=predicted_mol,
                      mol_cond=crystal_mol,
                      mol_pred_path='pred.sdf')
# Checks: clash, strain, hydrogen bonds, volume, bond lengths
```

Always validate DiffDock/Uni-Mol outputs through PoseBusters. Diffusion models can produce geometrically inconsistent poses.

## Virtual screening pipeline

```
1. Library prep (RDKit / Meeko):
   SMILES → 3D conformer → PDBQT (for Vina) or SDF (for DiffDock)
2. Pocket detection (if unknown):
   fpocket / PASS / DoGSiteScorer, or trust AF-predicted pocket
3. Initial dock:
   Vina-GPU or AutoDock-GPU (millions/day on A100)
4. Rescore top 1-10%:
   Gnina CNN rescoring
5. Final refinement (top 100-1000):
   DiffDock-L or Uni-Mol Docking
6. Validation:
   PoseBusters + MD short run (10 ns)
7. Affinity estimate:
   FEP+ or MM/GBSA on top 10-50
```

## Performance benchmarks

| Tool | Top-1 RMSD ≤ 2 Å (PoseBusters) |
|------|-------------------------------|
| AutoDock Vina | ~35% |
| Gnina (CNN-rescore) | ~50% |
| DiffDock | ~38% (PoseBusters strict) |
| DiffDock-L | ~54% |
| Uni-Mol Docking | ~56% |
| UMol | ~52% |

Note: DL methods **sometimes produce geometrically invalid poses** — always use PoseBusters.

## Common pitfalls

- **Hydrogens**: ensure protonation matches pH; use PROPKA
- **Protein preparation**: remove HETATMs you don't want (or keep explicitly)
- **Tautomers**: canonicalize ligand with RDKit or MolStandardize
- **Pocket definition**: wrong pocket center → wrong poses (Vina/AutoDock)
- **Covalent ligands**: most ML dockers don't handle; use Rosetta or AutoDock covalent
- **Large macrocycles/peptides**: AF3/Boltz better than docking
- **Metal coordination**: use NeuralPLexer or RFAA

## Integration

- **Upstream**: AF2/Boltz/Chai receptor → prep with PDBFixer → dock
- **Downstream**: MD relaxation → FEP on top 10 → experimental synthesis
- **Complement**: consensus across tools (DiffDock + Gnina + Uni-Mol agreement = high confidence)

## Meeko (ligand prep)

```bash
pip install meeko
```
```python
from meeko import MoleculePreparation, PDBQTWriterLegacy
from rdkit import Chem
mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
mol = Chem.AddHs(mol)
Chem.AllChem.EmbedMolecule(mol)
prep = MoleculePreparation()
prep.prepare(mol)
pdbqt = PDBQTWriterLegacy.write_string(prep.setup)
```

## Citation

- Corso et al. — DiffDock (ICLR 2023); DiffDock-L (ICLR 2024)
- McNutt et al. — Gnina (J Cheminform 2021)
- Zhou et al. — Uni-Mol / Uni-Mol Docking (ICLR 2023)
- Bryant et al. — UMol (Nat Comm 2024)
- Qiao et al. — NeuralPLexer (Nat Mach Intell 2024)
- Buttenschoen et al. — PoseBusters (Chem Sci 2024)

## Related

- `boltz-structure-prediction`, `alphafold-suite` — receptor prep
- `openmm-modern-md` — post-dock relaxation
- `free-energy-calculations` — ΔG on top hits
- `molecular-language-models` — ligand embeddings for VS
- `rdkit`, `datamol`, `meeko` (existing) — prep

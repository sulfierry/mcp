---
name: free-energy-calculations
description: "Alchemical free-energy methods for binding affinity (ΔG). FEP (Free Energy Perturbation), TI (Thermodynamic Integration), ABFE (Absolute Binding Free Energy), RBFE (Relative Binding Free Energy), MBAR/BAR analysis. Tools: FEP+ (Schrödinger), BFEE2, OpenMM+openmmtools+openfe, YANK, Amber TI, GROMACS pmx. OpenFF Sage ligand params. Triggers on FEP, free energy, alchemical, ABFE, RBFE, binding affinity, thermodynamic integration, MBAR, BAR."
category: scientific-writing
tags: [fep, free-energy, abfe, rbfe, alchemical, binding-affinity]
---

# Alchemical Free-Energy Calculations

## Methods

| Method | Question | Speed | Accuracy |
|--------|----------|-------|----------|
| **RBFE** (Relative) | ΔΔG (A→B) between congeners | faster (5-20 h) | < 1 kcal/mol RMSE |
| **ABFE** (Absolute) | ΔG of binding (ligand ↔ solvent) | slower (20-100 h) | 1-2 kcal/mol RMSE |
| **FEP** | λ-perturbation, multi-intermediate | both RBFE/ABFE | gold standard |
| **TI** | Gradient integration | similar to FEP | sensitive to windows |
| **MBAR** | Analysis: combine all λ data | post-hoc | lowest variance |
| **BAR** | Pair-wise analysis | post-hoc | older standard |

## When to use each

- **Lead optimization** (ranking close analogs): RBFE with FEP+ / openfe
- **Hit validation** (is binding real?): ABFE
- **Pocket specificity**: mutate residue → RBFE
- **Bind or not to target B** (vs A): ABFE on both + compare

## Tool landscape

| Tool | License | Engine |
|------|---------|--------|
| **FEP+** (Schrödinger) | Commercial | Desmond |
| **OpenFE (Open Free Energy)** | MIT | OpenMM |
| **BFEE2** | Open | NAMD |
| **YANK** | OSS | OpenMM (legacy) |
| **AMBER TI/FEP** | Commercial | pmemd |
| **GROMACS + pmx** | OSS | GROMACS |
| **Pymbar** | OSS | analysis-only (MBAR) |
| **Alchemistry scripts** | OSS | various |

Recommended OSS stack: **OpenFE + OpenMM + openff-toolkit + OpenFF Sage 2.2**.

## OpenFE workflow (RBFE)

```bash
pip install openfe
```

```python
import openfe
from openfe import SmallMoleculeComponent, ProteinComponent, SolventComponent
from openfe.protocols import openmm_rfe

# Load
receptor = ProteinComponent.from_pdb_file('receptor.pdb')
ligA = SmallMoleculeComponent.from_sdf_file('ligA.sdf')
ligB = SmallMoleculeComponent.from_sdf_file('ligB.sdf')

# Set up state: A and B
stateA = openfe.ChemicalSystem({'protein': receptor,
                                 'ligand': ligA,
                                 'solvent': SolventComponent()})
stateB = openfe.ChemicalSystem({'protein': receptor,
                                 'ligand': ligB,
                                 'solvent': SolventComponent()})

# Mapping
mapper = openfe.setup.LomapAtomMapper()
mapping = next(mapper.suggest_mappings(ligA, ligB))

# Protocol
settings = openmm_rfe.RelativeHybridTopologyProtocol.default_settings()
settings.simulation_settings.equilibration_length = 1.0 * unit.nanosecond
settings.simulation_settings.production_length = 5.0 * unit.nanosecond
protocol = openmm_rfe.RelativeHybridTopologyProtocol(settings)

# Run
transformation = openfe.Transformation(stateA, stateB, protocol, mapping)
result = transformation.create().execute()
print(f'ΔΔG = {result.get_estimate()} ± {result.get_uncertainty()}')
```

## Alchemical perturbation

- N lambda windows (11-21 typical)
- Soft-core potential for ligand decoupling
- Each λ: equilibrate 1 ns + production 5 ns → 20 × 6 = 120 ns total simulation per edge
- Multiple starting seeds (3-5) for error estimation

## Sanity checks / protocol hygiene

- **Cycle closure**: for edges A→B, B→C, C→A, sum ΔΔG should be 0 ± error
- **Convergence**: block averaging; check no drift in dG/dλ
- **Overlap** between adjacent λ windows (>20% ideal)
- **Replicate runs** (≥3 seeds per edge)
- **Benchmark**: reproduce experimental ΔΔG on congener series with known values first

## Benchmarks (ask before buying)

- **Schrödinger JACS series** (17 ligands × 8 targets): FEP+ RMSE ~1.1 kcal/mol
- **Merck/Abbott series**: similar
- **OpenFE matches** (OpenFF Sage 2.2): within 0.2 kcal of FEP+ on same benchmarks

## ABFE (absolute) with openfe

```python
from openfe.protocols import openmm_abfe
protocol = openmm_abfe.AbsoluteFreeEnergyProtocol(settings)
# stateA = system with ligand bound
# stateB = system without ligand (or ligand in bulk solvent)
```

Requires restraint (Boresch-style) on ligand to keep in pocket during decoupling. Restraint correction (~5-10 kcal/mol) must be computed analytically.

## Key gotchas

- Charged perturbations (net charge change) → need ion pair compensation or slow-growth
- Buried waters → W-MD or GCMC pre-equilibration
- Protonation changes → run separately per protonation state
- Ring opening/closing → often fails; use single-topology with care
- Ligand flexibility → longer equilibration, more sampling
- Pocket dynamics → MD of apo first; ensemble docking + FEP

## Integration

- **Input**: AF2/Boltz structure + MD-relaxed → FEP
- **Ligand**: OpenFF Sage 2.2 or GAFF2 (with AM1-BCC charges)
- **Protein**: ff14SB/ff19SB (AMBER) or CHARMM36m
- **Output**: ranked potency → experimental synthesis

## Timing (A100 GPU)

| Calc | Time |
|------|------|
| RBFE single edge | 3-6 h |
| ABFE single ligand | 15-40 h |
| Benchmark series (15 ligs) | 2-5 days parallel |

## References

- Wang et al. — FEP+ JACS benchmark (JACS 2015)
- Mey et al. — Best Practices for Alchemical FE (LiveCoMS 2020)
- Gapsys et al. — pmx automated RBFE (Chem Sci 2020)
- OpenFE docs: docs.openfree.energy
- Mobley & Gilson — *Annu Rev Biophys* (2017) — theoretical foundations

## Related

- `openmm-modern-md` — underlying MD engine
- `alphafold-suite`, `boltz-structure-prediction` — input structures
- `modern-ai-docking` — poses as starting points
- `foldx-rosetta-stability` — ΔΔG of mutations (complementary method)

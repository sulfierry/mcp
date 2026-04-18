---
name: openmm-modern-md
description: "Modern molecular dynamics with OpenMM, GROMACS, AMBER, NAMD. Force fields (AMBER ff14SB/ff19SB, CHARMM36m, OpenFF Sage), water models (TIP3P/TIP4P/OPC), solvation, equilibration protocols, production MD, enhanced sampling (metadynamics, REMD, GaMD), trajectory analysis with MDAnalysis. GPU acceleration. Triggers on molecular dynamics, MD, OpenMM, GROMACS, AMBER, NAMD, force field, CHARMM, metadynamics."
category: scientific-writing
tags: [molecular-dynamics, openmm, gromacs, amber, md, force-field]
---

# Modern Molecular Dynamics

## Engines (2024-2025)

| Engine | Strengths | License |
|--------|-----------|---------|
| **OpenMM** | Python-first, GPU, CUDA/Metal/OpenCL, extensible | MIT |
| **GROMACS** | Fastest CPU, mature, production scale | LGPL |
| **AMBER** (pmemd.cuda) | Strongest GPU for membrane, large systems | Commercial (pmemd free for academic) |
| **NAMD** | Scales to 100k cores | Free academic |
| **Desmond** (Schrödinger) | Industry FEP+ gold standard | Commercial |
| **HOOMD-blue** | Coarse-grain, soft matter | BSD |

Recommended starter: **OpenMM** (scriptable + PDBFixer + OpenFF integration).

## Force fields (2025 state of the art)

| FF | Atoms | Proteins | NA | Ligand |
|----|-------|----------|----|---------|
| **AMBER ff19SB** | atomistic | ✅ (improved backbone) | pair with OL21 / OL15 | GAFF2 or OpenFF |
| **CHARMM36m** | atomistic | ✅ IDP-friendly | ✅ | CGenFF |
| **OPLS-AA/M** | atomistic | ✅ | — | custom |
| **Martini 3** | coarse-grain | ✅ 4:1 mapping | ✅ | bead mapping |

Water: **OPC** (AMBER) or TIP3P (CHARMM36m) or TIP4P/Ew.

Ligand: **OpenFF Sage 2.2+** (SMIRNOFF) — state of art for small mol; replaces GAFF2 for many applications. Via OpenForceFields toolkit.

## Install OpenMM + ecosystem

```bash
mamba create -n md -c conda-forge openmm pdbfixer mdanalysis openff-toolkit \
  openmmforcefields ambertools
conda activate md
```

GPU detection:
```python
from openmm import Platform
Platform.getPlatformByName('CUDA')   # or 'OpenCL', 'Metal' (M-series Mac)
```

## Minimal protein-ligand MD in OpenMM

```python
from openmm.app import PDBFile, ForceField, Modeller, Simulation, StateDataReporter
from openmm import unit, LangevinMiddleIntegrator
from openmmforcefields.generators import SMIRNOFFTemplateGenerator
from openff.toolkit import Molecule

# 1. Load protein
pdb = PDBFile('receptor_ligand.pdb')

# 2. OpenFF for ligand
ligand = Molecule.from_file('ligand.sdf')
smirnoff = SMIRNOFFTemplateGenerator(molecules=[ligand],
                                      forcefield='openff-2.2.0')

# 3. Combined force field
ff = ForceField('amber14-all.xml', 'amber14/tip3p.xml')
ff.registerTemplateGenerator(smirnoff.generator)

# 4. Solvate + neutralize
modeller = Modeller(pdb.topology, pdb.positions)
modeller.addSolvent(ff, padding=1.0*unit.nanometer, ionicStrength=0.15*unit.molar)

# 5. System
system = ff.createSystem(modeller.topology,
                         nonbondedMethod=app.PME,
                         nonbondedCutoff=1.0*unit.nanometer,
                         constraints=app.HBonds)

# 6. Integrator + platform
integrator = LangevinMiddleIntegrator(300*unit.kelvin,
                                       1.0/unit.picosecond,
                                       2.0*unit.femtosecond)
platform = Platform.getPlatformByName('CUDA')
sim = Simulation(modeller.topology, system, integrator, platform)
sim.context.setPositions(modeller.positions)

# 7. Minimize + equilibrate
sim.minimizeEnergy()
sim.context.setVelocitiesToTemperature(300*unit.kelvin)
sim.step(50000)  # 100 ps equilibration

# 8. Production (with trajectory)
sim.reporters.append(app.DCDReporter('traj.dcd', 1000))
sim.reporters.append(StateDataReporter('log.csv', 1000,
    step=True, time=True, potentialEnergy=True, temperature=True))
sim.step(50_000_000)  # 100 ns at 2 fs step
```

## Standard protocol

1. **Prep**: PDBFixer (add missing atoms, remove crystal waters)
2. **Protonation**: PROPKA or H++ at pH 7.4
3. **Parametrize ligand**: OpenFF Sage (preferred) or GAFF2
4. **Solvate**: octahedral box, ≥10 Å padding
5. **Neutralize**: 0.15 M NaCl
6. **Minimize**: steepest descent 5000 steps
7. **Heat**: 0 → 300 K over 100 ps with positional restraints (heavy atoms)
8. **Equilibrate NVT** (100 ps) → **NPT** (500 ps-1 ns), gradually release restraints
9. **Production**: 100 ns - 1 µs NPT, no restraints
10. **Analyze**: MDAnalysis / PyTraj / MDTraj

## Enhanced sampling

| Method | Tool | Use case |
|--------|------|----------|
| Metadynamics | PLUMED + OpenMM/GROMACS | Free-energy landscape of CV |
| REMD | GROMACS/AMBER | Folding, rare states |
| GaMD (Gaussian accelerated) | AMBER | Ligand binding/unbinding |
| aMD | AMBER | Conformational sampling |
| umbrella sampling | PLUMED | PMF along path |
| WExplore / WESTPA | Weighted ensemble | Rare events |
| SMD (steered) | OpenMM/GROMACS | Pulling experiments |

PLUMED (tools.plumed.org) is FF-agnostic, supports all major engines.

## Trajectory analysis

```python
import mdanalysis as mda
u = mda.Universe('topology.pdb', 'traj.dcd')
# RMSD
from mdanalysis.analysis.rms import RMSD
rmsd = RMSD(u, u, select="protein and name CA").run()
# Pocket volume
# PyMOL, MDpocket, fpocket
# Secondary structure
# mdtraj.compute_dssp
```

Standard metrics: RMSD, RMSF, Rg, SASA, H-bonds, contact maps, clustering (gromos or k-means on RMSD).

## Timing (single H100 GPU)

| System size | Performance |
|-------------|-------------|
| 50k atoms (small protein + solvent) | 200-400 ns/day |
| 200k atoms (membrane protein) | 50-100 ns/day |
| 1M atoms (assembly) | 5-20 ns/day |

## Common pitfalls

- Ligand parametrization errors → explicit charges from AM1-BCC or RESP
- PBC artifacts → check box size, wrap trajectories
- Protonation states for buried residues → pKa calculation (PROPKA/H++)
- Missing loops/residues → fill with Modeller/Alphafold before MD
- Starting from poor AF2 → run short MD to relax (100 ps restrained)
- Not validating convergence → replicate runs (≥3), block averaging

## Integration

- AF2/Boltz → relax PDB → MD
- MD → cluster snapshots → docking against each
- FEP uses OpenMM under hood (FEP+, BFEE2, absolute binding via ABFE)

## Citation

- Eastman et al. — OpenMM (PLOS Comp Biol 2017)
- Abraham et al. — GROMACS (SoftwareX 2015)
- Case et al. — AMBER (J Chem Inf Model 2023)
- Tian et al. — ff19SB (JCTC 2020)
- Smith et al. — OpenFF Sage (JACS 2024)

## Related
- `free-energy-calculations` — FEP/ABFE on MD trajectories
- `alphafold-suite`, `boltz-structure-prediction` — upstream structures
- `modern-ai-docking` — docked poses refine with MD
- `mdanalysis-trajectory` (already in catalog) — deep analysis

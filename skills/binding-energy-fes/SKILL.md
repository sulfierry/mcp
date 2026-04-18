---
name: binding-energy-fes
description: "Binding energy calculations and free-energy landscapes (FES). Endpoint methods (MM/GBSA, MM/PBSA, LIE), enhanced sampling for PMF (metadynamics, umbrella sampling, REMD, ABMD, adaptive biasing force), FES reconstruction (WHAM, BAR, MBAR), collective variables (RMSD, distance, torsion, path-CV, CVAE-learned CVs), PLUMED. Triggers on binding energy, MM/GBSA, MM/PBSA, metadynamics, free energy landscape, PMF, umbrella sampling, FES, WHAM, PLUMED, REMD."
category: scientific-writing
tags: [binding-energy, fes, metadynamics, umbrella-sampling, mmgbsa, pmf, plumed]
---

# Binding Energy & Free Energy Landscapes

## Two complementary questions
1. **Binding energy** (single number): ΔG of bound vs unbound → affinity
2. **Free-energy landscape (FES)**: ΔG along reaction coordinate(s) → mechanism, pathways, barriers

## Binding energy methods

| Method | Speed | Accuracy | Use case |
|--------|-------|----------|----------|
| **MM/GBSA** | fast (~100 frames, min) | semi-quant ranking | Hit ranking, congener series |
| **MM/PBSA** | slower (PB solver) | similar to GBSA | More rigorous implicit solvent |
| **LIE** (Linear Interaction Energy) | fast | empirical fit | Needs training set |
| **ABFE (alchemical)** | 20-100 h/ligand | < 2 kcal/mol RMSE | Gold standard — see `free-energy-calculations` |
| **RBFE (FEP+)** | 3-6 h/edge | < 1 kcal/mol | Congener comparison |
| **SMD / steered MD** | slow | qualitative | Dissociation pathway |

### MM/GBSA protocol (AMBER / OpenMM)

```bash
# AMBER
mm_pbsa.py -i mmgbsa.in -o result.dat \
  -cp complex.prmtop -rp receptor.prmtop -lp ligand.prmtop \
  -y trajectory.nc
```

Input file (simplified):
```
&general
  startframe=100, endframe=500, interval=5, verbose=1
/
&gb
  igb=5, saltcon=0.150
/
```

Outputs ΔG_bind = ΔE_internal + ΔE_vdW + ΔE_elec + ΔG_pol + ΔG_np − TΔS.

- Usually drop −TΔS (entropy) for ranking — reduces noise
- Per-residue decomposition → identify hot spots

### MM/PBSA (slower, uses Poisson-Boltzmann)

Same tool, `ipb=2` (numerical PB). More rigorous for highly charged systems.

### OpenMM MM/GBSA alternative (gmxmmpbsa)
```bash
gmx_MMPBSA -i mmgbsa.in -cp complex.prmtop -ci index.ndx \
  -cg 0 1 -ct trajectory.xtc
```

## Free Energy Landscapes (FES)

Reconstruct ΔG(CV) along one or more collective variables (CVs).

### Collective variables (CVs)

| CV | Use case |
|----|----------|
| RMSD to reference | Folding / unfolding |
| Distance (atom pairs) | Binding, unbinding |
| Angle / dihedral | Conformational change |
| Radius of gyration (Rg) | Compaction |
| Contact map / path-CV | Transition paths |
| Q (native contacts) | Folding |
| CVAE / ML-learned | Rare events via data-driven CV |

### Metadynamics (Laio & Parrinello)

Adds history-dependent Gaussian bias on CV(s) → escape local minima, fill basins.

PLUMED config:
```
# plumed.dat
d: DISTANCE ATOMS=100,500           # CV1: pocket atom ↔ ligand atom
phi: TORSION ATOMS=1,2,3,4          # CV2: key torsion

metad: METAD ARG=d,phi ...
  PACE=500 HEIGHT=1.5 BIASFACTOR=10
  SIGMA=0.1,0.2 GRID_MIN=0.3,-pi GRID_MAX=2.0,pi
  FILE=HILLS

PRINT ARG=d,phi,metad.bias FILE=COLVAR STRIDE=100
```

Run with any MD engine patched with PLUMED (OpenMM/GROMACS/AMBER/NAMD).

### Well-Tempered Metadynamics (recommended)

Biasfactor gradually reduces Gaussian height → smoother convergence. Set `BIASFACTOR=5-15` depending on energy-barrier height.

### Reconstruct FES from HILLS

```bash
plumed sum_hills --hills HILLS --outfile fes.dat \
  --min 0.3,-pi --max 2.0,pi --bin 100,100 --kt 2.5
```

Output: ΔG(CV1, CV2) grid → plot with matplotlib/seaborn contour.

### Umbrella Sampling + WHAM

Alternative: bias each window separately → WHAM reconstruction.

```
# Windows along CV distance d = 0.3 … 2.0 Å, spacing 0.1 Å
for window in windows:
  run MD with harmonic restraint at window center
# Combine with WHAM
wham 0.3 2.0 100 0.001 300 0 metadata.dat fes.dat
```

Standard tools: **wham** (Grossfield), **PyEMMA**, **pymbar**.

### Replica Exchange MD (REMD, REST2, H-REMD)

Multiple temperature replicas (or Hamiltonian scaled) swap periodically. Samples rare states without biasing CVs directly.

GROMACS: `mdrun -multidir -replex 1000` (replex every 1000 steps).

### Adaptive Biasing Force (ABF)

Estimates mean force, accumulates in local histograms. Implementation: **colvars** module (NAMD/GROMACS/LAMMPS/VMD).

```tcl
# colvars.in
colvar {
  name d_bind
  distance {
    group1 { atomNumbers 100 }
    group2 { atomNumbers 500 }
  }
}
abf {
  colvars d_bind
  fullSamples 500
}
```

### Steered MD (SMD)

Pull ligand along coordinate with harmonic spring; reconstruct PMF via **Jarzynski** equality.

## Data-driven CV (ML-learned)

- **CVAE / TAE** (Time-lagged Autoencoder): learn low-dim CV from unbiased MD
- **SGOOP / VAMPnet**: optimize CV by spectral gap
- **SRV (State-free Reversible VAMPnets)**: kinetic CVs
Use when hand-crafted CVs fail to capture transitions.

## Quality control

- **Convergence**: bias height decrease to near-zero (well-tempered); block analysis of FES stable
- **Sampling**: ensure back-and-forth transitions across barriers (count recrossings ≥ 5)
- **Histogram overlap** (umbrella): > 20% between adjacent windows
- **Symmetry check**: if CV symmetric, FES should reflect
- **Error bars**: block averaging or bootstrap 3-5 replicate runs

## Converting FES → binding ΔG

For binding: ΔG_bind = ΔG(d=bound) − ΔG(d=unbound) + standard-state correction

Std-state correction: −kT ln(V_sim / V°) where V° = 1 M = 1660 Å³

Restraint correction if orientational restraints applied (Boresch scheme).

## Tools (integrated)

| Engine + CV | Tool |
|-------------|------|
| OpenMM + PLUMED | openmmtools, openmm-plumed |
| GROMACS + PLUMED | gmx patched with plumed |
| AMBER + PLUMED | pmemd.cuda.mpi + plumed |
| NAMD + colvars | native |
| LAMMPS + colvars | native |

Python post-processing: **PyEMMA** (MSM from trajectories), **MDAnalysis**, **HTMD**.

## Common pitfalls

- **Hysteresis** in metadynamics: bias not converged → one-way FES looks biased; use well-tempered + long run
- **CV choice**: too slow CVs → poor sampling; use committor analysis or VAMP-2 to validate
- **Insufficient sampling of bound state**: pre-equilibrate in bound pose, then bias along unbinding
- **Entropy neglect in MM/GBSA**: provides only enthalpy-ish — can't compare dissimilar binders
- **PB vs GB**: GB faster but less accurate for highly charged; verify on subset with PB
- **Water dynamics**: pocket waters matter (WaterMap / GCMC) — ignoring them biases ΔG

## Timeline (A100 GPU)

| Calc | Time |
|------|------|
| MM/GBSA (100 frames, protein+lig) | 5-30 min |
| MM/PBSA | 30-120 min |
| Well-tempered MetaD (converged FES 2D) | 5-50 ns × replicates = days |
| Umbrella sampling (20 windows × 5 ns) | 1-2 days |
| ABF (full PMF) | 1-3 days |
| SMD + Jarzynski (10-50 runs) | 1-3 days |

## Integration

- **Input structure**: AF2/Boltz + MD relaxation
- **CV selection**: structural analysis + kinetic clustering (MSM)
- **Validation**: FES → FEP on endpoints for cross-check
- **Mechanism**: path-CV from FES → disease-relevant insights for rational design

## Citation

- Laio & Parrinello — Metadynamics (PNAS 2002)
- Barducci et al. — Well-tempered MetaD (PRL 2008)
- Kästner — Umbrella sampling (WIREs CMS 2011)
- Tribello et al. — PLUMED 2 (Comp Phys Comm 2014)
- Gohlke & Case — MM/GBSA (J Comp Chem 2004)
- Kumar et al. — WHAM (J Comp Chem 1992)

## Related

- `free-energy-calculations` — alchemical FEP/ABFE/RBFE (complementary)
- `openmm-modern-md` — underlying MD engine
- `modern-ai-docking` — binding pose input
- `alphafold-suite`, `boltz-structure-prediction` — receptor prep
- `mdanalysis-trajectory` — trajectory post-processing

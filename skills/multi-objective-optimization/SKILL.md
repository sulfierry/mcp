---
name: Multi/Many-Objective Optimization
description: "Multi-objective and many-objective evolutionary optimization. NSGA-II, NSGA-III, MOEA/D, reference point methods, Pareto analysis, quality indicators, and decision making for 2-20+ objectives."
category: optimization
tags: multi-objective, many-objective, nsga-ii, nsga-iii, moead, pareto, optimization, evolutionary, moo
---

# Multi/Many-Objective Optimization

Expert in multi-objective and many-objective optimization — finding optimal trade-off solutions across 2 to 20+ competing objectives simultaneously.

## Use this skill when

- Optimizing 2+ conflicting objectives (cost vs. quality, speed vs. accuracy)
- Finding Pareto-optimal trade-off fronts
- Many-objective problems (4+ objectives) where dominance-based methods fail
- Decomposition-based optimization (MOEA/D, NSGA-III)
- Quality indicator computation (hypervolume, IGD, spread)
- Decision making: selecting a single solution from the Pareto front
- Molecular optimization (drug-likeness vs. activity vs. toxicity vs. synthesizability)
- Engineering design (weight vs. cost vs. strength vs. manufacturability)

## Fundamental Concepts

### Pareto Dominance

```
Solution A dominates B (A ≻ B) iff:
  - A is at least as good as B in ALL objectives
  - A is strictly better in AT LEAST ONE objective

Pareto-optimal set: solutions not dominated by any other
Pareto front: objective values of Pareto-optimal solutions

In many-objective (≥4): dominance becomes useless —
almost all solutions are non-dominated.
→ Need: reference points, decomposition, or indicators
```

### Algorithm Selection

| Objectives | Best Algorithm | Alternative | Key Feature |
|---|---|---|---|
| **2** | NSGA-II | SPEA2 | Crowding distance diversity |
| **3** | NSGA-III | MOEA/D | Reference point association |
| **4-10** | NSGA-III | RVEA, MOEA/D-AWA | Reference directions |
| **10-20+** | MOEA/D | RVEA, θ-DEA | Decomposition scalable |
| **Expensive (any)** | ParEGO | MOEA/D-EGO | Surrogate-assisted |
| **Combinatorial** | NSGA-II + problem-ops | MOEA/D | Custom operators |
| **Dynamic** | DNSGA-II | dCOEA | Change detection |

## Implementation with pymoo

### NSGA-II (2-3 Objectives)

```python
import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Define multi-objective problem
class DrugDesignProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=10,        # decision variables (molecular descriptors)
            n_obj=3,         # objectives
            n_ieq_constr=1,  # inequality constraints
            xl=np.zeros(10), # lower bounds
            xu=np.ones(10),  # upper bounds
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Objective 1: maximize potency (minimize negative)
        f1 = -potency_model(x)
        # Objective 2: minimize toxicity
        f2 = toxicity_model(x)
        # Objective 3: maximize synthesizability (minimize negative)
        f3 = -synth_score(x)

        # Constraint: drug-likeness (Lipinski) must be satisfied
        g1 = lipinski_violations(x) - 1  # g1 <= 0 means feasible

        out["F"] = [f1, f2, f3]
        out["G"] = [g1]

algorithm = NSGA2(
    pop_size=200,
    sampling=FloatRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True,
)

res = minimize(
    DrugDesignProblem(),
    algorithm,
    termination=('n_gen', 500),
    seed=42,
    verbose=True,
)

# Visualize Pareto front
plot = Scatter(title="Drug Design Pareto Front")
plot.add(res.F, facecolor="blue", edgecolor="none", alpha=0.5)
plot.show()
```

### NSGA-III (Many-Objective: 4+ Objectives)

```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.util.ref_dirs import get_reference_directions

# Reference directions for 5 objectives
# Das-Dennis: structured, good for ≤10 objectives
ref_dirs = get_reference_directions("das-dennis", 5, n_partitions=12)
# Energy-based: better for high dimensions
# ref_dirs = get_reference_directions("energy", 5, n_points=200)

algorithm = NSGA3(
    ref_dirs=ref_dirs,
    pop_size=len(ref_dirs),  # typically = number of ref dirs
    crossover=SBX(prob=0.9, eta=30),
    mutation=PM(eta=20),
)

res = minimize(problem, algorithm, termination=('n_gen', 600), seed=42)
print(f"Pareto front size: {len(res.F)}")
```

### MOEA/D (Decomposition-Based)

```python
from pymoo.algorithms.moo.moead import MOEAD

# MOEA/D: decomposes into single-objective subproblems
ref_dirs = get_reference_directions("uniform", 3, n_partitions=30)

algorithm = MOEAD(
    ref_dirs=ref_dirs,
    n_neighbors=20,          # neighborhood size T
    prob_neighbor_mating=0.9, # δ: probability of mating within neighborhood
    decomposition="tchebi",  # Tchebycheff, PBI, or weighted-sum
)

res = minimize(problem, algorithm, termination=('n_gen', 500))
```

## Quality Indicators

```python
from pymoo.indicators.hv import HV
from pymoo.indicators.igd import IGD
from pymoo.indicators.igd_plus import IGDPlus
from pymoo.indicators.spacing import SpacingIndicator

# Hypervolume: LARGER is better (volume dominated by PF)
hv = HV(ref_point=np.array([1.1, 1.1, 1.1]))
print(f"Hypervolume: {hv(res.F):.4f}")

# IGD: SMALLER is better (distance to true PF)
igd = IGD(true_pareto_front)
print(f"IGD: {igd(res.F):.6f}")

# IGD+: Pareto-compliant version
igd_plus = IGDPlus(true_pareto_front)
print(f"IGD+: {igd_plus(res.F):.6f}")

# Spacing: uniformity of distribution (SMALLER = more uniform)
spacing = SpacingIndicator()
print(f"Spacing: {spacing(res.F):.6f}")
```

### Statistical Comparison

```python
from scipy.stats import mannwhitneyu, kruskal

# Compare two algorithms across 30 runs
hv_algo1 = [run_algorithm1(seed=i) for i in range(30)]
hv_algo2 = [run_algorithm2(seed=i) for i in range(30)]

stat, p_value = mannwhitneyu(hv_algo1, hv_algo2, alternative='greater')
print(f"p-value: {p_value:.4f}")
if p_value < 0.05:
    print("Algorithm 1 is significantly better")
```

## Decision Making (Selecting Final Solution)

```python
from pymoo.decomposition.asf import ASF
from pymoo.mcdm.pseudo_weights import PseudoWeights

# Method 1: Pseudo-weights (intuitive preference)
weights = np.array([0.5, 0.3, 0.2])  # importance per objective
pw = PseudoWeights(weights)
idx = pw.do(res.F)
print(f"Selected solution index: {idx}")

# Method 2: Achievement Scalarizing Function (ASF)
# Find solution closest to ideal point with given weights
asf = ASF()
idx = asf(res.F, weights).argmin()

# Method 3: Knee point (maximum trade-off)
from pymoo.mcdm.knee_point import KneePointFinder
kpf = KneePointFinder()
idx = kpf.do(res.F)

# Method 4: Compromise programming (closest to utopia)
ideal = res.F.min(axis=0)
nadir = res.F.max(axis=0)
normalized = (res.F - ideal) / (nadir - ideal + 1e-10)
distances = np.linalg.norm(normalized, axis=1)
idx = distances.argmin()
print(f"Compromise solution: {res.F[idx]}")
```

## Advanced Topics

### Custom Reference Directions

```python
# Layered reference directions for many-objective
from pymoo.util.ref_dirs import get_reference_directions

# Two-layer approach for 8 objectives
outer = get_reference_directions("das-dennis", 8, n_partitions=3)
inner = get_reference_directions("das-dennis", 8, n_partitions=2)
# Shrink inner points toward center
inner = inner / 2 + 1 / (2 * 8)
ref_dirs = np.vstack([outer, inner])
```

### Surrogate-Assisted MOO (Expensive Problems)

```python
# ParEGO: scalarize + GP surrogate for each subproblem
# When objective evaluations are expensive (e.g., CFD, molecular docking)
from pymoo.algorithms.moo.age2 import AGEMOEA2

# AGE-MOEA2: adaptive geometry estimation
algorithm = AGEMOEA2(pop_size=100)
```

### Constraint Handling in MOO

```python
# Custom constraint violation for repair
class ConstrainedMOP(ElementwiseProblem):
    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0] - 1)**2 + x[1]**2
        
        # Inequality constraints: g(x) <= 0
        g1 = x[0] + x[1] - 1.5  # x0 + x1 <= 1.5
        g2 = -x[0] + x[1] - 0.5 # x1 - x0 <= 0.5
        
        out["F"] = [f1, f2]
        out["G"] = [g1, g2]
```

### Visualization for Many Objectives

```python
from pymoo.visualization.pcp import PCP
from pymoo.visualization.radar import Radar
from pymoo.visualization.heatmap import Heatmap

# Parallel Coordinate Plot (best for 4-10 objectives)
pcp = PCP(title="Pareto Front — 5 Objectives",
          labels=["Potency", "Toxicity", "Synth", "ADME", "Cost"])
pcp.set_axis_style(color="grey", alpha=0.3)
pcp.add(res.F, color="blue", alpha=0.3)
pcp.add(res.F[idx], linewidth=3, color="red")  # selected solution
pcp.show()

# Radar/Spider plot for single solution comparison
radar = Radar(labels=["Potency", "Toxicity", "Synth", "ADME", "Cost"])
radar.add(res.F[0], label="Solution A")
radar.add(res.F[idx], label="Selected")
radar.show()

# Heatmap for comparing many solutions
heatmap = Heatmap(labels=["f1", "f2", "f3", "f4", "f5"])
heatmap.add(res.F[:20])
heatmap.show()
```

## Key Libraries

| Library | Focus | Strengths |
|---|---|---|
| **pymoo** | Full MOO framework | NSGA-II/III, MOEA/D, visualization, indicators |
| **DEAP** | Evolutionary framework | Flexible, multi-objective support |
| **Platypus** | MOEA library | Clean API, many algorithms |
| **jMetalPy** | Multi-objective | Academic reference implementation |
| **PaGMO/PyGMO** | Parallel optimization | Island model, multi-objective |
| **Optuna** | Hyperparameter MOO | TPE-based, Pareto dashboard |

## Anti-Patterns

- ❌ Using NSGA-II for >3 objectives (dominance resistance → use NSGA-III/MOEA/D)
- ❌ Comparing PFs without statistical tests across multiple runs
- ❌ Reporting only hypervolume — use ≥2 indicators (HV + IGD)
- ❌ Ignoring reference point choice for hypervolume (changes ranking!)
- ❌ Normalizing objectives with fixed bounds instead of adaptive nadir/ideal
- ❌ Too few reference directions for many-objective (need ≥10× per objective)
- ❌ Choosing a solution without explicit decision-making methodology
- ❌ Not validating the Pareto front against single-objective optima per axis

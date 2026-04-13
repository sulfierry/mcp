---
name: Genetic Algorithms & Evolutionary Computation
description: "Genetic algorithms, genetic programming, differential evolution, CMA-ES, island models, and evolutionary strategies. Fitness landscape analysis, operator design, and constraint handling for real-world optimization."
category: optimization
tags: genetic-algorithm, evolutionary-computation, ga, gp, differential-evolution, cma-es, optimization, metaheuristics
---

# Genetic Algorithms & Evolutionary Computation

Expert in evolutionary computation — designing, implementing, and tuning population-based optimization algorithms for complex search spaces.

## Use this skill when

- Designing genetic algorithms for combinatorial or continuous optimization
- Implementing custom crossover, mutation, and selection operators
- Solving problems with rugged, deceptive, or multimodal fitness landscapes
- Applying evolutionary strategies (ES), differential evolution (DE), or CMA-ES
- Genetic programming (GP) for symbolic regression or program synthesis
- Island-model and distributed evolutionary computation
- Constraint handling in evolutionary optimization
- Fitness landscape analysis and algorithm selection

## Core Paradigm

```
Initialize Population P(0) of N individuals
t ← 0
while not termination_criterion:
    Evaluate fitness f(x) for each x ∈ P(t)
    Parents ← Selection(P(t))
    Offspring ← Variation(Parents)      # crossover + mutation
    P(t+1) ← Replacement(P(t), Offspring)
    t ← t + 1
return best individual found
```

## Algorithm Selection Guide

| Problem Type | Best Algorithm | Alternative | When |
|---|---|---|---|
| **Continuous, unimodal** | CMA-ES | L-BFGS | Smooth landscape, moderate dims |
| **Continuous, multimodal** | DE/rand/1/bin | CMA-ES w/ restarts | Rugged landscape, <100 dims |
| **Continuous, high-dim** | CMA-ES (large-scale) | PSO | >100 dimensions |
| **Combinatorial (discrete)** | GA + problem-specific ops | Simulated annealing | TSP, scheduling, assignment |
| **Mixed-integer** | GA + repair/decode | MIES | Both continuous and discrete vars |
| **Symbolic/programs** | Genetic programming | Grammar evolution | Finding mathematical expressions |
| **Expensive evaluations** | Surrogate-assisted EA | Bayesian optimization | <1000 evaluations budget |
| **Dynamic environment** | Hyper-mutation GA | Particle swarm | Fitness changes over time |
| **Constrained** | ε-constrained DE | Penalty + repair | Hard/soft constraints |

## Genetic Algorithm Implementation

### Python (DEAP Framework)

```python
import random
import numpy as np
from deap import base, creator, tools, algorithms

# 1. Define fitness and individual
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

# 2. Register operators
toolbox = base.Toolbox()
N_VARS = 30
BOUNDS = (-5.12, 5.12)

toolbox.register("attr_float", random.uniform, BOUNDS[0], BOUNDS[1])
toolbox.register("individual", tools.initRepeat, creator.Individual,
                  toolbox.attr_float, n=N_VARS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 3. Fitness function (Rastrigin)
def rastrigin(individual):
    A = 10
    n = len(individual)
    return (A * n + sum(x**2 - A * np.cos(2 * np.pi * x) for x in individual),)

toolbox.register("evaluate", rastrigin)
toolbox.register("mate", tools.cxSimulatedBinaryBounded,
                  low=BOUNDS[0], up=BOUNDS[1], eta=20.0)
toolbox.register("mutate", tools.mutPolynomialBounded,
                  low=BOUNDS[0], up=BOUNDS[1], eta=20.0, indpb=1.0/N_VARS)
toolbox.register("select", tools.selTournament, tournsize=3)

# 4. Run
pop = toolbox.population(n=100)
hof = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min)
stats.register("avg", np.mean)
stats.register("std", np.std)

pop, log = algorithms.eaSimple(pop, toolbox,
                                cxpb=0.9, mutpb=0.1, ngen=300,
                                stats=stats, halloffame=hof, verbose=True)
print(f"Best fitness: {hof[0].fitness.values[0]:.6f}")
```

### Differential Evolution

```python
from scipy.optimize import differential_evolution

def objective(x):
    """Ackley function — multimodal, deceptive."""
    n = len(x)
    sum1 = -0.2 * np.sqrt(np.sum(x**2) / n)
    sum2 = np.sum(np.cos(2 * np.pi * x)) / n
    return -20 * np.exp(sum1) - np.exp(sum2) + 20 + np.e

bounds = [(-5, 5)] * 10
result = differential_evolution(
    objective, bounds,
    strategy='best1bin',   # mutation strategy
    maxiter=1000,
    popsize=15,            # multiplier: pop = popsize * n_vars
    tol=1e-12,
    mutation=(0.5, 1.0),   # F: dithering range
    recombination=0.7,     # CR: crossover probability
    seed=42,
    polish=True,           # L-BFGS polish at the end
    workers=-1,            # parallel evaluation
)
print(f"Minimum: {result.fun:.10f} at {result.x}")
```

### CMA-ES (Covariance Matrix Adaptation)

```python
import cma

# CMA-ES: state-of-the-art for continuous optimization
x0 = np.random.randn(10)  # initial solution
sigma0 = 0.5  # initial step size

es = cma.CMAEvolutionStrategy(x0, sigma0, {
    'maxiter': 1000,
    'tolx': 1e-12,
    'tolfun': 1e-12,
    'popsize': 50,  # None = auto
    'bounds': [[-5] * 10, [5] * 10],
    'seed': 42,
})

while not es.stop():
    solutions = es.ask()
    fitnesses = [objective(x) for x in solutions]
    es.tell(solutions, fitnesses)
    es.disp()

result = es.result
print(f"Best: f={result.fbest:.10f}")
```

## Operator Design Principles

### Selection Pressure Control

| Operator | Pressure | Use When |
|---|---|---|
| **Tournament (k=2)** | Low | Early exploration, diverse pop |
| **Tournament (k=5+)** | High | Late exploitation, convergence |
| **Roulette wheel** | Variable | Proportional fitness, positive values |
| **Rank-based** | Moderate | Fitness scaling issues |
| **Truncation** | Very high | Large populations, (μ,λ)-ES |
| **Lexicase** | Unique | GP, multiple test cases |

### Crossover Operators

```python
# SBX for real-valued (distribution index η)
# η → ∞: offspring near parents (exploitation)
# η → 0: uniform spread (exploration)

# For combinatorial:
# - Order crossover (OX) for permutations (TSP)
# - Uniform crossover for binary strings
# - PMX for permutations with position importance
```

### Adaptive Parameter Control

```python
# Self-adaptive mutation rate (1/5 success rule for ES)
class AdaptiveMutation:
    def __init__(self, sigma=0.1, tau=0.1):
        self.sigma = sigma
        self.tau = tau
    
    def mutate(self, individual):
        # Self-adaptation: mutate sigma first
        self.sigma *= np.exp(self.tau * np.random.randn())
        return individual + self.sigma * np.random.randn(len(individual))

# JADE: adaptive DE with memory
# F and CR adapated based on successful parameters
```

## Constraint Handling

```python
# Method 1: Penalty function
def penalized_fitness(x, constraints):
    f = objective(x)
    penalty = sum(max(0, g(x))**2 for g in constraints)
    return f + 1e6 * penalty

# Method 2: Feasibility rules (Deb 2000)
def constrained_tournament(ind1, ind2):
    feas1 = is_feasible(ind1)
    feas2 = is_feasible(ind2)
    if feas1 and not feas2: return ind1
    if feas2 and not feas1: return ind2
    if not feas1 and not feas2:
        return ind1 if violation(ind1) < violation(ind2) else ind2
    return ind1 if ind1.fitness < ind2.fitness else ind2

# Method 3: ε-constrained (gradually tighten feasibility)
# Start with ε = max_violation, reduce to 0 over generations
```

## Fitness Landscape Analysis

```python
# Fitness Distance Correlation (FDC)
def fdc(population, fitnesses, optimum):
    """FDC < -0.15: easy. FDC > 0.15: hard (deceptive)."""
    distances = [np.linalg.norm(ind - optimum) for ind in population]
    return np.corrcoef(fitnesses, distances)[0, 1]

# Ruggedness: autocorrelation of random walk
def ruggedness(objective, x0, n_steps=1000, step_size=0.01):
    fitnesses = []
    x = x0.copy()
    for _ in range(n_steps):
        x += np.random.randn(len(x)) * step_size
        fitnesses.append(objective(x))
    return np.corrcoef(fitnesses[:-1], fitnesses[1:])[0, 1]
```

## Key Libraries

| Library | Language | Strengths |
|---|---|---|
| **DEAP** | Python | Flexible, GP support, distributed |
| **pymoo** | Python | Multi-objective, visualization |
| **CMA-ES (pycma)** | Python | Gold standard for continuous |
| **scipy.optimize.differential_evolution** | Python | Simple DE, built-in |
| **ECJ** | Java | Full-featured EC framework |
| **JMETALPY** | Python | Multi-objective focus |
| **Platypus** | Python | MOEA library |
| **Optuna** | Python | Hyperparameter tuning with TPE |

## Anti-Patterns

- ❌ Using GA for smooth, differentiable problems (use gradient methods)
- ❌ Population too small (<50 for real-valued, <100 for combinatorial)
- ❌ Fixed mutation rate throughout evolution (use adaptation)
- ❌ Premature convergence without diversity maintenance
- ❌ Evaluating unnecessary fitness recalculations (cache evaluations)
- ❌ Random initialization outside feasible region for constrained problems
- ❌ Ignoring problem structure — designing generic operators instead of problem-specific ones
- ❌ Not comparing against simple baselines (random search, hill climbing)

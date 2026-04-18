---
name: causal-inference
description: "Pearl-style causal inference for PhD-grade scientific rigor. DAGs, do-calculus, backdoor/frontdoor criteria, counterfactuals, identification, confounders, colliders, mediation. Triggers when user discusses causal claims, confounding, treatment effects, instrumental variables, natural experiments, RCT analysis, observational study adjustments, or mediation analysis."
category: scientific-writing
tags: [causal-inference, dag, pearl, econometrics, statistics, phd]
---

# Causal Inference (Pearl framework)

## When to use
- User makes/questions causal claim in observational data
- Designing/analyzing RCT, quasi-experiment, instrumental variable, natural experiment
- Adjusting for confounding in regression or matching
- Reviewing paper claiming "X causes Y" from correlational data
- Mediation / moderation analysis

## Do NOT use for
- Pure prediction tasks (correlation suffices)
- Qualitative studies without quantitative causal claim

## Core framework (Pearl)

**Causal hierarchy (ladder):**
1. **Association** — seeing: `P(Y|X)` (correlations, ML predictions)
2. **Intervention** — doing: `P(Y|do(X))` (RCT, policy effect)
3. **Counterfactual** — imagining: `P(Y_x|X',Y')` (what-if, attribution)

Regression/ML operate at rung 1. Causal claims require rungs 2-3.

## DAG (Directed Acyclic Graph) basics

```
     Z (confounder)
    / \
   ↓   ↓
   X → Y
       ↑
       C (collider — don't condition!)
```

**Three structural patterns:**

| Pattern | Example | Condition on? |
|---------|---------|---------------|
| Chain `X→M→Y` | Mediator | Blocks path (may want partial) |
| Fork `X←Z→Y` | Confounder | MUST condition |
| Collider `X→C←Y` | Selection bias | NEVER condition (opens backdoor) |

**Classic mistake**: conditioning on colliders induces spurious correlation. See Berkson's paradox, "healthy worker" effect.

## Identification strategies

### 1. Backdoor criterion (Pearl)
Set `Z` blocks all backdoor paths from X to Y and contains no descendants of X.
→ `P(Y|do(X)) = Σ P(Y|X,Z) P(Z)` (g-formula)

### 2. Frontdoor criterion
Use when unmeasured confounder U between X and Y exists but a mediator M is observed and fully mediates X→Y.

### 3. Instrumental variables (IV)
Instrument Z satisfies: (a) Z→X, (b) Z⊥Y | X (exclusion), (c) Z⊥U (independence from confounder).
→ 2SLS, Wald estimator. Weak instruments = biased.

### 4. Regression discontinuity (RDD)
Sharp cutoff c on running variable X0. Treatment = 1{X0 ≥ c}. Local randomization near cutoff.
Assumption: no manipulation of X0.

### 5. Difference-in-differences (DiD)
Pre-post × treated-control. Identifies ATT under parallel trends.
Check: pre-treatment trends visually + placebo tests.

### 6. Synthetic controls (Abadie)
Weighted combination of donor units to build counterfactual.

### 7. Propensity score methods
Estimate `e(X) = P(Treat|X)`. Match, stratify, or inverse-probability weight (IPW).
Assumes: unconfoundedness given X, positivity (overlap).

## Checklist for reviewing causal claims

1. Draw the DAG. Pre-registered?
2. Identify: backdoor / frontdoor / IV / DiD / RDD?
3. Measured confounders adjusted? Unmeasured confounders plausible?
4. Colliders inadvertently conditioned on (e.g., selection bias)?
5. Positivity/overlap in covariates?
6. Effect heterogeneity (CATE) explored?
7. Sensitivity analysis: E-value, Rosenbaum bounds, Oster δ
8. Pre-registration / SAP?

## Common estimands

| Estimand | Meaning | Symbol |
|----------|---------|--------|
| ATE | Average Treatment Effect | `E[Y(1)−Y(0)]` |
| ATT | ATE on the Treated | `E[Y(1)−Y(0)|T=1]` |
| CATE | Conditional ATE | `E[Y(1)−Y(0)|X=x]` |
| LATE | Local ATE (IV) | Compliers only |
| NDE/NIE | Direct / indirect mediation | Pearl mediation |

## Tooling

- Python: `dowhy` (identification + estimation + refutation), `causalml`, `econml`, `causal-learn` (causal discovery)
- R: `dagitty`, `CausalImpact`, `MatchIt`, `Synth`, `tidysynth`, `did`
- DAGs: `dagitty.net` (web), `dagitty` R, `CausalFusion`

## Sensitivity analysis (always)

- **E-value** (VanderWeele): minimum confounder strength to explain away effect
- **Oster δ**: selection on unobservables relative to observables
- **Rosenbaum bounds**: for matched studies
- **Negative controls**: outcome unaffected by X should show null

## Key references

- Pearl — *Causality* (2009), *The Book of Why* (2018)
- Hernán & Robins — *Causal Inference: What If* (free online, MIT/Harvard)
- Imbens & Rubin — *Causal Inference for Statistics*
- Morgan & Winship — *Counterfactuals and Causal Inference*
- Cunningham — *Causal Inference: The Mixtape* (free online)

## Anti-patterns to flag

- "Controlled for X, Y, Z" without DAG justification → may open collider path
- Table 2 fallacy (interpreting control coefficients as causal)
- Stepwise regression for causal identification
- Comparing "statistical significance" vs "effect size" confusion
- Mediation via Baron-Kenny (superseded by Imai/Pearl causal mediation)
- Matching without positivity checks
- IV with weak instrument (F<10)

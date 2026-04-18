---
name: academic-epistemology
description: "Philosophy of science for PhD-level epistemic rigor. Popper (falsificationism), Kuhn (paradigms), Lakatos (research programmes), Feyerabend, Bayesian epistemology, inference to best explanation (IBE), underdetermination, theory-ladenness, scientific realism vs instrumentalism, causation vs correlation, demarcation problem. Triggers on falsifiable, paradigm, research programme, philosophy of science, epistemology, scientific reasoning, demarcation."
category: scientific-writing
tags: [epistemology, popper, kuhn, lakatos, bayesian, philosophy-of-science]
---

# Academic Epistemology

## When to use
- Framing thesis Introduction (what counts as evidence?)
- Defending methodological choices in viva
- Peer-reviewing claims ("is this falsifiable?")
- Positioning work in a research programme
- Discussing anomalies without abandoning theory

## Core positions

### Popper — falsificationism
- Demarcation: science = falsifiable claims; unfalsifiable → pseudoscience (psychoanalysis example).
- Progress via **bold conjectures** + **severe tests**. Confirmation ≠ proof.
- Corollary: avoid "safe" hypotheses. Prefer risky predictions.
- Criticism: strict falsificationism doesn't describe actual practice (Duhem-Quine thesis).

### Kuhn — paradigms & scientific revolutions
- Normal science within a **paradigm** (shared exemplars, methods, ontology).
- Anomalies accumulate → **crisis** → **revolution** → new paradigm.
- Paradigms are **incommensurable** (different vocabularies, standards).
- Your thesis typically extends normal science within current paradigm — acknowledge this.

### Lakatos — research programmes
- Hard core (unrevisable assumptions) + protective belt (revisable auxiliary hypotheses).
- Programmes are **progressive** (predict new facts) or **degenerative** (ad hoc rescues).
- Practical middle ground between Popper's strictness and Kuhn's descriptivism.
- Use to defend your research programme: "Each round adds new predictions, not just saves."

### Feyerabend — epistemic anarchism
- "Anything goes" — no universal method works across sciences.
- Historical case: Galileo's arguments were rhetorical, not deductive.
- Useful caution: don't fetishize single methodology.

## Bayesian epistemology

- Belief = probability. Update via Bayes:
  `P(H|E) ∝ P(E|H) · P(H)`
- Priors explicit, posteriors testable, sequential updates natural.
- Severity (Mayo): test passes only if `P(E|¬H) is low`.
- Model comparison: Bayes factors, posterior predictive checks, LOO-CV.
- Field-specific: `PyMC`, `Stan`, `brms`, `NumPyro`.

## Inference to the Best Explanation (IBE, Harman/Lipton)

- Infer the hypothesis that **best explains** evidence — not merely consistent.
- Criteria: consilience, simplicity, mechanism, fit with background knowledge.
- Warning: "best of available" ≠ "true". Rival explanations must be actually canvassed.
- Common in historical sciences (evolution, cosmology, forensics).

## Duhem-Quine underdetermination

Any test involves auxiliary assumptions (instruments, theory, background). Failed test → could be the core hypothesis OR any auxiliary. No clean falsification in practice.

Implication: make your auxiliaries explicit. List them. This is what methods sections are for.

## Theory-ladenness of observation (Hanson)

What counts as data depends on theory (e.g., "a cell", "a boson" presuppose concepts). Raw perception + pure theory-neutrality is a myth.

Implication: in thesis Methods, declare your ontology (what things exist for this work).

## Scientific realism vs anti-realism

- **Realism**: theories describe mind-independent reality; success = approximate truth.
- **Instrumentalism**: theories are predictive tools, nothing more.
- **Constructive empiricism** (van Fraassen): aim for empirical adequacy, agnostic on unobservables.
- **Structural realism** (Worrall/Ladyman): structure preserved across theory change.

Declare your stance when relevant (philosophy, foundations, interpretation-heavy fields like QM).

## Causation vs correlation

See `causal-inference` skill for Pearl framework. Epistemology:
- **Hume**: constant conjunction (+ temporal priority + contiguity).
- **Counterfactual** (Lewis): C causes E iff E wouldn't happen without C.
- **Interventionist** (Woodward): causes are things we could (in principle) manipulate.
- **Mechanistic** (Salmon, Craver): causal process/machinery.

Most modern experimental causal inference leans interventionist + mechanistic.

## Demarcation: what's science?

Popper: falsifiability. Modern: no single criterion; cluster of features:
- Falsifiable claims
- Peer-reviewed community
- Reproducible methods
- Openness to criticism
- Predictive track record
- Rejects ad hoc rescues

## Key distinctions (for writing)

| Pair | Difference |
|------|-----------|
| Law vs hypothesis | Law = broad regularity; hypothesis = specific, testable |
| Correlation vs causation | Statistical dependence vs intervention-invariant |
| Replication vs reproduction | Same study rerun (replication) vs same data rerun (reproduction) |
| Internal vs external validity | Within-sample causal vs generalization |
| Discovery vs justification | How you arrived vs how you defend |
| Descriptive vs normative | What is vs what should be |
| Explanation vs prediction | Why something happens vs what will happen |

## How to deploy in thesis writing

### In Introduction
- State framework (exploratory vs hypothesis-testing).
- If hypothesis-testing: articulate falsifiable predictions.
- If theory-building: acknowledge your paradigm + why extending it.

### In Methods
- Make auxiliaries explicit (preprocessing choices, software versions).
- Pre-register specific vs exploratory analyses.
- State stopping rules.

### In Discussion
- Honestly label: confirmation vs corroboration (Popper: theories never *proven*, only *corroborated*).
- Identify alternative explanations; show why less plausible.
- Label: what would change your mind? (severe-test criterion)

### In defense
- "Is this falsifiable?" — Yes: here's the prediction that, if wrong, would refute.
- "You chose [method]; why not [alternative]?" — Epistemological trade-offs (severe testing vs discoverability).

## References

- Popper — *The Logic of Scientific Discovery*, *Conjectures and Refutations*
- Kuhn — *The Structure of Scientific Revolutions*
- Lakatos & Musgrave — *Criticism and the Growth of Knowledge*
- Feyerabend — *Against Method*
- Mayo — *Statistical Inference as Severe Testing*
- Sober — *Core Questions in Philosophy*, *Evidence and Evolution*
- Pearl & Mackenzie — *The Book of Why* (causation)
- Chalmers — *What Is This Thing Called Science?* (textbook)
- van Fraassen — *The Scientific Image*
- Woodward — *Making Things Happen*

## Anti-patterns to detect

- "Our theory predicts X" when "X" is unfalsifiably vague
- Post-hoc explanation fitting every possible result
- Treating p < 0.05 as theory-confirmation rather than corroboration
- Claiming causation from observational data without intervention/IV/DAG
- Ad hoc auxiliary additions to save a failing hypothesis (degenerative programme)
- Underdetermination waived away ("we ruled out everything")
- Theory-neutral observation claims

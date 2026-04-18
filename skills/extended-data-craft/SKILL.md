---
name: extended-data-craft
description: "Extended Data figures and Supplementary Information for Nature/Science/Cell submissions. ED-figure anatomy (standalone caption, high-content density), SI structure (methods in depth, source data, extended analyses), reporting summary (Nature), cross-referencing discipline, figure-supplement vs extended-data distinction. Triggers on Extended Data, Supplementary, SI, ED figure, source data, reporting summary."
category: scientific-writing
tags: [extended-data, supplementary, nature, cell, figures, phd]
---

# Extended Data & Supplementary Craft

## Why ED/SI matters for top-tier
In Nature / Science / Cell, reviewers scrutinize ED + SI heavily. Many papers are accepted/rejected based on ED strength, not main figures. Treat them as paper-within-the-paper.

## Terminology (varies by journal)

| Journal | Main | Expanded | Raw |
|---------|------|----------|-----|
| Nature | Main Fig 1-N (≤ 6 typically) | Extended Data Fig 1-10 | Supplementary Information |
| Nature Methods | Main Fig 1-N | Supplementary Fig 1-N | SI |
| Cell | Main 1-7 | Figure S1, S2 (per main fig) | SI Methods |
| Science | Fig 1-N (≤ 4) | — | Materials & Methods (body) + Supplementary (figs + tables) |
| eLife | Main 1-N | Figure supplements (indexed to parent fig) | Appendices |

## Extended Data Figure anatomy (Nature)

Each ED figure must:
- Stand alone (reader grasps without main text)
- Have self-contained title + caption (often 200-400 w)
- Include all controls, replicates, quantifications
- Match main-figure aesthetic (same palette, fonts, sizing)
- Cite EVERY panel in main text explicitly

## Typical 10 ED figures (biology paper)

1. ED1: Reagent / reagent validation (antibody specificity, construct maps)
2. ED2: Expanded methods comparison or QC
3. ED3: Replicates / biological variability
4. ED4: Negative / positive controls
5. ED5: Additional conditions / doses
6. ED6: Alternative experimental system (orthogonal validation)
7. ED7: Structural / computational extended analyses
8. ED8: Single-cell / subpopulation breakdowns
9. ED9: Genetic / pharmacological perturbation controls
10. ED10: Survival / clinical / in-vivo expansion

## Supplementary Information structure

```
Supplementary Information
├── Supplementary Methods (extended methods, parameters, algorithms)
├── Supplementary Figures (rare if ED covers main needs)
├── Supplementary Tables (large tables: sample metadata, gene lists, parameters)
├── Supplementary Notes (short essays on specific points)
├── Supplementary Data (separate files: source data, sequences)
├── Supplementary Video (separate files)
└── Source Data (per-figure Excel/CSV)
```

## Source Data discipline (Nature 2020+ mandate)

Each main + ED figure needs `Source Data Fig N.xlsx` with:
- Sheet per panel (Fig 1a, 1b, ...)
- Raw values that generated plot
- Replicate counts + statistics formula
- Not just summary statistics; individual data points

Reviewers verify plots against Source Data.

## Reporting Summary (Nature, Life Sciences journals)

PDF form covering:
- Statistical reporting (sample size, replication, allocation, blinding)
- Reagents (antibody, cell-line authentication)
- Eukaryotic cell lines
- Animals
- Human subjects / ethics
- Data availability
- Code availability

Fill BEFORE submission. Editors desk-reject for missing fields. Fields flagged "n/a" require justification.

## Cross-referencing discipline

Every ED panel MUST be cited in:
- Main text (at least once)
- Main figure caption (where related)
- Main text methods (where relevant)

Absent citation → reviewer flags as "unnecessary", often cut from paper.

## Main-vs-ED decision rubric

| Content | Main | ED |
|---------|------|----|
| Core claim with key quantification | ✅ | |
| Replicates of main experiment | | ✅ |
| Controls supporting main claim | | ✅ |
| Alternative interpretation data | | ✅ |
| Methodological validation | | ✅ |
| Orthogonal validation of main finding | | ✅ (or main if space) |
| Extensive exploration of parameter space | | ✅ (SI) |
| Full pipeline documentation | | SI Methods |

Rule of thumb: if you'd lose sleep over it being cut → main. If it supports but doesn't carry the story → ED.

## Extended Data caption pattern

```
ED Fig X: [Title as complete sentence describing finding].
(a) [Panel description: what's shown, n, technique]. [Quantification: sample
size, statistical test, p value]. (b) ... (c) ... Individual data points
shown; bars represent mean ± s.e.m. n=[number] biological replicates per
condition. Statistical test: [two-sided Student's t-test / Mann-Whitney /
ANOVA with Tukey]. Exact p values in Source Data.
```

## Common reviewer complaints about ED/SI

- "Missing controls for [condition]" → add or pre-empt
- "Sample size too small" → explicitly power-justify in caption
- "Replicates unclear" → distinguish biological vs technical
- "Source data missing" → upload per figure
- "Reporting summary incomplete" → fill every field
- "Mismatch between main text value and ED figure" → triple-check before submission

## Nature-specific rules

- Max 10 Extended Data figures (exceeding requires editor permission)
- ED figures count against review time
- ED figures published alongside main (online) — permanent part of paper
- Same peer review as main figures

## Cell-specific rules

- Figure supplements indexed to parent main figure (Fig S1 supports Fig 1)
- STAR Methods (Structured, Transparent, Accessible Reporting) in body, not SI
- Key Resources Table mandatory

## Science-specific rules

- No ED — everything in Supplementary (which can be extensive)
- Supplementary split into: Materials & Methods, Figs S1-N, Tables S1-N, References
- Main paper MUST stand alone for non-specialist — SI depth for specialists

## Anti-patterns

- Dumping failed experiments into SI (looks unprincipled)
- ED figures without citation in main
- Caption says "see Methods" without reference pointer
- Source data as PDFs (must be machine-readable)
- SI text exceeding main text length (reorganize)
- Using main-text slots for controls (move to ED)
- Inconsistent panel labels (a,b,c vs A,B,C)
- Different color palettes main vs ED (jarring)
- Missing scale bars (image figures)
- n reported without distinguishing technical vs biological replicates

## Checklist

- [ ] Each ED panel cited in main text
- [ ] Source Data per figure (main + ED)
- [ ] Reporting Summary complete
- [ ] Statistical tests + exact p values in captions
- [ ] Replicate nature (biol/tech) labeled
- [ ] Scale bars on all image panels
- [ ] Error bar definition in every caption
- [ ] Key Resources Table (Cell) / similar in Methods
- [ ] Max 10 ED figures (Nature)
- [ ] Main figures stand alone for non-specialist
- [ ] ED figures stand alone for specialist
- [ ] SI text < main text length
- [ ] Source Data Excel files per figure
- [ ] Videos in standard format (MP4 H.264) with legends

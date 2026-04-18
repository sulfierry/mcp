---
name: systematic-review-prisma
description: "PRISMA 2020-compliant systematic review protocol. Registration (PROSPERO), search strategy, PICO, inclusion/exclusion, dual screening, risk of bias (ROB2/ROBINS-I), data extraction, GRADE certainty, PRISMA flow diagram, synthesis (narrative, meta-analysis, GRADE summary). Triggers on systematic review, scoping review, meta-analysis, PRISMA, PROSPERO, Cochrane review, umbrella review, realist synthesis."
category: scientific-writing
tags: [prisma, systematic-review, meta-analysis, cochrane, grade, phd]
---

# Systematic Review (PRISMA 2020)

## When to use
- Conducting systematic/scoping/umbrella review or meta-analysis
- Writing review protocol for PROSPERO registration
- Auditing existing review against PRISMA 2020 checklist

## Review types (choose one)

| Type | Purpose | Synthesis |
|------|---------|-----------|
| Systematic review | Answer focused question | Narrative / meta-analysis |
| Meta-analysis | Quantitative pooling | Forest plot, heterogeneity |
| Scoping review | Map field breadth | Charting (JBI, Arksey-O'Malley) |
| Rapid review | Fast policy-relevant | Abbreviated methods |
| Umbrella review | Review of reviews | Overview of systematic reviews |
| Realist synthesis | Mechanisms + context | Narrative, program theory |
| Living review | Continuously updated | Incremental |

## Protocol checklist (pre-registration)

Register BEFORE screening starts:
- **PROSPERO** (health)
- **OSF Registries** (any field)
- **Research Registry** (surgery)
- **INPLASY**

Protocol must specify:
1. Review question (PICO/PECO/SPIDER/CoCoPop)
2. Eligibility criteria (include/exclude)
3. Information sources (databases + grey lit)
4. Search strategy (Boolean + MeSH + drafted by librarian)
5. Screening process (dual, blinded, conflict resolution)
6. Data extraction fields
7. Risk of bias tool
8. Synthesis plan (narrative vs meta, subgroups, sensitivity)
9. Certainty assessment (GRADE)
10. Amendments policy

## PICO frameworks

| Framework | For | Elements |
|-----------|-----|----------|
| PICO | Intervention | Population, Intervention, Comparator, Outcome |
| PECO | Exposure (epi) | Population, Exposure, Comparator, Outcome |
| SPIDER | Qualitative | Sample, Phenomenon, Design, Evaluation, Research type |
| CoCoPop | Prevalence | Condition, Context, Population |
| PEO | Qualitative | Population, Exposure, Outcome |

## Search strategy

**Databases (minimum)**:
- Medicine: MEDLINE (PubMed), Embase, Cochrane CENTRAL
- Psychology: PsycINFO, PubMed
- Ed: ERIC, PsycINFO
- General: Scopus, Web of Science
- Grey: OpenGrey, ClinicalTrials.gov, WHO ICTRP, preprint servers (bioRxiv, medRxiv)

**Search construction**:
- Blocks per PICO element, OR within, AND between
- Controlled vocabulary (MeSH/Emtree) + free-text + wildcards
- Peer-review via PRESS checklist (Peer Review of Electronic Search Strategies)
- Report exact strings per database + date of last search

## Screening workflow

1. **Deduplication**: EndNote/Zotero + Rayyan/Covidence dedup
2. **Title/abstract screening**: dual, blinded, Rayyan/Covidence
3. **Conflict resolution**: third reviewer or consensus
4. **Full-text screening**: dual, reasons for exclusion logged
5. **Inter-rater reliability**: Cohen's κ ≥ 0.6 recommended
6. **Snowballing**: forward (citing) + backward (references) of included

Tools: Rayyan (free), Covidence, DistillerSR, ASReview (AI-assisted).

## Risk of bias (ROB) tools

| Study type | Tool |
|------------|------|
| RCT | **RoB 2.0** (Cochrane) |
| Non-randomized interventions | **ROBINS-I** |
| Diagnostic accuracy | **QUADAS-2** |
| Prognostic | **QUIPS** / PROBAST |
| Prevalence | JBI checklist |
| Qualitative | CASP |
| Systematic reviews | AMSTAR 2, ROBIS |

Report domain-level + overall judgment. robvis R package → traffic-light plots.

## PRISMA 2020 flow diagram

```
Identification
  Records from databases (n = )
  Records from registers (n = )
  Records from other sources (n = )
     ↓ Duplicates removed (n = )
Screening
  Records screened (n = )
     → Excluded (n = )
  Reports sought for retrieval (n = )
     → Not retrieved (n = )
  Reports assessed for eligibility (n = )
     → Excluded with reasons (n = , by reason)
Included
  Studies included (n = ), reports (n = )
```

Use prisma2020 R package or `prismastatement.org` app.

## Data extraction

Standardize in piloted form. Fields:
- Study ID, design, setting, dates
- Population (n, age, sex, comorbidity, country)
- Intervention details (TIDieR checklist)
- Comparator
- Outcomes (definition, measurement, timing)
- Effect estimates + 95% CI + variance
- Funding, COI
- Risk of bias per domain

Tools: Covidence, EPPI-Reviewer, SRDR+, SWiM tables.

## Synthesis

### Narrative synthesis
- SWiM guidance (Synthesis Without Meta-analysis)
- Grouping by outcome, population, intervention
- Visual: harvest plot, effect direction plot

### Meta-analysis
- Random-effects default (DerSimonian-Laird or REML)
- I² / τ² for heterogeneity; prediction intervals
- Subgroup + meta-regression (if k ≥ 10 per covariate)
- Publication bias: funnel plot, Egger's test, trim-and-fill, Doi plot
- Sensitivity: leave-one-out, risk-of-bias subset

Tools: `metafor` (R, gold standard), `meta` R, `metan` Stata, `PythonMeta`.

### Network meta-analysis (NMA)
Indirect comparisons. Assumes transitivity + consistency. Tools: `netmeta` R, `multinma` R. SUCRA for ranking.

## GRADE (certainty of evidence)

Rate per outcome across studies:
- Start: RCTs = high, observational = low
- **Downgrade** for: risk of bias, inconsistency, indirectness, imprecision, publication bias
- **Upgrade** for: large effect, dose-response, plausible confounders would reduce effect

Summary: High / Moderate / Low / Very Low. Use GRADEpro GDT (free).

## Reporting checklists

- **PRISMA 2020**: systematic reviews
- **PRISMA-S**: search reporting
- **PRISMA-ScR**: scoping reviews
- **PRISMA-NMA**: network MA
- **MOOSE**: observational study MA
- **RAMESES**: realist / meta-narrative
- **ENTREQ**: qualitative synthesis

## Timeline (realistic)

- Protocol: 4-8 weeks
- Search + deduplication: 2-4 weeks
- Screening: 2-6 months (depends on hits)
- Extraction + ROB: 2-4 months
- Synthesis + write-up: 2-4 months

**Total**: 12-24 months for rigorous SR.

## Anti-patterns

- Post-hoc protocol changes without amendment log
- Single-reviewer screening (bias)
- Narrative synthesis reported as "meta-analysis"
- Ignoring grey literature / preprints → publication bias
- Missing PRESS peer review of search strategy
- Reporting "no heterogeneity" from non-significant Q (underpowered)
- Cherry-picked subgroups without pre-registration

---
name: open-science-workflow
description: "Open science lifecycle for PhD-grade work. Pre-registration (OSF, AsPredicted, Registered Reports), protocol sharing (protocols.io), preprint servers (arXiv, bioRxiv, medRxiv, SSRN, PsyArXiv, EarthArXiv, ChemRxiv), data sharing (Zenodo, OSF, domain repositories), code DOI, open access routes (gold, green, diamond), licensing (CC-BY, ODbL), ORCID, CRediT taxonomy, ROR, RAiD. Triggers on pre-registration, preprint, registered report, open access, OSF, Zenodo, CRediT, ORCID, FAIR."
category: scientific-writing
tags: [open-science, pre-registration, preprint, osf, zenodo, credit]
---

# Open Science Workflow

## Four pillars
1. **Pre-registered design** — commit before data
2. **Shared materials** — data, code, protocols, stimuli
3. **Open access** — accessible output
4. **Transparent authorship** — CRediT, conflicts, funding

## Pre-registration

### When
Before any data collection / analysis if predictive. For secondary data: before looking.

### Where
| Platform | Best for |
|----------|----------|
| **OSF Registries** | any field, versioned |
| **AsPredicted.org** | short pre-reg (9 questions), psych |
| **PROSPERO** | systematic reviews (health) |
| **ClinicalTrials.gov** | clinical trials (required US/EU) |
| **WHO ICTRP** | international clinical trials |
| **EGAP** | experimental policy/political science |
| **clinicaltrials.gov + EudraCT** | drug trials |

### Contents
1. Research question (specific, falsifiable)
2. Hypotheses (directional if warranted)
3. Design (RCT? quasi-exp? obs?)
4. Sample size + stopping rule (power calc)
5. Variables (DVs, IVs, covariates, exclusions)
6. Analysis plan (model, test, threshold)
7. Inference criteria (what counts as support vs refutation)
8. Deviations-from-plan policy

## Registered Reports (IPA)

Submit Stage 1 manuscript (intro + methods) → peer-reviewed → in-principle acceptance (IPA) → data collection → Stage 2 (results + discussion) → publication regardless of outcome.

Publishers: Cortex, Nature Human Behaviour, BMC Psychology, PLOS Biology, eLife, Royal Society Open Science.

Eliminates publication bias, p-hacking, HARKing.

## Preprint servers (by field)

| Field | Server |
|-------|--------|
| Physics/Math/CS | **arXiv** |
| Biology | **bioRxiv** |
| Medicine | **medRxiv** |
| Social sciences | **SSRN**, SocArXiv |
| Psychology | **PsyArXiv** |
| Chemistry | **ChemRxiv** |
| Earth science | **EarthArXiv** |
| Engineering | **TechRxiv**, engrXiv |
| Humanities | **Humanities Commons** |
| General | **Research Square**, Preprints.org, Zenodo preprints |

Post on submission. Usually required by funders (NIH, Wellcome).

## Protocol sharing

- **protocols.io** — versioned lab protocols with DOI
- **Bio-protocol** — peer-reviewed methods
- **OSF** — generic

Cite protocol DOI in paper methods.

## Data sharing (FAIR)

See also: `reproducibility-manifest` skill for detailed infrastructure.

Hierarchy:
1. **Raw data** — often embargoed/restricted (sensitive samples)
2. **Processed data** — share whenever possible
3. **Metadata** — always share (even if data restricted)
4. **Summary statistics** — minimum acceptable

Controlled access for sensitive data: **EGA**, **dbGaP**, **NDA**.

## Open access (OA) routes

| Route | Meaning | Cost |
|-------|---------|------|
| **Gold** | Publish in OA journal | APC (often $2k-$12k) |
| **Green** | Self-archive in repo (preprint or postprint) | Free |
| **Hybrid** | Subscription journal with OA option | APC |
| **Diamond** | OA, no APC to author | Free (community-funded) |
| **Bronze** | Free-to-read, not CC-licensed | Publisher-dependent |

Check journal's **Sherpa Romeo** entry for green OA permissions.

**Transformative agreements** (read-and-publish deals) via consortia: check if your institution has one.

Diamond examples: Q Open, SciPost, Cell Reports Methods (partially).

## Data licensing

| License | Meaning |
|---------|---------|
| **CC0** | Public domain dedication |
| **CC-BY** | Credit required — default for open |
| **CC-BY-SA** | Share-alike |
| **CC-BY-NC** | Non-commercial (creates compatibility issues; avoid) |
| **ODbL** | For databases |

Never: CC-BY-ND (prevents reuse / translation).

## Code licensing

| License | Note |
|---------|------|
| **MIT** | Permissive, most compatible |
| **Apache-2.0** | Permissive + patent clause |
| **BSD-3-Clause** | Permissive, academic-friendly |
| **GPL-3.0** | Copyleft — viral |
| **MPL-2.0** | File-level copyleft |
| **Unlicense / 0BSD** | Public-domain-like |

Default recommendation: **MIT or Apache-2.0** unless you need copyleft.

## Authors, identifiers, contributions

- **ORCID** (`https://orcid.org/0000-0000-0000-0000`): link all authors; required by most journals.
- **ROR** (`https://ror.org/...`): institutional identifier.
- **RAiD**: persistent project ID.
- **Funder IDs** (Crossref, ROR): report funding transparently.

### CRediT taxonomy (14 roles)
Conceptualization, Data curation, Formal analysis, Funding acquisition, Investigation, Methodology, Project administration, Resources, Software, Supervision, Validation, Visualization, Writing – original draft, Writing – review & editing.

Each author's roles listed at end of paper.

## Transparency statements (required by many venues)

- **Data availability**: where + how + license
- **Code availability**: URL + DOI + version
- **Materials availability**: sharing policy
- **Conflicts of interest** (ICMJE disclosure form)
- **Funding** (with grant numbers)
- **Ethics approval** (IRB/ethics committee ID)
- **AI disclosure** (is AI used in writing/analysis? how?)
- **Author contributions** (CRediT)

## Post-publication

- **Registered reports** + **retractable** corrections if needed via **PubPeer** (post-pub review).
- **Loop** / **ResearchGate** / **personal site** for outreach (but: real archival = Zenodo/OSF).
- **Altmetrics** (Altmetric.com, PlumX) — complementary, not replacement for citations.
- **Versioned re-sharing** — update preprints; cite v2, v3.

## Field-aware checklists

- **NIH**: Data Management and Sharing Policy (2023+) — plan at proposal stage.
- **Wellcome Trust**: mandatory OA CC-BY, preprints + data sharing.
- **ERC**: Plan S compliant, open access required.
- **cOAlition S / Plan S**: CC-BY on accepted manuscript, no embargoes.
- **ARRIVE 2.0**: animal research reporting.
- **CONSORT**: clinical trials.
- **STROBE**: observational.
- **TRIPOD+AI**: prediction models.
- **SPIRIT**: trial protocols.

## Anti-patterns

- Preprint without corresponding code/data
- "Available on reasonable request" (≈ never shared)
- CC-BY-NC for academic work (blocks other academics)
- Pre-registration that's vague ("we'll test H1") — must be specific
- HARKing then claiming pre-registration
- Open data without metadata/codebook
- Code dumps without README or env lockfile
- Using `gradient-descent.com` style personal URLs for archival (non-persistent)

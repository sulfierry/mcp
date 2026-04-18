---
name: reproducibility-manifest
description: "Computational reproducibility infrastructure for PhD-grade research. Containerized environments (Docker, Apptainer/Singularity), language-specific lockfiles (uv, poetry, renv, conda-lock), workflow orchestration (Nextflow, Snakemake, Make), data/code archiving (Zenodo, OSF, Dryad), persistent identifiers (DOI, ORCID), FAIR principles. Triggers on reproducibility, replicable, code sharing, data sharing, FAIR, containerization for research."
category: scientific-writing
tags: [reproducibility, docker, fair, zenodo, phd, open-science]
---

# Reproducibility Manifest

## When to use
- Preparing code + data for publication (required by most top journals)
- Archiving analysis for long-term reuse
- Responding to reviewers demanding reproducibility artifacts
- Submitting to venues with reproducibility badges (ACM, NeurIPS, MICCAI)

## Levels of reproducibility

1. **Methods reproducibility**: enough detail to rerun in principle
2. **Results reproducibility**: same result from same code + data (computational)
3. **Robustness**: same conclusion on variations (different subset, seed)
4. **Generalizability**: same conclusion across populations/settings

## Minimum reproducibility manifest

Repo layout (gold standard):
```
project-root/
├── README.md                   # entry point, DOI, badges
├── CITATION.cff                # machine-readable citation
├── LICENSE                     # code license (MIT/Apache/GPL)
├── LICENSE-DATA                # data license (CC-BY-4.0 typical)
├── paper/                      # manuscript source (LaTeX)
├── code/
│   ├── src/                    # source code
│   └── notebooks/              # analysis notebooks
├── data/
│   ├── raw/                    # immutable input (often via Zenodo ref)
│   ├── processed/              # reproducible from raw
│   └── README.md               # data dictionary
├── results/
│   ├── figures/
│   └── tables/
├── env/
│   ├── Dockerfile              # or Apptainer.def
│   ├── pyproject.toml          # or requirements.lock
│   └── environment.yml         # conda lockfile
├── workflow/
│   └── Snakefile               # or main.nf / Makefile
├── docs/
│   └── reproduce.md            # step-by-step reproduction
└── CHANGELOG.md
```

## Environment pinning (choose per language)

### Python
- **uv** (new SOTA, 2024+): `uv lock` + `uv sync`. Replaces pip-tools/poetry.
- **pixi**: conda-alternative. Deterministic cross-platform.
- **poetry**: still common. `poetry lock --no-update`.
- **conda-lock**: `conda-lock --file environment.yml -p linux-64 -p osx-arm64`.
- NEVER: bare `pip install foo` → not reproducible.

### R
- **renv**: `renv::snapshot()` → renv.lock. Restore: `renv::restore()`.
- **groundhog**: time-travel package versions.
- **rocker** Docker images pinned by R version.

### Julia
- `Project.toml` + `Manifest.toml` tracked in git. `Pkg.instantiate()`.

### System
- **Nix / NixOS**: purely functional, hermetic — gold standard but steep learning curve.
- **Guix**: similar, scientific-community favorite.

## Containerization

**Docker** (most portable):
```dockerfile
FROM python:3.12-slim@sha256:<digest>  # pin digest!
COPY pyproject.toml uv.lock .
RUN pip install uv && uv sync --frozen
COPY . .
ENTRYPOINT ["python", "-m", "analysis"]
```

Pin base image digest. Use multi-stage to reduce size.

**Apptainer (formerly Singularity)** for HPC/no-root:
```
Bootstrap: docker
From: python:3.12-slim

%post
  pip install uv
  uv sync --frozen
```

**Binder / mybinder.org**: one-click reproducible notebooks from GitHub repo with `environment.yml`.

## Workflow orchestration

| Tool | Strengths | Field |
|------|-----------|-------|
| **Nextflow** | DSL2, multi-cloud, nf-core curated pipelines | bioinformatics gold std |
| **Snakemake** | Python-based, conda integration | bio/general |
| **WDL + Cromwell** | Cloud workflows, Broad Institute | genomics |
| **CWL** | JSON/YAML, portable | standard-compliant |
| **Make** | Universal, simple | general |
| **dvc** | Data + ML pipeline versioning | ML |
| **Prefect / Airflow** | Orchestration-heavy | production |

All provide DAG execution, resumability, and provenance graphs.

## Data archiving (long-term, citable)

**Generalist**:
- **Zenodo** (CERN/EU) — DOI, 50 GB free per deposit, integrates with GitHub releases
- **Dryad** — curated, fee-based, biomedical/environmental
- **OSF (Open Science Framework)** — projects + files + pre-reg
- **Figshare** — free up to 20 GB
- **Harvard Dataverse** — social sciences

**Domain-specific**:
- Genomics: SRA / ENA / GEO / ArrayExpress
- Proteomics: PRIDE / MassIVE
- Structures: PDB / EMDB
- Neuro: OpenNeuro, DANDI
- Materials: Materials Cloud, NOMAD
- Climate: PANGAEA

**Archived code (DOI)**:
Zenodo-GitHub integration: tag release → Zenodo mints DOI automatically.

## FAIR principles

- **Findable**: DOI/PID, rich metadata, indexed
- **Accessible**: open protocol (HTTP), metadata even if data restricted
- **Interoperable**: standard formats (CSV, HDF5, Parquet, NetCDF, BIDS)
- **Reusable**: clear license, provenance, domain standards

Check via **F-UJI** (FAIR assessment), **FAIR-Checker**, ARDC tools.

## Persistent identifiers (PIDs)

- **DOI** for artifact (via Zenodo/Dryad)
- **ORCID** for authors
- **RAiD** for projects
- **ROR** for institutions
- **IGSN** for samples
- **Ontologies**: EDAM, UBERON, CL, MESH, ChEBI — use terms, not free text

## Recommended badges / checklists

- **ACM Reproducibility Badges**: Artifacts Evaluated, Results Reproduced, Results Replicated
- **NeurIPS/ICML Reproducibility Checklist**
- **MICCAI Code & Data Availability**
- **TRIPOD-AI** for clinical prediction models
- **ARRIVE 2.0** for animal research

## Seed and determinism

- Set seeds for every RNG source: Python `random`, NumPy, PyTorch, TF, JAX, R `set.seed()`.
- Document non-determinism sources: GPU atomics, parallel reductions, threading.
- Record: CUDA version, cuDNN, BLAS variant (MKL/OpenBLAS), CPU model.

## Provenance tracking

- **ReproZip** captures execution + deps automatically.
- **Sumatra** logs analysis runs.
- **MLflow** / **DVC** / **Weights & Biases** for ML experiments.
- **Provenance crates** (RO-Crate) for workflow metadata.

## Publishing checklist

Before submission:
- [ ] Repo public (or embargoed with DOI)
- [ ] CITATION.cff present
- [ ] Dockerfile/env lockfile committed
- [ ] All figures/tables regenerable from `make reproduce`
- [ ] Raw data archived at Zenodo/domain repo with DOI
- [ ] ORCID linked to all authors
- [ ] License files present (code + data separate)
- [ ] README has exact "How to reproduce in X minutes" section
- [ ] CI runs end-to-end on tagged release

## Anti-patterns

- "Data available on request" → reviewers rightly flag
- Analysis in Excel without script → irreproducible
- Dependencies listed as `requirements.txt` with no versions
- `conda activate my-env` without environment.yml
- `latest` Docker tag (breaks on rebuild)
- Git repo without release tag referenced in paper
- Figures generated by `gedit`-edited scripts in subfolders

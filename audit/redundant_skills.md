# Redundant skills audit

Total skills: 1179   |   Target: ~65-80 removable   |   Est token reduction after Phase 1: ~18 skills

## Phase 1 — Near-duplicate pairs (pick one)

| A | A lines | B | B lines | Recommend keep | Reason |
|---|---------|---|---------|----------------|--------|
| `anndata` | 398 | `anndata-data-structure` | 548 | **anndata-data-structure** | B significantly more content |
| `scanpy` | 384 | `scanpy-scrna-seq` | 381 | **scanpy** | A longer/canonical |
| `scvi-tools` | 188 | `scvi-tools-single-cell` | 590 | **scvi-tools-single-cell** | B significantly more content |
| `pydeseq2` | 557 | `pydeseq2-differential-expression` | 356 | **pydeseq2** | A longer/canonical |
| `deseq2-basics` | 469 | `deseq2-differential-expression` | 488 | **deseq2-basics** | A canonical name |
| `rnaseq-de` | 87 | `rnaseq-to-de` | 338 | **rnaseq-to-de** | B significantly more content |
| `featurecounts-counting` | 185 | `featurecounts-rna-counting` | 327 | **featurecounts-rna-counting** | B significantly more content |
| `pyopenms` | 215 | `pyopenms-mass-spectrometry` | 575 | **pyopenms-mass-spectrometry** | B significantly more content |
| `rdkit` | 778 | `rdkit-cheminformatics` | 466 | **rdkit** | A longer/canonical |
| `molfeat` | 509 | `molfeat-molecular-featurization` | 409 | **molfeat** | A longer/canonical |
| `datamol` | 704 | `datamol-cheminformatics` | 466 | **datamol** | A longer/canonical |
| `torch-geometric` | 421 | `torch-geometric-graph-neural-networks` | 534 | **torch-geometric** | A canonical name |
| `networkx` | 435 | `networkx-graph-analysis` | 553 | **networkx** | A canonical name |
| `flowio` | 606 | `flowio-flow-cytometry` | 345 | **flowio** | A longer/canonical |
| `adaptyv` | 211 | `adaptyv-bio` | 457 | **adaptyv-bio** | B significantly more content |
| `dbsnp-database` | 622 | `dbsnp-queries` | 171 | **dbsnp-database** | A longer/canonical |
| `clinvar-database` | 455 | `clinvar-lookup` | 188 | **clinvar-database** | A longer/canonical |
| `single-cell-annotation` | 250 | `single-cell-annotation-guide` | 251 | **single-cell-annotation** | A canonical name |

## Phase 2 — Cluster consolidations (manual merge needed)

### Agent↔Skill collisions (9) — decide per pair
| Agent | Skill same ID | Keep as |
|-------|---------------|---------|
| `academic-pipeline` | yes | agent (if persona needed) OR skill (if not) |
| `bioinformatics-researcher` | yes | agent (if persona needed) OR skill (if not) |
| `code-reviewer` | yes | agent (if persona needed) OR skill (if not) |
| `deep-research` | yes | agent (if persona needed) OR skill (if not) |
| `devops-engineer` | yes | agent (if persona needed) OR skill (if not) |
| `docking-specialist` | yes | agent (if persona needed) OR skill (if not) |
| `fullstack-developer` | yes | agent (if persona needed) OR skill (if not) |
| `python-architect` | yes | agent (if persona needed) OR skill (if not) |
| `ui-ux-designer` | yes | agent (if persona needed) OR skill (if not) |

### Cluster merge targets
- **Error/Debug (18 skills)**: merge `error-debugging-*` + `error-diagnostics-*` (6 dup). Keep 1 of `error-analysis`, `error-trace`, `smart-debug`.
- **Review (16)**: merge `peer-review`+`peer-reviewer`+`peer-review-methodology` → 1. `code-review-*` (3) → 1. `comprehensive-review-*` (2) → 1.
- **TDD (6)**: `tdd-orchestrator`+`test-driven-development`+4×`tdd-workflows-tdd-*` → keep 1 orchestrator + cycle doc.
- **Migration (9)**: `framework-migration-*` (3) + `legacy-modernizer` + `dependency-upgrade` → 1 migration guide + 1 dep-upgrade.
- **DB migration (3)**: `database-migration` + `database-migrations-*` (2) → 1.
- **Context/ctx (10)**: 8 overlapping → keep 2 (save/restore + optimization).
- **FastAPI (3)**: `fastapi-developer`+`fastapi-pro`+`fastapi-templates` → 1.
- **Nextflow/Snakemake**: `*-pipelines` + `*-workflow-engine` → 1 each.
- **C4 (5)**: `c4-{code,component,container,context,architecture}` → 1 unified.
- **Variant calling (25)**: consolidar tooling-specific sob 1 guide + tool pages.
- **Docking (5)**: agent `docking-specialist` + skill `molecular-docking` suficientes; fundir tool pages.

## Files to delete (Phase 1 only, safe)
- `skills/anndata/`   (redundant with `anndata-data-structure`)
- `skills/scanpy-scrna-seq/`   (redundant with `scanpy`)
- `skills/scvi-tools/`   (redundant with `scvi-tools-single-cell`)
- `skills/pydeseq2-differential-expression/`   (redundant with `pydeseq2`)
- `skills/deseq2-differential-expression/`   (redundant with `deseq2-basics`)
- `skills/rnaseq-de/`   (redundant with `rnaseq-to-de`)
- `skills/featurecounts-counting/`   (redundant with `featurecounts-rna-counting`)
- `skills/pyopenms/`   (redundant with `pyopenms-mass-spectrometry`)
- `skills/rdkit-cheminformatics/`   (redundant with `rdkit`)
- `skills/molfeat-molecular-featurization/`   (redundant with `molfeat`)
- `skills/datamol-cheminformatics/`   (redundant with `datamol`)
- `skills/torch-geometric-graph-neural-networks/`   (redundant with `torch-geometric`)
- `skills/networkx-graph-analysis/`   (redundant with `networkx`)
- `skills/flowio-flow-cytometry/`   (redundant with `flowio`)
- `skills/adaptyv/`   (redundant with `adaptyv-bio`)
- `skills/dbsnp-queries/`   (redundant with `dbsnp-database`)
- `skills/clinvar-lookup/`   (redundant with `clinvar-database`)
- `skills/single-cell-annotation-guide/`   (redundant with `single-cell-annotation`)
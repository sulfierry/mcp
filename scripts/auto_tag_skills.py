#!/usr/bin/env python3
"""Auto-tag skills by inferring category from id + name + description + path.

Writes tags into skills_index.json. Use --apply-frontmatter to also patch
SKILL.md YAML blocks (destructive — make backup first).
"""
from __future__ import annotations
import argparse, json, re, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "skills_index.json"
SKILLS = ROOT / "skills"

# Ordered rules — first match wins. Keys checked against combined
# lowercase "id name description path".
RULES: list[tuple[str, list[str]]] = [
    ("single-cell",        ["scrna", "single-cell", "scanpy", "anndata", "scvi", "scvelo", "harmony", "celltypist", "popv", "doublet", "cellxgene", "muon", "mofaplus"]),
    ("spatial-omics",      ["spatial-", "cellchat", "scirpy", "perturb-seq", "stereo", "visium", "merfish"]),
    ("bulk-rnaseq",        ["rnaseq", "deseq", "edger", "pydeseq", "salmon", "star-rna", "tximport", "featurecounts", "hisat2", "rnaseq-de"]),
    ("variant-calling",    ["variant", "vcf", "gatk", "clair", "deepvariant", "bcftools-variant", "tiledbvcf", "snpeff"]),
    ("gwas",               ["gwas", "plink", "prs", "polygenic", "fine-mapping", "ld-", "linkage-diseq", "mendelian-rand"]),
    ("clinical-genomics",  ["clinvar", "clinical-variant", "pharmacogenomics", "clinpgx", "acmg", "pharmgx"]),
    ("cancer-genomics",    ["somatic", "tmb", "neoantigen", "tumor-", "cfdna", "ctdna", "dhdna", "liquid-biopsy", "cosmic", "onco", "hla-"]),
    ("methylation",        ["methylation", "bismark", "methylkit", "dmr", "cpg", "methylation-clock"]),
    ("chip-atac",          ["chipseq", "chip-seq", "atac", "macs3", "homer", "peak-call", "clip-"]),
    ("hic-3d",             ["hic-", "tad-", "compartment", "loop-call", "contact-pairs"]),
    ("long-read",          ["nanopore", "pacbio", "hifi", "long-read", "basecalling", "medaka", "isoseq", "m6anet"]),
    ("short-read-align",   ["bwa", "bowtie", "hisat", "alignment-", "pairwise-alignment", "multiple-alignment", "msa-"]),
    ("ngs-qc",             ["fastp", "fastqc", "fastq-", "trim", "adapter", "duplicate", "contamination", "busco"]),
    ("genome-annotation",  ["prokka", "genome-anno", "repeat-anno", "orf-", "eukaryotic-gene-pred", "functional-anno", "ncrna-"]),
    ("assembly",           ["assembly", "scaffolding", "polish", "finishing"]),
    ("phylogenetics",      ["phylo", "tree-", "ortholog", "synteny", "divergence", "ancestral", "species-tree", "msa-stat"]),
    ("microbiome",         ["microbiome", "metagenom", "metaphlan", "kraken", "amplicon", "qiime2", "edna-", "strain-"]),
    ("pathogen-surveill",  ["pathogen", "amr-", "outbreak", "variant-surveill", "transmission-inference"]),
    ("proteomics",         ["proteomics", "maxquant", "pyopenms", "dia-", "peptide-", "ptm-", "protein-inference", "msdial"]),
    ("mass-spec-metab",    ["metabolom", "xcms", "msdial", "matchms", "lipidomics"]),
    ("cheminformatics",    ["rdkit", "datamol", "molfeat", "descriptor", "featuriz", "smiles", "substructure", "fragment", "chembl", "pubchem", "zinc-database", "unichem"]),
    ("drug-discovery",     ["admet", "medchem", "sar-", "docking", "diffdock", "autodock", "virtual-screen", "target-", "drug-", "pharm-"]),
    ("structural-biology", ["alphafold", "esm", "pdb-", "emdb", "struct-predict", "structure-", "binding-site", "viennarna", "plannotate"]),
    ("mol-dynamics",       ["mdanalysis", "molecular-dynamics", "gromacs", "openmm"]),
    ("immunology",         ["mhc-", "hla-", "immunogen", "epitope", "tcr-", "immcantation", "vdjtools", "scirpy", "repertoire"]),
    ("crispr",              ["crispr", "sgrna", "grna", "crispresso", "mageck", "jacks", "base-editing", "prime-editing", "hdr-"]),
    ("bio-database",       ["ensembl", "uniprot", "entrez", "ncbi", "pubmed", "biorxiv", "openalex", "depmap", "opentargets", "dbsnp", "gnomad", "reactome", "kegg", "interpro", "string-database", "brenda", "pride", "hmdb", "drugbank", "gtopdb", "dailymed", "fda", "ddinter", "archs4", "geo-database", "cbioportal", "clinicaltrials"]),
    ("imaging",            ["napari", "cellpose", "histolab", "image-", "opencv", "pydicom", "nnunet", "segment", "imc-", "pathml", "pyimagej", "omero", "trackpy", "simpleitk"]),
    ("flow-cytometry",     ["flowio", "fcs-", "cytometry", "gating", "compensation"]),
    ("ml-framework",       ["pytorch", "torch-", "sklearn", "scikit-", "transformers", "pymc", "stable-baselines", "lightning", "bayesian", "xgboost", "umap", "shap", "pytdc", "genetic-algorithms", "multi-objective-optimization", "pymoo", "pufferlib", "qiskit", "cirq", "qutip", "pennylane", "model-curation", "model-validation"]),
    ("deep-learning-bio",  ["deepchem", "torchdrug", "esm-", "scvi-", "cellpose", "nnunet", "alphafold", "diffdock"]),
    ("statistics",         ["statsmodels", "pymc", "survival", "scikit-survival", "logistic", "multiple-testing", "sample-size", "power-", "mediation", "bayesian-inference", "effect-measures", "correlation"]),
    ("visualization-scientific", ["matplotlib", "seaborn", "plotly", "ggplot", "heatmap", "volcano", "sashimi", "circos", "upset", "ideogram", "genome-track", "deeptools", "igv", "mermaid-expert", "infograph", "scientific-schem", "color-palette", "pnas-", "nejm-", "nature-", "cell-figure", "elife-", "lancet-", "latex-poster"]),
    ("workflow-engine",    ["nextflow", "snakemake", "wdl", "cwl", "airflow"]),
    ("pipeline-bio",       ["-pipeline"]),
    ("notebook-writing",   ["jupyter-", "quarto", "rmarkdown", "obsidian", "markdown-"]),
    ("scientific-writing", ["academic-paper", "thesis", "manuscript", "latex-", "peer-review", "citation", "research-grant", "grant-proposal", "scientific-paper", "scientific-manuscript", "paperzilla", "paper-lookup", "pubmed-sum", "literature-review"]),
    ("research-methods",   ["hypothes", "hypogenic", "deep-research", "socratic", "brainstorm", "scientific-method", "peer-review-method"]),
    ("frontend",           ["react-", "nextjs", "vue", "svelte", "angular", "tailwind", "ui-", "ux-", "frontend", "web-design", "mobile-develop", "ios-", "react-native", "flutter", "godot", "unity"]),
    ("backend-api",        ["fastapi", "django", "flask", "nodejs", "graphql-arch", "api-design", "api-document"]),
    ("langs",              ["python-pro", "python-arch", "python-perform", "async-python", "bash-", "posix-shell", "golang-pro", "go-concur", "rust-pro", "rust-async", "rust-engineer", "cpp-pro", "c-pro", "c-systems", "csharp-", "dotnet-", "java-pro", "scala-", "ruby-pro", "elixir-", "php-", "julia-", "haskell-", "matlab", "minecraft-bukkit", "typescript-", "javascript-pro", "modern-javascript", "embedded-c", "arm-cortex", "network-programming-c", "memory-safety-patterns", "compiler-internals", "gpu-cuda", "numerical-methods", "applied-mathematics", "interval-arithmetic", "python-packaging", "uv-package-manager"]),
    ("databases",          ["postgres", "supabase", "sql-", "sqlalch", "bigquery", "vector-", "database-arch", "database-admin", "database-mig", "database-optim", "polars", "dask", "vaex", "zarr"]),
    ("devops-infra",       ["docker", "kubernetes", "k8s-", "terraform", "helm-", "istio", "linkerd", "mesh", "bazel", "nx-", "turborepo", "gitops", "github-actions", "gitlab-", "ci-cd", "cicd", "prometheus", "grafana", "observability", "slo-", "sre-", "cloud-arch", "multi-cloud", "hybrid-cloud", "deployment", "monorepo", "serverless", "conductor-", "saga-", "cost-optimization", "hpc-engineer", "network-engineer", "systems-engineer", "devops-troubleshooter", "on-call-handoff", "incident-runbook", "postmortem-writing", "event-store-design"]),
    ("security",           ["security", "threat", "stride", "attack-tree", "pci", "gdpr", "hipaa", "sast", "malware", "reverse-engineer", "binary-", "firmware", "memory-forensic", "mtls", "auth-", "wcag", "pentest", "compliance", "secret", "backend-security", "frontend-security", "mobile-security"]),
    ("testing",            ["tdd-", "test-driven", "testing-", "test-generate", "webapp-test", "e2e-test", "performance-test", "javascript-test", "python-test", "bats-test", "test-automator", "qa-expert", "web3-testing", "coverage-analysis"]),
    ("debug-error",        ["debug", "error-", "incident-response", "incident-respond", "debugger", "systematic-debug", "low-level-debug"]),
    ("refactoring",        ["refactor", "legacy-modern", "framework-mig", "dependency-upgrade", "codebase-cleanup", "simplif", "tech-debt"]),
    ("code-review",        ["code-review", "code-reviewer", "receiving-code-review", "requesting-code-review", "comprehensive-review", "peer-review-code"]),
    ("architecture",       ["architect", "c4-", "domain-driv", "event-sourcing", "cqrs", "saga-orchestr", "microservice", "monorepo-arch", "architecture-decision", "architecture-pattern"]),
    ("agent-orchestration",["agent-orchestr", "multi-agent", "orchestrator", "planning-", "executing-plan", "task-", "dispatching-parallel"]),
    ("llm-rag",            ["llm-", "rag-", "prompt-engineer", "embedding", "hybrid-search", "mcp-", "claude-api", "langchain"]),
    ("seo",                ["seo-"]),
    ("finance-business",   ["finance", "equity", "quant-", "backtest", "kpi-", "startup-", "billing", "payment", "stripe", "paypal", "market-", "risk-metric", "employment-", "legal-"]),
    ("ops-analytics",      ["dx-optim", "data-engineer", "data-scientist", "data-pipeline", "data-quality", "data-preproc", "data-import", "data-storytell", "exploratory-data", "profile-report", "mlops", "ml-pipeline", "ml-engineer", "llm-architect"]),
    ("context-mgmt",       ["context-", "ctx-"]),
    ("claude-tooling",     ["claude-", "mcp-builder", "mcp-develop", "skill-creator", "tool-design", "hosted-agents", "subagent-", "using-superpowers", "filesystem-context", "memory-systems", "consciousness-council", "full-stack-orchestration"]),
    ("git-workflow",       ["git-", "gitops-", "github-", "gitlab-", "changelog"]),
    ("cli-tools",          ["bash-", "posix-shell", "shellcheck", "markitdown", "defuddle"]),
    ("design-diagrams",    ["mermaid", "c4-", "diagram", "canvas", "infograph", "json-canvas", "brand-", "theme-factory", "web-artifact", "graphify"]),
]

DEFAULT_CAT = "misc"

_WORD_BOUNDARY = re.compile(r"[a-z0-9]+")

def _has_token(blob_tokens: set[str], key: str) -> bool:
    """Match key against blob_tokens using word boundaries.

    Blob tokens are produced by splitting on non-alphanumeric characters, so
    every token is already a self-contained word. Keys are normalized the
    same way and must match as exact tokens. Trailing `-`/`_` in a key is
    just a stylistic hint from the rule table and is stripped.
    """
    # Normalize key: drop trailing separators, split into parts
    clean = key.rstrip("-_ ")
    parts = [p for p in re.split(r"[-_ ]+", clean) if p]
    if not parts:
        return False
    # All parts must appear as exact tokens
    return all(p in blob_tokens for p in parts)


def classify(s: dict) -> str:
    # Classify on id+name+path only. Descriptions are prose and produce
    # spurious matches (e.g. a biology skill mentioning "testing methods"
    # would land in `testing`). id/name/path are terser and domain-scoped.
    blob = f"{s.get('id','')} {s.get('name','')} {s.get('path','')}".lower()
    tokens = set(_WORD_BOUNDARY.findall(blob))
    for cat, keys in RULES:
        if any(_has_token(tokens, k) for k in keys):
            return cat
    return DEFAULT_CAT

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--apply-frontmatter", action="store_true", help="Rewrite SKILL.md YAML blocks (destructive; makes backup)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    data = json.loads(INDEX.read_text())
    from collections import Counter
    before = Counter(s.get("category") or "" for s in data)
    after = Counter()
    changes = 0
    for s in data:
        new = classify(s)
        if s.get("category") != new:
            changes += 1
        s["category"] = new
        after[new] += 1

    print(f"Total skills: {len(data)}")
    print(f"Changes: {changes}")
    print("\nCategory distribution (new):")
    for c, n in after.most_common():
        print(f"  {n:4d}  {c}")

    if args.dry_run:
        print("\nDRY-RUN — no writes")
        return

    # Backup + write index
    shutil.copy(INDEX, INDEX.with_suffix(".json.bak"))
    INDEX.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"\nIndex updated: {INDEX}  (backup: {INDEX}.bak)")

    if args.apply_frontmatter:
        patched = 0
        for s in data:
            skill_md = SKILLS / s["path"]
            if not skill_md.is_file():
                continue
            txt = skill_md.read_text(encoding="utf-8", errors="ignore")
            m = re.match(r"^(---\s*\n)(.*?)(\n---\s*\n)", txt, re.S)
            if not m:
                continue
            fm = m.group(2)
            if re.search(r"^category:\s*\S+", fm, re.M):
                new_fm = re.sub(r"^category:\s*.*$", f"category: {s['category']}", fm, count=1, flags=re.M)
            else:
                new_fm = fm.rstrip() + f"\ncategory: {s['category']}"
            if new_fm != fm:
                skill_md.write_text(m.group(1) + new_fm + m.group(3) + txt[m.end():], encoding="utf-8")
                patched += 1
        print(f"SKILL.md patched: {patched}")

if __name__ == "__main__":
    main()

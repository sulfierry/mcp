---
name: Literature Review
description: "Expert skill for systematic literature search, PubMed/arXiv/Semantic Scholar queries, PRISMA-compliant reviews, citation graph analysis, and research gap identification for scientific papers and theses."
category: scientific-writing
tags: literature, review, pubmed, arxiv, systematic-review, prisma, citations, search, bibliography, research
source: custom
---

# Literature Review

## Use this skill when

- Conducting systematic literature searches across PubMed, arXiv, Semantic Scholar
- Writing literature review sections for papers, theses, or grant proposals
- Performing PRISMA-compliant systematic reviews
- Identifying research gaps and positioning your work
- Building citation networks and analyzing citation patterns
- Generating BibTeX bibliographies from search results
- Summarizing and synthesizing findings across multiple papers
- Fact-checking claims against published literature

## Instructions

### Search Strategy

```
1. DEFINE    → Formulate PICO/PEO research question
2. SEARCH    → Query databases with Boolean operators
3. SCREEN    → Title/abstract screening with inclusion/exclusion criteria
4. EXTRACT   → Full-text data extraction into structured table
5. SYNTHESIZE → Identify themes, gaps, and consensus
6. WRITE     → Narrative or thematic synthesis
```

### Database Query Patterns

#### PubMed (Biomedical)
```python
from Bio import Entrez

Entrez.email = "your@email.com"

def search_pubmed(query: str, max_results: int = 100):
    """Search PubMed with structured query."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, 
                            sort="relevance", datetype="pdat", 
                            mindate="2020", maxdate="2026")
    results = Entrez.read(handle)
    ids = results["IdList"]
    
    # Fetch abstracts
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="xml")
    records = Entrez.read(handle)
    
    papers = []
    for article in records["PubmedArticle"]:
        medline = article["MedlineCitation"]
        papers.append({
            "pmid": str(medline["PMID"]),
            "title": medline["Article"]["ArticleTitle"],
            "journal": medline["Article"]["Journal"]["Title"],
            "year": medline["Article"]["Journal"]["JournalIssue"]["PubDate"].get("Year", ""),
            "abstract": medline["Article"].get("Abstract", {}).get("AbstractText", [""])[0],
        })
    return papers

# Example: drug-target interaction papers
results = search_pubmed(
    '("drug target interaction"[Title/Abstract] OR "DTI prediction"[Title/Abstract]) '
    'AND ("deep learning"[Title/Abstract] OR "neural network"[Title/Abstract]) '
    'AND "kinase"[Title/Abstract] '
    'AND 2020:2026[dp]'
)
```

#### arXiv (CS/ML/Physics)
```python
import arxiv

def search_arxiv(query: str, max_results: int = 50):
    """Search arXiv with sorting by relevance."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    return [{
        "title": r.title,
        "authors": [a.name for a in r.authors],
        "abstract": r.summary,
        "url": r.entry_id,
        "published": r.published.strftime("%Y-%m-%d"),
        "categories": r.categories,
    } for r in search.results()]
```

#### Semantic Scholar (Cross-domain)
```python
import requests

def search_semantic_scholar(query: str, limit: int = 50, year: str = "2020-"):
    """Search Semantic Scholar with citation counts."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "year": year,
        "fields": "title,authors,abstract,year,citationCount,journal,url",
    }
    resp = requests.get(url, params=params)
    return resp.json().get("data", [])
```

### PRISMA Workflow

```
Identification:   Database search → n records
                  Other sources → n records
                          ↓
Screening:        Remove duplicates → n unique
                  Title/abstract screen → n excluded (with reasons)
                          ↓
Eligibility:      Full-text assessment → n excluded (with reasons)
                          ↓
Included:         Qualitative synthesis → n studies
                  Quantitative synthesis (meta-analysis) → n studies
```

### Writing the Review

#### Thematic Organization (Preferred)
```
1. Overview paragraph: scope, search strategy, n papers found
2. Theme 1: [e.g., "Sequence-based DTI methods"]
   - Chronological development
   - Key methods and results
   - Limitations
3. Theme 2: [e.g., "Structure-based approaches"]
   - ...
4. Theme 3: [e.g., "Graph neural network methods"]
   - ...
5. Synthesis: convergent findings, open questions
6. Research gap: what your work addresses
```

#### Comparison Table Template
```markdown
| Method | Year | Input Features | Architecture | Dataset | Performance |
|--------|------|---------------|--------------|---------|-------------|
| DeepDTA | 2018 | SMILES + protein seq | CNN | Davis, KIBA | CI=0.878 |
| GraphDTA | 2020 | Molecular graph + seq | GCN+CNN | Davis, KIBA | CI=0.884 |
| DrugBAN | 2022 | Molecular graph + protein | Bilinear attention | BindingDB | AUROC=0.87 |
| DT-Kinase | 2026 | ESM-2 + MolBERT embeddings | Adapted CNN | Kinase-specific | MCC=0.52 |
```

### BibTeX Generation

```python
def format_bibtex(paper: dict) -> str:
    """Generate BibTeX entry from paper metadata."""
    author = paper.get("authors", "Unknown")
    if isinstance(author, list):
        author = " and ".join(author[:3])
        if len(paper.get("authors", [])) > 3:
            author += " and others"
    
    key = f"{author.split()[0].lower()}{paper.get('year', 'nd')}"
    
    return f"""@article{{{key},
  title={{{paper.get('title', '')}}},
  author={{{author}}},
  journal={{{paper.get('journal', '')}}},
  year={{{paper.get('year', '')}}},
  doi={{{paper.get('doi', '')}}}
}}"""
```

### Quality Assessment

For each included paper, assess:
- **Study design**: RCT > cohort > case-control > cross-sectional
- **Sample size**: Adequate statistical power?
- **Methodology**: Reproducible? Code/data available?
- **Bias risk**: Selection, reporting, confirmation bias
- **Relevance**: Directly addresses your research question?

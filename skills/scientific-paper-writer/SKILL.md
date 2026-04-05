---
name: Scientific Paper Writer
description: "Expert skill for writing publication-ready scientific papers with IMRaD structure, LaTeX output, data integration, citation management, and journal-specific formatting (Nature, Science, NeurIPS, IEEE, APA 7)."
category: scientific-writing
tags: paper, manuscript, imrad, latex, writing, nature, science, neurips, ieee, apa, academic, publication
source: custom
---

# Scientific Paper Writer

## Use this skill when

- Writing a new scientific paper from scratch with IMRaD structure
- Converting research results, data files, and figures into a manuscript
- Formatting papers for specific journals (Nature, Science, NeurIPS, IEEE, APA 7)
- Drafting individual sections (Abstract, Introduction, Methods, Results, Discussion)
- Converting between citation formats (APA ↔ IEEE ↔ Chicago ↔ Vancouver)
- Writing bilingual abstracts (English + Portuguese or other languages)
- Polishing scientific prose for clarity, conciseness, and academic tone

## Do not use this skill when

- Doing literature search or systematic review (use `literature-review` skill)
- Peer reviewing an existing manuscript (use `peer-reviewer` skill)
- Working on a thesis chapter (use `thesis-writer` skill)
- Formatting LaTeX compilation issues only (use `latex-manuscript` skill)

## Instructions

### Writing Workflow

```
1. OUTLINE  → Structure the paper: sections, key arguments, figure placement
2. DRAFT    → Write each section with proper academic conventions
3. CITE     → Add and format references (BibTeX)
4. FIGURES  → Integrate data files and figure references
5. POLISH   → Improve clarity, remove redundancy, strengthen transitions
6. FORMAT   → Apply journal-specific style (Nature, IEEE, etc.)
```

### Paper Structure (IMRaD)

When writing a scientific paper, always follow this structure unless the journal specifies otherwise:

```latex
\begin{document}

\title{Descriptive Title: Key Finding or Method (≤15 words)}
\author{Authors with affiliations}
\date{}
\maketitle

\begin{abstract}
% 150-300 words. Structure: Background → Gap → Approach → Results → Conclusion
\end{abstract}

\section{Introduction}
% Funnel structure: Broad context → Specific problem → Knowledge gap → 
% "Here we show..." → Brief approach → Key contributions (numbered list)

\section{Methods}  % or Materials and Methods
% Reproducible detail level. Subsections for each technique.
% Include: datasets, preprocessing, model architecture, training protocol,
% evaluation metrics, statistical tests, software versions

\section{Results}
% Present findings without interpretation. Each paragraph ties to a figure.
% Use: "Figure 1 shows...", "Table 2 summarizes..."
% Statistical reporting: metric (95% CI [lower, upper], p < threshold)

\section{Discussion}
% Interpretation → Comparison with literature → Limitations → Future work
% Never introduce new data in Discussion

\section{Conclusion}
% 1 paragraph. Restate key finding + broader impact. No speculation.

\end{document}
```

### Section-by-Section Writing Guide

#### Abstract (~250 words)
```
Sentence 1-2: Background context and significance
Sentence 3:   Knowledge gap ("However, ... remains unknown")
Sentence 4:   "Here, we present/show/demonstrate..."
Sentence 5-6: Key methods summary
Sentence 7-8: Principal results with numbers
Sentence 9:   Conclusion and broader implications
```

#### Introduction (3-5 paragraphs)
```
Para 1: Broad field context, why this matters
Para 2: Narrow to specific problem, prior work
Para 3: Knowledge gap, what's missing
Para 4: "In this work, we..." — your approach
Para 5: Contributions list (numbered)
```

#### Methods
Always include these subsections for computational papers:
- **Data Collection & Preprocessing**: Dataset source, size, splits, cleaning
- **Model Architecture**: Layer-by-layer description with dimensions
- **Training Protocol**: Optimizer, LR schedule, batch size, epochs, hardware
- **Evaluation Metrics**: MCC, AUROC, AUPRC, with threshold selection method
- **Statistical Analysis**: Tests used, significance level, multiple comparison correction
- **Software & Reproducibility**: Package versions, random seeds, code availability

#### Results
```
Each result paragraph:
1. One-sentence topic: what this analysis shows
2. Setup: what was compared/measured
3. Finding: "We observed..." with exact numbers
4. Figure reference: "(Figure X, Table Y)"
5. Statistical support: "p < 0.001, 95% CI [a, b]"
```

#### Discussion
```
Para 1: Restate main finding in broader context
Para 2-3: Compare with prior work (agreement/disagreement)
Para 4: Limitations (be honest and specific)
Para 5: Future directions
Para 6: Concluding statement
```

### Journal-Specific Formatting

| Journal | Style | Word Limit | Refs | Figures |
|---------|-------|-----------|------|---------|
| Nature | `nature` | 3000 (Article) | ~50 | 6-8 |
| Science | `science` | 2500 | ~40 | 4 |
| NeurIPS | `neurips_2024` | 9 pages | unlimited | inline |
| IEEE | `IEEEtran` | 8-10 pages | ~30 | inline |
| APA 7 | `apa7` | varies | unlimited | end |
| Bioinformatics | `bioinfo` | 7 pages | ~50 | 5-7 |

### LaTeX Templates

```latex
% Nature Article
\documentclass{nature}
\bibliographystyle{naturemag}

% NeurIPS
\documentclass{article}
\usepackage{neurips_2024}
\bibliographystyle{unsrtnat}

% IEEE
\documentclass[conference]{IEEEtran}
\bibliographystyle{IEEEtran}

% APA 7
\documentclass[man,12pt]{apa7}
\bibliographystyle{apacite}
```

### Citation Best Practices

```bibtex
% Always include: author, title, journal, year, volume, pages, doi
@article{vaswani2017attention,
  title={Attention is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and others},
  journal={Advances in Neural Information Processing Systems},
  volume={30},
  year={2017},
  doi={10.48550/arXiv.1706.03762}
}
```

**Citation rules**:
- Every factual claim needs a citation (except your own results)
- Cite primary sources, not reviews (unless reviewing the field)
- Use "et al." for 3+ authors in text (APA: 3+; IEEE: depends)
- Self-citations: ≤10% of total references
- Cite recent work (last 5 years for 50%+ of refs)

### Writing Quality Checklist

- [ ] No first person in Methods/Results (use passive voice)
- [ ] No vague claims ("significant improvement" → "12.3% improvement")
- [ ] All figures/tables referenced in text
- [ ] All abbreviations defined on first use
- [ ] Consistent notation throughout
- [ ] Numbers: spell out 1-9, digits for 10+
- [ ] No orphan paragraphs (every section has ≥2 paragraphs)
- [ ] Conclusion doesn't introduce new information
- [ ] Data availability statement included
- [ ] Code availability statement included

### Common Pitfalls

| Issue | Wrong | Correct |
|-------|-------|---------|
| Vague quantifier | "significantly better" | "12.3% higher MCC (p=0.003)" |
| Missing comparison | "Our model achieves 0.85" | "Our model achieves 0.85 vs. 0.72 baseline" |
| Overclaiming | "This proves that..." | "These results suggest that..." |
| Passive voice abuse | "It was observed that..." | "We observed..." (Introduction/Discussion OK) |
| Citation needed | "Kinases are important..." | "Kinases play central roles in... [1-3]" |

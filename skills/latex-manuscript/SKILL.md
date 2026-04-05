---
name: LaTeX Manuscript
description: "Expert skill for LaTeX scientific document compilation, versioning, diff generation, BibTeX/Biber bibliography management, and troubleshooting. Covers manuscript preparation, figure management, and publisher submission requirements."
category: scientific-writing
tags: latex, bibtex, biber, compilation, manuscript, typesetting, pdf, figures, tables, academic
source: custom
---

# LaTeX Manuscript

## Use this skill when

- Compiling LaTeX manuscripts to PDF
- Managing BibTeX/Biber bibliographies
- Creating publication-quality figures and tables in LaTeX
- Troubleshooting LaTeX compilation errors
- Generating diffs between manuscript versions (latexdiff)
- Preparing camera-ready submissions for conferences/journals
- Converting between document formats (Markdown ↔ LaTeX)

## Instructions

### Compilation Pipeline

```bash
# Standard compilation (pdflatex + bibtex)
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Modern compilation (lualatex + biber) — recommended
lualatex main.tex
biber main
lualatex main.tex
lualatex main.tex

# One-command with latexmk (watches for changes)
latexmk -pdf main.tex           # pdflatex
latexmk -lualatex main.tex      # lualatex
latexmk -pvc main.tex           # continuous preview

# Tectonic (Rust-based, auto-downloads packages)
tectonic main.tex
```

### Figure Best Practices

```latex
\usepackage{graphicx}
\usepackage{subcaption}

% Single figure
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/contact_map.pdf}
  \caption{Contact map of EGFR kinase domain (PDB: 1M17) at 8\AA{} 
           threshold. Dark pixels indicate residue pairs within contact 
           distance.}
  \label{fig:contact-map}
\end{figure}

% Multi-panel figure
\begin{figure}[htbp]
  \centering
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{figures/roc_curve.pdf}
    \caption{ROC curve (AUROC = 0.87)}
    \label{fig:roc}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\textwidth}
    \includegraphics[width=\textwidth]{figures/pr_curve.pdf}
    \caption{Precision-Recall curve (AUPRC = 0.82)}
    \label{fig:pr}
  \end{subfigure}
  \caption{Classification performance of DT-Kinase Level 4 CNN on the 
           test set. (a)~ROC curve showing AUROC of 0.87. 
           (b)~Precision-Recall curve showing AUPRC of 0.82.}
  \label{fig:performance}
\end{figure}
```

### Table Best Practices

```latex
\usepackage{booktabs}
\usepackage{siunitx}

\begin{table}[htbp]
  \centering
  \caption{Comparison of DTI prediction methods on the kinase benchmark 
           dataset. Best results in \textbf{bold}. $\pm$ denotes standard 
           deviation over 5 random seeds.}
  \label{tab:comparison}
  \begin{tabular}{lccc}
    \toprule
    Method & MCC & AUROC & AUPRC \\
    \midrule
    DeepDTA (2018)      & 0.38 $\pm$ 0.03 & 0.79 $\pm$ 0.02 & 0.74 \\
    GraphDTA (2020)     & 0.41 $\pm$ 0.02 & 0.81 $\pm$ 0.01 & 0.76 \\
    DrugBAN (2022)      & 0.45 $\pm$ 0.02 & 0.82 $\pm$ 0.01 & 0.78 \\
    \midrule
    DT-Kinase L4 (Ours) & \textbf{0.52 $\pm$ 0.02} & \textbf{0.87 $\pm$ 0.01} & \textbf{0.82} \\
    \bottomrule
  \end{tabular}
\end{table}
```

### Version Control & Diff

```bash
# Generate diff between two versions
latexdiff v1/main.tex v2/main.tex > diff.tex
pdflatex diff.tex

# Git-based diff
latexdiff-vc --git --flatten -r HEAD~1 main.tex
```

### Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Undefined control sequence` | Missing `\usepackage{}` | Add the required package |
| `Missing $ inserted` | Math symbol outside math mode | Wrap in `$...$` |
| `Float too large` | Image wider than `\textwidth` | Reduce `width=` parameter |
| `Citation undefined` | Missing bibtex run | Run `bibtex main` then `pdflatex` twice |
| `I can't find file` | Wrong path | Check `\graphicspath{{figures/}}` |
| `Dimension too large` | Recursive include | Check for circular `\input` |

### Camera-Ready Checklist

- [ ] All fonts embedded (`pdffonts main.pdf` — no Type 3)
- [ ] Figures are vector (PDF/EPS) not raster (PNG/JPG) where possible
- [ ] References complete (no "?" in output)
- [ ] Page count within limit
- [ ] Author information matches submission system
- [ ] Supplementary material in separate PDF
- [ ] High-resolution figures (≥300 DPI for raster)

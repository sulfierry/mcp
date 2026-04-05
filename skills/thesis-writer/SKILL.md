---
name: Thesis Writer
description: "Expert skill for writing PhD/MSc thesis chapters, dissertations, and academic monographs. Covers chapter structure, argument flow, committee expectations, defense preparation, and LaTeX thesis templates."
category: scientific-writing
tags: thesis, dissertation, phd, masters, academic-writing, chapters, defense, latex
source: custom
---

# Thesis Writer

## Use this skill when

- Writing a PhD or Master's thesis chapter
- Structuring a dissertation from scratch
- Converting published papers into thesis chapters
- Writing the thesis Introduction and general Discussion/Conclusion chapters
- Preparing for thesis defense (anticipated questions, presentation slides)
- Formatting a thesis in LaTeX (university template)

## Instructions

### Thesis Structure

```
FRONT MATTER
├── Title page
├── Abstract (English + Portuguese)
├── Acknowledgments
├── Table of Contents
├── List of Figures / Tables / Abbreviations
│
BODY
├── Chapter 1: Introduction & Literature Review
│   ├── 1.1 Context and motivation
│   ├── 1.2 State of the art (lit review)
│   ├── 1.3 Research gap
│   ├── 1.4 Objectives and contributions
│   └── 1.5 Thesis outline
│
├── Chapter 2: Theoretical Background
│   ├── 2.1 Domain fundamentals
│   ├── 2.2 Methods and techniques
│   └── 2.3 Mathematical framework
│
├── Chapter 3-N: Research Contributions
│   ├── (One chapter per published/submitted paper)
│   ├── Connecting paragraph at start
│   ├── Paper content (expanded)
│   └── Supplementary material
│
├── Chapter N+1: General Discussion
│   ├── Summary of contributions
│   ├── Cross-chapter synthesis
│   ├── Limitations
│   └── Future work
│
└── Chapter N+2: Conclusion
    ├── Thesis summary (1 paragraph per chapter)
    └── Final remarks

BACK MATTER
├── Bibliography (unified)
├── Appendices (code, supplementary data)
└── Curriculum Vitae (optional)
```

### Chapter Writing Guidelines

#### Chapter 1: Introduction (~20-30 pages)
```
Goal: Set the stage for the entire thesis

Opening (1-2 pages): 
  - Start with a compelling hook (real-world problem)
  - Establish significance of the field
  
Literature Review (10-15 pages):
  - Organize thematically, NOT chronologically
  - Show evolution of ideas leading to your gap
  - Use comparison tables for related work
  
Research Gap (1-2 pages):
  - Explicitly state what is missing
  - Connect the gap to your objectives
  
Objectives (1 page):
  - General objective (1 sentence)
  - Specific objectives (numbered list, 3-5 items)
  - Map each objective to a thesis chapter
  
Thesis Outline (1 page):
  - 1 paragraph per chapter describing content
```

#### Paper-as-Chapter Conversion
```
When incorporating a published paper as a thesis chapter:

1. Add a "Chapter Preamble" (1/2 page):
   - "This chapter is based on: [full citation]"
   - "Author contributions: [your role]"
   - "Connection to previous chapter: [bridge paragraph]"

2. Expand the paper:
   - More detailed Methods (no page limit)
   - Additional results that didn't fit the paper
   - Extended discussion tying to thesis narrative

3. Unify notation:
   - Consistent symbols across all chapters
   - Notation table in front matter
   - Cross-references to other chapters
```

### LaTeX Thesis Template

```latex
\documentclass[12pt, a4paper, twoside]{report}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{amsmath, amssymb}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage[style=numeric-comp, backend=biber]{biblatex}
\addbibresource{references.bib}

% Margins (check university requirements)
\usepackage[top=3cm, bottom=2cm, left=3cm, right=2cm]{geometry}
\usepackage{setspace}
\onehalfspacing

\begin{document}

\input{chapters/00-titlepage}
\input{chapters/01-abstract}
\input{chapters/02-acknowledgments}

\tableofcontents
\listoffigures
\listoftables

\input{chapters/03-introduction}
\input{chapters/04-background}
\input{chapters/05-contribution1}
\input{chapters/06-contribution2}
\input{chapters/07-contribution3}
\input{chapters/08-discussion}
\input{chapters/09-conclusion}

\printbibliography

\appendix
\input{chapters/appendix-a}

\end{document}
```

### Defense Preparation

```
Anticipated Questions (prepare answers for):

METHODOLOGY:
- "Why did you choose this method over [alternative]?"
- "What assumptions does your model make?"
- "How would your results change with different hyperparameters?"

RESULTS:
- "Is this improvement statistically significant?"
- "Why does your model fail on [edge case]?"
- "How do you explain the discrepancy with [related work]?"

CONTRIBUTION:
- "What is the main takeaway of your thesis?"
- "How does this advance the state of the art?"
- "What would you do differently if starting over?"

FUTURE WORK:
- "What is the most impactful next step?"
- "Could this approach generalize to [other domain]?"
- "What are the practical applications?"
```

### Writing Quality for Thesis

- **Consistency**: Same terminology throughout (create a glossary)
- **Narrative flow**: Each chapter starts with a bridge to the previous one
- **Self-contained chapters**: Each chapter has its own introduction and conclusion
- **Visual aids**: ≥1 figure per 3 pages of text
- **Notation table**: Centralized in front matter
- **Cross-references**: Use `\ref{}` and `\pageref{}` extensively

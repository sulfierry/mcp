---
name: Peer Reviewer
description: "Expert skill for systematic peer review of scientific manuscripts. Implements multi-perspective review with quantitative scoring rubrics, structural analysis, statistical verification, and constructive revision suggestions."
category: scientific-writing
tags: peer-review, manuscript, review, revision, evaluation, academic, quality, scientific
source: custom
---

# Peer Reviewer

## Use this skill when

- Reviewing a manuscript before journal submission (self-review)
- Conducting formal peer review as a reviewer
- Evaluating statistical claims and methodology
- Providing structured feedback with actionable revision suggestions
- Assessing a manuscript against journal acceptance criteria
- Reviewing a thesis chapter or dissertation draft

## Instructions

### Review Framework (8 Dimensions)

Score each dimension 0-100:

| Dimension | Weight | What to Evaluate |
|-----------|--------|-------------------|
| **Novelty** | 15% | Is this new? How does it advance the field? |
| **Significance** | 15% | Does it matter? Would the field change without it? |
| **Soundness** | 20% | Are methods correct? Statistics valid? Conclusions supported? |
| **Clarity** | 15% | Is it well-written? Can you follow the logic? |
| **Reproducibility** | 10% | Could you replicate this? Code/data available? |
| **Completeness** | 10% | Are comparisons adequate? Missing experiments? |
| **Presentation** | 10% | Figures clear? Tables readable? Consistent notation? |
| **Ethics** | 5% | Proper citations? No plagiarism? Data integrity? |

**Overall Score**: Weighted average → Decision mapping:
- 80-100: Accept / Accept with minor revisions
- 60-79: Major revisions required
- 40-59: Reject and resubmit
- 0-39: Reject

### Review Structure

```markdown
## Summary
[2-3 sentences: what the paper does and its main contribution]

## Strengths
1. [Specific strength with evidence from the paper]
2. [...]
3. [...]

## Weaknesses
1. [Major] [Specific issue with suggestion for improvement]
2. [Major] [...]
3. [Minor] [...]

## Detailed Comments
### Introduction
- [Line-specific comment]

### Methods
- [Methodological concern]
- [Missing detail]

### Results
- [Statistical issue]
- [Missing comparison]

### Discussion
- [Overclaiming]
- [Missing limitation]

## Questions for Authors
1. [Clarifying question]
2. [Request for additional analysis]

## Scores
| Dimension | Score | Justification |
|-----------|-------|---------------|
| Novelty | XX/100 | [Brief reason] |
| ... | ... | ... |
| **Overall** | **XX/100** | **[Decision]** |

## Recommendation
[ ] Accept
[ ] Minor revisions
[ ] Major revisions
[ ] Reject and resubmit
[ ] Reject
```

### Statistical Verification Checklist

- [ ] Sample sizes reported for all experiments
- [ ] Appropriate statistical tests used (parametric vs. non-parametric)
- [ ] Multiple comparison correction applied (Bonferroni, FDR)
- [ ] Effect sizes reported (not just p-values)
- [ ] Confidence intervals provided
- [ ] Random seeds reported for reproducibility
- [ ] Cross-validation strategy appropriate (no data leakage)
- [ ] Train/validation/test splits clearly described
- [ ] Baseline comparisons are fair (same data, same preprocessing)

### Common Red Flags

| Red Flag | Where to Check | Action |
|----------|---------------|--------|
| Cherry-picked metrics | Results tables | Request all standard metrics |
| Missing error bars | Figures | Request confidence intervals |
| Unfair baselines | Methods/Results | Request re-running with same data |
| P-hacking | Methods | Check multiple comparison correction |
| Data leakage | Methods | Verify train/test separation |
| Overclaiming | Abstract/Discussion | Suggest hedging language |
| Missing ablations | Results | Request component analysis |
| No code/data | Methods | Request availability statement |

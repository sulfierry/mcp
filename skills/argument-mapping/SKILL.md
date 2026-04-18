---
name: argument-mapping
description: "Close-reading and argument analysis at PhD level. Toulmin model, argument diagrams, steel-manning, counterargument generation, fallacy detection, Rapoport rules, dialectical analysis. For literature critique, paper review, thesis defense prep, discussion-section writing. Triggers on argument analysis, critical reading, steel-manning, counterargument, dialectic, close reading, argument structure."
category: scientific-writing
tags: [argument, critical-thinking, toulmin, steel-manning, phd]
---

# Argument Mapping & Close Reading

## When to use
- Critiquing a paper (review or journal club)
- Drafting Discussion / Limitations section
- Defense prep — anticipate examiner objections
- Literature review — distinguishing assertion from evidence
- Writing response to reviewers

## Toulmin model (core)

Every argument decomposes into:

- **Claim** (C): what's asserted
- **Data** (D): evidence presented
- **Warrant** (W): inference rule connecting D → C
- **Backing** (B): support for the warrant
- **Qualifier** (Q): strength/confidence marker ("probably", "in most cases")
- **Rebuttal** (R): conditions under which claim fails

Example paper claim:
> C: "LLM X outperforms baseline on benchmark Y"
> D: "Accuracy 82% vs 73% on Y test set"
> W: "Higher benchmark accuracy = better model"
> B: "Y is widely used; past predictive of field use"
> Q: "On this particular benchmark"
> R: "Unless Y has contamination / distributional shift from deploy target"

Most weak papers hide W (unexamined inference) and lack R (no limitations honestly stated).

## Steel-manning (Rapoport)

Before critique, state the opponent's position *so well they'd endorse it*:

1. Re-express the position charitably (they agree: "yes that's what I meant")
2. List points of agreement
3. Mention what you learned from them
4. Only then — refute

Reviewers who skip 1-3 produce shallow critiques. Rapoport rules improve paper reviews and defense answers.

## Argument diagrams

Trees / graphs of claim dependencies:

```
             Main Claim
            /          \
       Sub-C1         Sub-C2
       /    \         /    \
    D1-a  D1-b    D2-a  D2-b  ← Evidence
```

Supports vs attacks. Use tools: **Argüman**, **Kialo**, **Rationale**, **Araucaria**, **MindMup**.

## Common fallacies in academic writing

| Fallacy | Example |
|---------|---------|
| Ad hominem | Attacking author, not argument |
| Straw man | Caricaturing opposing view |
| Appeal to authority | "Nobel laureate X says" without evidence |
| Circular reasoning | Using conclusion as premise |
| Cherry-picking | Showing only confirming data |
| Hasty generalization | Small-N → universal claim |
| Post hoc | Correlation → causation |
| False dichotomy | Ignoring middle positions |
| Moving goalposts | Redefining success after results |
| Texas sharpshooter | Drawing target after shots |
| p-hacking / HARKing | Hypothesis after results known |
| No true Scotsman | Excluding counterexamples ad hoc |
| Tu quoque | "Others do it too" |
| Base-rate neglect | Ignoring prior probability |
| Survivorship bias | Studying winners only |

## Dialectical structure for Discussion section

1. **What we claim** (restate main finding, specific qualifiers)
2. **Why this matters** (theoretical + practical)
3. **How it compares** (alignment + divergence from prior work)
4. **Alternative interpretations** (list 2-3 + why less plausible)
5. **Limitations** (internal validity, external validity, construct validity, statistical validity)
6. **What would change our mind** (falsification conditions — rare but strong)
7. **Future work** (concrete, not vague)

## Close-reading checklist (paper critique)

Read paper 3× with different lenses:

**Pass 1 — Structure**:
- What is the central claim (1 sentence)?
- What are contributions (listed)?
- What question does it answer?

**Pass 2 — Evidence**:
- Is each claim backed by data/analysis?
- Sample size + effect size + CI adequate?
- Alternative explanations considered?
- Confounders addressed?

**Pass 3 — Warrants**:
- What inference rules are assumed?
- Are they justified or smuggled in?
- Would critic in field accept them?

## Counterargument generation

For every claim, enumerate:

- **Methodological**: sampling, measurement, analysis pipeline
- **Statistical**: power, multiple comparisons, assumptions
- **Interpretive**: alternative frames, confounds
- **External validity**: generalization limits
- **Theoretical**: competing theories
- **Practical**: implementation at scale

## Reviewer's "killer" questions

Practice answering:
- "Why is this novel vs [paper X, year]?"
- "What's the effect size in practical terms?"
- "How would you respond if [alternative explanation]?"
- "What's the one experiment that could falsify this?"
- "Why these parameters and not others?"
- "Are you sure the signal isn't artifact of [pipeline step]?"

## Steel-man vs straw-man test

Before submitting critique, ask: "If the author read this, would they say:
(a) 'Fair — I see the objection'  ← steel-man
(b) 'That's not what I argued'      ← straw-man
(c) 'They didn't read it'           ← unfair"

Only (a) earns reviewer credibility.

## Feynman technique for clarity

To verify you understand an argument (yours or another's):
1. Write it for a bright 12-year-old.
2. Find gaps in your explanation.
3. Fill gaps from source. Repeat.
4. If you can't do step 1, you don't understand it.

## References

- Toulmin — *The Uses of Argument*
- Walton — *Informal Logic*, *Argumentation Schemes*
- Kahneman — *Thinking, Fast and Slow* (cognitive biases)
- Dennett — *Intuition Pumps* (Rapoport rules Ch 3)
- Van Eemeren & Grootendorst — Pragma-dialectics
- Graff & Birkenstein — *They Say / I Say* (academic templates)

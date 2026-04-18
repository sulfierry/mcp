---
name: nature-style-guide
description: "Nature/Science/Cell prose style enforcement. Voice (active 'we show'), tense (present for claims, past for methods), hedge elimination, concrete nouns over abstract nominalizations, parallel structure, British vs US English per journal, in-text citation style (numeric vs author-year). Triggers on Nature style, Science style, Cell style, prose editing, hedge, nominalization, voice, tense."
category: scientific-writing
tags: [style, prose, nature, science, cell, editing, voice]
---

# Nature/Science/Cell Style

## When to use
- Polishing manuscript prose before submission at top-tier
- Editing passive, hedging, or abstract sentences
- Aligning voice/tense/citation style with journal

## Voice: Active over passive

Active puts agent first, reads faster:

| Passive (weak) | Active (strong) |
|----------------|-----------------|
| "The reaction was carried out by the enzyme." | "The enzyme catalyzed the reaction." |
| "It was observed that X increases Y." | "X increases Y." |
| "A structure was determined at 2.1 Å." | "We determined the structure at 2.1 Å." |

**"We"** is accepted and preferred at Nature / Cell / Science. Single-author paper: "I" is acceptable (rare in STEM).

Passive is OK when the object is the topic:
> "The protein was first identified by Smith (1995); subsequent structural studies revealed..."

## Tense

| Context | Tense |
|---------|-------|
| General scientific fact | present ("DNA carries genetic information") |
| Specific results of THIS study | past ("we observed", "the mutation reduced activity") |
| Implications / interpretations | present ("these findings suggest") |
| Other researchers' results | past ("Smith reported") |
| Figure captions / what a figure shows | present ("Figure 1 shows") |
| Methods | past ("we synthesized", "cells were cultured") |
| Literature review | present perfect or past ("has been reported" / "reported") |

## Hedge elimination

Hedges cluster; remove redundant ones:

**Stacked hedges** (weak):
> "The results may suggest that X could potentially contribute to Y."

**One calibrated qualifier** (strong):
> "The results suggest that X contributes to Y."

Or if uncertainty is real:
> "X likely contributes to Y (p = 0.03), although causation remains untested."

### Hedge words to audit
- may, might, could, would, seem, appear, suggest, indicate, possibly, potentially, perhaps, somewhat, relatively

Rule: ≤ 1 hedge word per sentence. Zero in title/abstract unless statistically required.

## Concrete nouns over nominalizations

Nominalizations convert verbs to abstract nouns ("investigation", "examination", "determination"). Replace with verbs.

| Nominalization (dense) | Verb (clear) |
|------------------------|--------------|
| "We performed an investigation of..." | "We investigated..." |
| "The determination of structure was achieved..." | "We determined the structure..." |
| "A reduction in activity was observed..." | "Activity decreased..." |
| "There was an examination of..." | "We examined..." |

Gopen & Swan's principle: stress position (end of sentence) should carry new/important information.

## Parallel structure

List elements share grammatical form:

**Not parallel** (jarring):
> "We isolated the protein, crystallization, and then determined structure."

**Parallel**:
> "We isolated the protein, crystallized it, and determined its structure."

## Specific over general

**Vague**:
> "At high resolution, we observed the molecule."

**Specific**:
> "At 2.1 Å resolution, we resolved 287 amino-acid side chains."

Numbers + units + context > adjectives.

## British vs US English per journal

| Journal | Variant |
|---------|---------|
| Nature (and all Springer Nature UK-managed) | **British** |
| Science (AAAS) | **US** |
| Cell (Cell Press / Elsevier) | **US** |
| NEJM | **US** |
| Lancet | **British** |
| eLife | either (consistent) |
| PNAS | **US** |

Common differences:
- -ize vs -ise (Nature UK accepts both -ize; verify style sheet)
- colour vs color
- centre vs center
- analyse vs analyze (British vs US)
- organise vs organize
- towards vs toward (British vs US)
- amongst vs among
- spelling of specific words: sulphur (UK) vs sulfur (US)

Set Word/LaTeX language pack to your target before writing.

## Citation styles

| Journal | Style |
|---------|-------|
| Nature | numeric superscript¹ |
| Science | numeric (in parentheses, unitalicized) *(1)* |
| Cell | author-year (Smith et al., 2020) |
| PNAS | numeric (parenthetical) |
| eLife | author-year |
| NEJM | numeric superscript |
| Lancet | numeric (parenthetical) |
| PLOS | numeric (parenthetical) |

Use Zotero / Mendeley / EndNote with journal-specific CSL style file.

## Word budgets (typical)

| Journal | Article | Letter/Report | Abstract |
|---------|---------|---------------|----------|
| Nature | 4500 w | 2000 w (Letter) | 150 w |
| Science | 4500 w (Research Article) | 2500 w (Report) | 125 w + 1-paragraph summary |
| Cell | 8000 w (Article) | — | 150 w |
| NEJM | 2700 w (Original) | 1000 w (Brief) | 300 w structured |
| eLife | no hard limit | — | 150-200 w |

Budget includes/excludes references, captions, methods — verify per journal.

## Sentence length + rhythm

Mix short and long:
- ≤ 15 words: punch, connection
- 15-25: workhorse
- 25-35: complex ideas, subordination
- > 40: suspect; rewrite

Alternate to maintain reader engagement. Stacking >30-word sentences ≥ 3 in a row = bad.

## Figure references in text

Each figure MUST be cited in text, in order:

> "...as shown in Fig. 1a..."
> "Figure 2 depicts..."

Nature-style: "Fig. 1a" inline; "Figure 1" sentence-initial. Check journal guide (abbreviation rules vary).

## Numbers and units

| Rule | Example |
|------|---------|
| Spell out 0-9, numerals for ≥10 | "three proteins", "12 samples" (varies by journal) |
| Units: SI, space before unit | "2.1 Å", "100 µM", "5 °C" |
| Decimal: period (Nature/Cell), comma (some European) | "0.5" or "0,5" |
| Significant figures: match precision of measurement | report SD to same decimal as mean |

## Ambiguity elimination

- "It" / "they" / "this": always check antecedent is clear
- "Latter" / "former": clarify if >2 items
- Acronyms: define at first use in text + abstract separately
- "Recent": date-stamp ("recently (2023)")

## Nature/Cell "Significance sentence"

Often requested first sentence of Introduction and Discussion. Formula:

> "[Broad phenomenon] [specific mystery]. We [brief approach]. We find [specific result]. This [implication]."

## Common Nature-style patterns

- Opening: "Physical/biological phenomenon X has long been understood to..."
- Transition between paragraphs: "Given this, we asked whether..."
- Results anchor: "Fig. 1a shows..."
- Discussion framing: "Our finding challenges/extends..."
- Closing: "These results establish [X], and open the door to [Y]."

## Pre-submission linting checklist

- [ ] Passive voice < 20% (Word grammar checker / Hemingway App)
- [ ] Stacked hedges removed
- [ ] No nominalization chain >2 in a sentence
- [ ] Citation style matches journal
- [ ] Spelling variant consistent (UK or US throughout)
- [ ] Abbreviations defined at first use (+ in abstract independently)
- [ ] Word count within journal limit
- [ ] Figure / table / equation numbers sequential, all cited
- [ ] All references complete (no "in prep" unless allowed)
- [ ] Title is a declarative claim, not a topic phrase
- [ ] Abstract starts with broad hook, ends with implication
- [ ] No "very", "really", "basically", "simply" — remove all

## References

- Schimel — *Writing Science* (Oxford)
- Gopen & Swan — "The Science of Scientific Writing" (*Am Scientist* 78, 550-558)
- Strunk & White — *The Elements of Style*
- Pinker — *The Sense of Style*
- Mensh & Kording — "Ten simple rules for structuring papers" (PLOS CB)
- Nature / Science / Cell journal style guides (available on journal websites)
- Hemingway App, Grammarly, ProWritingAid — prose linters
- CSL style repository: zotero.org/styles

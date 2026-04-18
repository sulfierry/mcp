# Skills

## Anatomy

A skill is a directory under `skills/<id>/` containing a `SKILL.md` with YAML frontmatter + markdown body.

```
skills/causal-inference/
├── SKILL.md              # required
├── references/           # optional: long-form docs
│   └── *.md
└── scripts/              # optional: helper code exposed via get_skill_scripts
    └── *.py
```

## Frontmatter schema

```yaml
---
name: causal-inference
description: "Pearl-style causal inference for PhD-grade scientific rigor. Triggers on ..."
category: scientific-writing          # auto-tagged if missing
tags: [causal-inference, phd, statistics]
license: MIT                          # optional
source: custom                        # optional; "custom" = this repo, or upstream name
---
```

Required: `name`, `description`. Everything else is optional or overlay-supplied.

## Body structure

Loose convention (helps `list_sections` work):

```markdown
# <name>

## When to use
...

## Install / setup
...

## Core workflows
...

## Related
- `other-skill-id` — ...
```

## Adding a skill

1. Create `skills/my-new-skill/SKILL.md` with frontmatter.
2. `python3 scripts/build_catalog.py` — regenerates `skills_index.json`.
3. `python3 scripts/auto_tag_skills.py` — applies category rules (if `category:` not set in frontmatter).

## Categories (56)

Auto-tagger classifies by rule table in `scripts/auto_tag_skills.py`. First matching rule wins; default is `misc`. Classification uses id + name + path tokens — not descriptions (avoids pollution).

Top buckets: `misc`, `variant-calling`, `single-cell`, `devops-infra`, `langs`, `bio-database`, `visualization-scientific`, `frontend`, `cheminformatics`, `ml-framework`, `chip-atac`, `architecture`, `phylogenetics`, `statistics`, `security`, `scientific-writing`, `testing`, `debug-error`.

Run `list_categories()` via MCP or CLI to see current counts.

## Retagging

Edit rules in `scripts/auto_tag_skills.py`, then:
```bash
python3 scripts/auto_tag_skills.py            # applies, updates overlay
```

Overlay is additive — manual categorizations in `skills_index.json` survive unless the same id gets reclassified on rerun.

## Scripts

Files under a skill's `scripts/` subdirectory are exposed via `get_skill_scripts(id)`. Useful for:
- Code snippets the assistant can run/adapt
- CLI wrappers
- Input/output schema examples

## Manually setting category

Add `category:` in frontmatter:
```yaml
---
name: my-skill
description: ...
category: structural-biology
---
```

Build_catalog reads this; auto-tagger overrides only if the id matches a rule. To pin, add a rule or skip auto-tagger for that skill.

## Trigger descriptions

Descriptions should contain trigger keywords that the assistant might match semantically:

> "Pearl-style causal inference for PhD-grade scientific rigor. DAGs, do-calculus, backdoor/frontdoor criteria, counterfactuals, ... **Triggers when user discusses causal claims, confounding, treatment effects, instrumental variables, natural experiments, RCT analysis, observational study adjustments.**"

The "Triggers" sentence is heuristic guidance for `search_skills` and for LLM reasoning — not enforced.

## License

Each skill carries its own license in frontmatter (`license: MIT` etc.). When a skill is imported from an upstream repo, the upstream license is preserved in `source:`.

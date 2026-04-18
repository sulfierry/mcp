# Agents

Agents are specialist personas that combine multiple skills with an expert system prompt. Same SKILL.md schema as skills; the distinction is the `kind="agent"` tag applied at registry load.

## Current roster

| Agent | Focus |
|-------|-------|
| `academic-pipeline` | 10-stage research→write→integrity check→peer review→revise |
| `bioinformatics-researcher` | Computational biology, protein structure, docking, kinase biology |
| `code-reviewer` | Systematic review — Python/TS/Go/Rust/Java |
| `deep-research` | 7 modes: full research, quick brief, PRISMA, Socratic, fact-check, lit review, quality review |
| `devops-engineer` | Docker/K8s/Terraform/GitHub Actions/Prometheus/Grafana/GitOps |
| `docking-specialist` | Molecular docking campaigns (prep, libraries, sites, protocols, interpretation) |
| `fullstack-developer` | React/Next + FastAPI + PostgreSQL + Docker, TDD + CI/CD |
| `python-architect` | Async, type-safe, SOLID, FastAPI/Django/SQLAlchemy, Python 3.12+ |
| `ui-ux-designer` | Design systems, WCAG 2.2, Figma→code, micro-animations |

Plus imported curated agents under `agents/by-*`: `by-design`, `by-screening`, `by-research`, `by-epitope`, `by-humanization` (protein-design personas from blatant-why).

## Invoking

Via Claude Code `Agent` tool:
```
Agent(subagent_type="code-reviewer", description="review PR #42", prompt="...")
```

Or discover via MCP:
```
search_skills("python backend", kind="agent")
get_skill("python-architect", kind="agent")
```

## Schema

Same SKILL.md format as a skill. Difference: stored under `agents/<id>/` and loaded into the agent registry.

## Collision with skills of same id

Agent and skill registries can both hold the same id. `get_skill(id)` without `kind` tries skills first then falls back to agents. To force, pass `kind="skill"` or `kind="agent"`.

## Adding an agent

```
agents/my-agent/SKILL.md
```

Frontmatter identical to a skill. Restart server to pick up.

## When skill vs agent?

- **Skill**: a how-to reference the assistant consults when working on a task.
- **Agent**: a persona that encapsulates a workflow and is *invoked* (often as a subagent) to execute a multi-step task with its own internal reasoning.

Example: `peer-review` is a skill (methodology reference); `academic-paper-reviewer` is an agent (simulates 5 reviewer personas end-to-end).

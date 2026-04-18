# Project scopes

Scopes let different working directories see different slices of the catalog. A `.mcp.json` in the directory declares which MCP servers (and which filter) the assistant should connect to when launched there.

## Why

Registering all 1,260 skills globally costs ~1-2 KB of tool-schema tokens every session, even when most are irrelevant. Project scopes:

- Cut per-session overhead to 0 in neutral directories
- Expose a focused ~200-skill slice in domain directories
- Let Copilot/Claude see the same filter (both read workspace `.mcp.json`)

## Pre-built scopes

| Scope | Skills | MCPs loaded | Intended work |
|-------|--------|-------------|---------------|
| `code` | 358 | `skills-server-code` | programming (lang, framework, devops, ML, LLM, testing, security, architecture) |
| `mol` | 228 | `skills-server-mol`, `bw-pdb`, `bw-uniprot`, `bw-research` | protein / drug / MD modeling |
| `sci` | 149 | `skills-server-sci`, `bw-research` | scientific writing, peer review, PRISMA, Nature-grade craft |

Each lives at `~/work/<name>-scope/` with its own `.mcp.json` and `README.md`.

## How scopes work

Each `.mcp.json` spawns a filtered instance of the main `mcp_skills_server.py`:

```json
{
  "mcpServers": {
    "skills-server-code": {
      "type": "stdio",
      "command": "/path/to/.venv/bin/python3",
      "args": ["/path/to/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/server",
        "SKILLS_CATEGORY_FILTER": "frontend,backend-api,devops-infra,langs,databases,testing,architecture,refactoring,git-workflow,security,debug-error,agent-orchestration,claude-tooling,context-mgmt,llm-rag,design-diagrams,notebook-writing,workflow-engine,ops-analytics,cli-tools,ml-framework,deep-learning-bio,statistics,code-review",
        "AGENTS_CATEGORY_FILTER": ""
      }
    }
  }
}
```

Key env vars:
- `SKILLS_CATEGORY_FILTER` — comma-separated. Empty / unset = all skills.
- `AGENTS_CATEGORY_FILTER` — same, for the agent registry (defaults to all 9).

## The `scope` CLI

`scripts/scope` (symlinked to `~/.local/bin/scope`) brings a scope's `.mcp.json` into your current working directory without needing to `cd` to `~/work/<scope>-scope/`.

```bash
scope                 # show active scope + list available
scope list            # just list
scope code            # copy code-scope/.mcp.json to ./
scope --symlink mol   # or symlink (tracks upstream edits)
scope none            # remove local .mcp.json (moves to .bak)
```

The CLI auto-discovers any `~/work/*-scope/` directory. Override root with `SCOPE_ROOT=~/custom/path`.

## Typical workflow

```bash
cd ~/real/project
scope code                     # .mcp.json now present
claude                         # assistant sees 358 code skills
```

Switch domain mid-project:

```bash
scope none                     # deactivate
scope mol                      # switch to molecular modeling
claude
```

## Creating a new scope

Manually:

```bash
mkdir -p ~/work/data-scope
cat > ~/work/data-scope/.mcp.json <<'JSON'
{
  "mcpServers": {
    "skills-server-data": {
      "type": "stdio",
      "command": "/path/to/.venv/bin/python3",
      "args": ["/path/to/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/server",
        "SKILLS_CATEGORY_FILTER": "statistics,ml-framework,deep-learning-bio,databases,notebook-writing,visualization-scientific,ops-analytics",
        "AGENTS_CATEGORY_FILTER": ""
      }
    }
  }
}
JSON
scope list   # data appears automatically
```

Add an optional `README.md` inside the dir documenting the scope.

## Available categories

Run inside any scope (or global session):

```
list_categories()
```

or CLI:
```bash
PYTHONPATH=server .venv/bin/python3 -c \
  "from skill_registry import SkillRegistry; \
   r=SkillRegistry('skills',overlay_index='skills_index.json'); r.scan(); \
   [print(c) for c in r.list_categories()]"
```

56 categories currently. Top buckets: `misc`, `variant-calling`, `single-cell`, `devops-infra`, `langs`, `bio-database`, `visualization-scientific`, `frontend`, `cheminformatics`, `ml-framework`, `structural-biology`, `scientific-writing`.

## Opt-out: don't register a global skills-server

If you always open the assistant from inside a scope, skip the user-scope registration:

```bash
SKIP_CLAUDE_USER_SCOPE=1 ./scripts/sync_skills.sh
```

Or `export SKIP_CLAUDE_USER_SCOPE=1` permanently. Scripts and Copilot-config injection respect this flag.

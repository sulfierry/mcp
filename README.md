# Skills MCP

Local **Model Context Protocol** server exposing **1,270+ curated skills** and **18 agent personas** to AI coding assistants.

Default support: **Claude Code**, **GitHub Copilot CLI**, **OpenAI Codex CLI** (plus VS Code, Cursor, Claude Desktop, Antigravity, Qwen).

## Why this exists

Using skills **directly from upstream repos** (cloning `awesome-claude-subagents`,
`scientific-agent-skills`, `bioSkills`, etc. and symlinking into `~/.claude/skills/`)
looks free but has a real cost: **every session loads the full skill list into
context as a system reminder**. With 1,270 skills that is **~32 KB / 8-10k
tokens per session**, paid whether you use any skill or not.

This repo wraps those skills in a thin MCP server that exposes them **lazily**:
3 tool schemas (~270 tokens) at session start, full SKILL.md bodies only when
searched or fetched. The numbers:

| Approach | Cost per session | Discovery |
|----------|------------------|-----------|
| Raw symlinks into `~/.claude/skills/` | **~8-10k tokens** (full list dumped) | eager |
| This MCP server (default) | **~270 tokens** (3 tool schemas) | lazy on-demand |
| MCP + scope filter (e.g. `mol` = 228 skills) | **~270 tokens**, narrower catalog | lazy on-demand |

## Highlights

- **1,270+ skills** from 10+ curated upstream repos (bio, scientific writing, engineering, ML/LLM)
- **~30× cheaper** per session than raw upstream skill symlinks (measured)
- **3 consolidated tools** — down from 6 (schema budget: 500 tok → 270 tok)
- **Markdown + prefix-grouped output** — `list_skills(format='md')` is 70 % smaller than JSON
- **Project scopes**: per-directory skill filtering (`code` / `mol` / `sci`)
- **Session LRU cache** + budget regression tests (`tests/test_token_budget.py`)
- **Transport**: stdio + SSE (HTTP)

## Install

```bash
git clone https://github.com/sulfierry/mcp.git && cd mcp
python3 -m venv .venv && source .venv/bin/activate
pip install fastmcp pyyaml
./scripts/sync_skills.sh          # first-time: pulls curated skills from 10+ sources
```

The sync script is **token-optimized by default**: it does NOT create
`~/.claude/skills/` / `~/.codex/skills/` symlinks, because those dirs cause
the IDE to dump the full 1,270-skill list into every session. Opt in via
`NATIVE_SKILL_WHITELIST="graphify,foo"` if you need specific skills reachable
through `/slash` commands, or `ENABLE_NATIVE_SKILL_SYMLINKS=1` to restore
legacy all-skills behavior.

Sync is idempotent and re-runnable to pull updates. See [`docs/SYNC.md`](docs/SYNC.md) and [`docs/TOKEN-OPTIMIZATION.md`](docs/TOKEN-OPTIMIZATION.md) for the full trade-off and all opt-out flags.

## Register with your assistant

### Claude Code
```bash
claude mcp add --scope user skills-server \
  $(pwd)/.venv/bin/python3 $(pwd)/server/mcp_skills_server.py
```

### GitHub Copilot CLI
Write `~/.copilot/mcp-config.json`:
```json
{
  "mcpServers": {
    "skills-server": {
      "type": "stdio",
      "command": "/ABSOLUTE/PATH/mcp/.venv/bin/python3",
      "args": ["/ABSOLUTE/PATH/mcp/server/mcp_skills_server.py"],
      "env": { "PYTHONPATH": "/ABSOLUTE/PATH/mcp/server" }
    }
  }
}
```

### OpenAI Codex CLI
```bash
codex mcp add skills-server --env PYTHONPATH="$(pwd)/server" \
  -- $(pwd)/.venv/bin/python3 $(pwd)/server/mcp_skills_server.py
```

Or let `sync_skills.sh` configure all of them automatically (VS Code, Cursor, Qwen, Claude Desktop, Antigravity too).

## Usage

After registering, the assistant gains **3 consolidated tools**:

| Tool | Purpose |
|------|---------|
| `list_skills(limit, offset, category, kind, compact, format, group_by_prefix, include_categories, pretty)` | Paginated catalog with optional markdown output, prefix grouping, and category counts |
| `search_skills(query, limit, kind, compact, format, pretty)` | Keyword search across skills + agents |
| `get_skill(skill_id, section, kind, mode, verbose, keep_frontmatter)` | Fetch skill body. `mode='outline'` returns H2 titles only (TOC); `mode='scripts'` returns helper scripts |

Typical flow inside the assistant:
```
search_skills("molecular docking", format="md")
  → get_skill("diffdock", mode="outline")     # cheap: just section titles
  → get_skill("diffdock", section="Usage")    # one H2 block
```

Everything produced is minified JSON by default (`pretty=True` to indent).
Resources `skills://catalog` and `skills://categories` are also available for
clients that auto-subscribe.

## Project scopes

Different work benefits from different skill subsets. Pre-built scopes in `~/work/<scope>-scope/`:

| Scope | Skills | Focus |
|-------|--------|-------|
| `code` | 358 | Languages, frameworks, DevOps, testing, architecture, LLM/ML, security |
| `mol` | 228 | Structure prediction (AF2/3, Boltz, Chai-1), RFdiffusion, MD (OpenMM/GROMACS), FEP/ABFE/FES, docking |
| `sci` | 149 | PhD-grade writing, rigor (PRISMA, causal inference, reproducibility), Nature/Science craft |

Activate with the `scope` CLI:
```bash
scope sci                # copies sci-scope/.mcp.json to cwd
scope --symlink code     # or symlink (tracks upstream changes)
scope none               # deactivate in current dir
```

Details: [`docs/SCOPES.md`](docs/SCOPES.md).

## Directory layout

```
mcp/
├── server/
│   ├── mcp_skills_server.py      # FastMCP entry point
│   ├── skill_registry.py         # scan / filter / overlay
│   └── external_mcps/            # vendored domain-specific MCP servers (pdb, uniprot, ...)
├── skills/                        # 1,270+ skill dirs (SKILL.md each)
├── agents/                        # 18 agent personas
├── commands/                      # slash commands (gmmsb-*)
├── scripts/
│   ├── sync_skills.sh            # pull from source repos, configure IDEs
│   ├── auto_tag_skills.py        # category classifier (overlay)
│   ├── build_catalog.py          # regenerate skills_index.json
│   └── scope                     # activate a scope's .mcp.json in cwd
├── skills_index.json             # overlay: category + tags per skill
├── start_server.sh               # one-command launcher (stdio or SSE)
└── docs/                         # deep-dive documentation
```

## Documentation

| File | Topic |
|------|-------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Server internals, overlay system, namespace merge |
| [`docs/SCOPES.md`](docs/SCOPES.md) | Project scopes, `SKILLS_CATEGORY_FILTER`, scope CLI |
| [`docs/SKILLS.md`](docs/SKILLS.md) | Skill anatomy, adding a skill, auto-tagger |
| [`docs/AGENTS.md`](docs/AGENTS.md) | Agent personas, `kind` filter |
| [`docs/SYNC.md`](docs/SYNC.md) | Source repositories, sync phases, opt-out flags |
| [`docs/EXTERNAL-MCPS.md`](docs/EXTERNAL-MCPS.md) | Vendored domain servers (pdb, uniprot, sabdab, research, ...) |
| [`docs/TOKEN-OPTIMIZATION.md`](docs/TOKEN-OPTIMIZATION.md) | All 20+ optimizations, measured savings vs raw upstream, budget regression tests |

## License

MIT for this repository's own code. Individual skills and vendored MCP servers retain their upstream licenses (listed in their SKILL.md frontmatter or subdirectory READMEs).

## Issues / contributions

Bugs: https://github.com/sulfierry/mcp/issues · Pull requests welcome.

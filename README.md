# Skills MCP

Local **Model Context Protocol** server exposing **1,270+ curated skills** and **9 agent personas** to AI coding assistants.

Default support: **Claude Code**, **GitHub Copilot CLI**, **OpenAI Codex CLI** (plus VS Code, Cursor, Claude Desktop, Antigravity, Qwen).

## Highlights

- **1,270+ skills**, **9 agents**, **56 categories** (auto-tagged)
- **Token-efficient**: default `list_skills()` payload ≈ 4 KB (baseline was 483 KB, -99 %)
- **Project scopes**: filter skills per working dir (`code` / `mol` / `sci`) — activate with `scope <name>`
- **Namespace-merged API**: 6 tools handle both skills and agents via `kind` filter
- **Transport**: stdio + SSE (HTTP)

## Install

```bash
git clone https://github.com/sulfierry/mcp.git && cd mcp
python3 -m venv .venv && source .venv/bin/activate
pip install fastmcp pyyaml
./scripts/sync_skills.sh          # first-time: pulls curated skills from 10+ sources
```

Sync is idempotent and re-runnable to pull updates. See [`docs/SYNC.md`](docs/SYNC.md) for source list, curation, and opt-out flags.

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

After registering, the assistant gains 6 tools:

| Tool | Purpose |
|------|---------|
| `list_skills(limit, offset, category, kind, compact)` | Paginated catalog |
| `list_categories(kind)` | Counts per category |
| `search_skills(query, limit, kind, compact)` | Keyword search, merged skill+agent |
| `get_skill(skill_id, section, kind)` | Fetch SKILL.md (optionally by H2 section) |
| `list_sections(skill_id, kind)` | H2 titles for cheap TOC |
| `get_skill_scripts(skill_id, kind)` | Helper scripts from skill's `scripts/` subdir |

Typical flow inside the assistant:
```
search_skills("molecular docking") → get_skill("diffdock", section="Usage")
```

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
├── agents/                        # 9 agent personas
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
| [`docs/TOKEN-OPTIMIZATION.md`](docs/TOKEN-OPTIMIZATION.md) | How default payload shrank 99 % |

## License

MIT for this repository's own code. Individual skills and vendored MCP servers retain their upstream licenses (listed in their SKILL.md frontmatter or subdirectory READMEs).

## Issues / contributions

Bugs: https://github.com/sulfierry/mcp/issues · Pull requests welcome.

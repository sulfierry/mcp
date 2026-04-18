# Architecture

## Server stack

```
Client (Claude Code / Copilot CLI / Codex / VS Code / Cursor / ...)
  │   JSON-RPC (stdio)  or  HTTP/SSE
  ▼
server/mcp_skills_server.py       FastMCP tool registration
  │
  ▼
server/skill_registry.py          Scan + overlay + filter + query
  │
  ▼
skills/*/SKILL.md                 Skill artifacts (frontmatter + prose)
agents/*/SKILL.md                 Agent personas (same schema)
skills_index.json                 Overlay: category, tags, source per id
```

## Registry lifecycle

On process start:

1. `SkillRegistry(skills_dir, overlay_index, kind)` is instantiated twice — once for `skills/`, once for `agents/`.
2. `scan()` walks `rglob("SKILL.md")`, parses YAML frontmatter, populates an `id → SkillEntry` dict.
3. `_apply_overlay()` reads `skills_index.json` and rewrites `category` / `tags` where present — this lets the auto-tagger drive classification without mutating source files.
4. `_apply_category_filter()` drops entries whose category is not in `SKILLS_CATEGORY_FILTER` (if set). This is how project scopes restrict surface area.

## Overlay system

`skills_index.json` is a flat array:

```json
[{"id": "boltz-structure-prediction",
  "name": "boltz-structure-prediction",
  "description": "...",
  "path": "boltz-structure-prediction/SKILL.md",
  "category": "structural-biology",
  "tags": [],
  "source": "custom"}, ...]
```

- `scripts/build_catalog.py` regenerates it from SKILL.md frontmatter.
- `scripts/auto_tag_skills.py` post-processes and assigns `category` via rule-based classifier (regex on id + name + path; descriptions excluded to avoid pollution).
- Users can manually edit entries — they survive re-runs because auto-tagger only rewrites on its own classification pass, not per-field merge.

## Namespace merge (skills ↔ agents)

Two registries, unified façade:

```python
def _registries_for(kind: str) -> list[SkillRegistry]:
    if kind == "skill":  return [registry]
    if kind == "agent":  return [agent_registry]
    return [registry, agent_registry]   # default: both
```

All 6 tools accept an optional `kind` param. Output entries carry a `kind` field so the client can distinguish. Dropping dedicated `list_agents/get_agent/search_agents` tools saved ~300 tokens of always-loaded schema per session.

## Category filter (project scopes)

`SKILLS_CATEGORY_FILTER` env var (comma-separated) gates which skills the server exposes. Combined with MCP project scope (`.mcp.json` per working dir), this enables:

- `~/work/mol-scope/` → only 15 molecular categories → ~228 skills visible
- `~/work/code-scope/` → 24 code categories → ~358 skills
- `~/work/sci-scope/` → 9 scientific-writing categories → ~149 skills
- Anywhere else → server not registered → 0 skill overhead

Filter applies *after* overlay, so user customizations flow through.

## Trim & pagination

Default `list_skills()` returns 50 entries, compact mode (id + name + category, no description). Non-compact truncates descriptions to 160 chars (configurable via `desc_chars`).

`skills://catalog` MCP resource used to return 483 KB of full frontmatter on auto-load; now emits only `{id, name, category}` (~109 KB). Clients that auto-fetch resources pay 4× less.

## Section-filtered fetches

`get_skill(id, section="Quick Start")` returns only the matching H2 block, typically shrinking a 5-30 KB SKILL.md to 0.5-2 KB. `list_sections(id)` returns the cheap TOC (H2 titles only).

## External MCP servers

`server/external_mcps/` hosts vendored third-party MCP servers (e.g., `blatant_why/pdb/server.py`). These run as separate processes — the main skills server does not proxy them. Each has a README explaining install and API key requirements. See [`EXTERNAL-MCPS.md`](EXTERNAL-MCPS.md).

## Transport

- **stdio**: default. One subprocess per client. Recommended for desktop integrations.
- **SSE**: run `./start_server.sh --sse 8765` to expose HTTP/SSE on `localhost:8765`. Use for shared deployments or non-stdio clients.

## Performance

| Operation | Time (cold start) |
|-----------|-------------------|
| `SkillRegistry.scan()` for 1,260 skills | ~150 ms |
| `_apply_overlay()` | ~20 ms |
| `list_skills(limit=50)` | < 5 ms |
| `search_skills(query)` (linear scan) | < 20 ms |
| `get_skill(id)` + read SKILL.md | 2-5 ms |

Memory: ~30 MB resident for 1,260 skills.

# Token optimization

Baseline `list_skills()` payload once exceeded 483 KB (≈ 120 K tokens) for 1,179 skills — flooding context on every session. Current default is 4.1 KB (≈ 1 K tokens). This doc covers every knob.

## Measured impact

| Call | Before | After | Δ |
|------|--------|-------|---|
| `list_skills()` default | 483,002 chars | 4,152 chars | −99.1 % |
| `list_skills(category='X')` | — | ~600 chars | new |
| `list_skills(limit=50, compact=False)` trimmed desc | ~400 KB | 12.6 KB | −97 % |
| `get_skill(id, section='Quick Start')` | 5-30 KB | ~1 KB | −80 to −98 % |
| `list_sections(id)` | — | ~200 chars | cheap TOC |
| `skills://catalog` auto-load resource | 483 KB | 109 KB | −77 % |
| Tool schemas in context | ~800 tokens (9 tools) | ~270 tokens (3 tools) | merged + consolidated |

## Techniques

### 1. Pagination + compact mode

`list_skills()` returns `{total, offset, limit, count, has_more, skills}`. Default `limit=50, compact=True` (id + name + category only). Clients can page through with `offset`. `compact=False` includes description, truncated to 160 chars.

### 2. Category filter at scope level

`SKILLS_CATEGORY_FILTER` env var restricts the registry at scan time. Project scopes set it per `.mcp.json`. A 149-skill `sci` scope pays 1/8 the tokens of the unfiltered catalog. See [`SCOPES.md`](SCOPES.md).

### 3. Namespace merge (skills ↔ agents)

Previously: 3 separate tools for agents (`list_agents`, `get_agent`, `search_agents`). Now: all tools accept `kind` param. Dropping 3 tool schemas saves ~300 tokens of always-loaded surface per session.

### 4. Description truncation

Long descriptions (e.g., academic-paper lists Chinese triggers and 10+ synonyms) get truncated to 160 chars in `list_skills(compact=False)`. Full description only in `get_skill(id)`.

### 5. Lean `skills://catalog` resource

Some MCP clients auto-subscribe to resources. The catalog resource used to dump full frontmatter. Now emits only `{id, name, category}` — 4× smaller, still useful as an index.

### 6. Section-filtered `get_skill`

```python
get_skill("molecular-docking", section="Quick Start")
# returns just the "## Quick Start" H2 block, not the full 5 KB file
```

Pair with `list_sections(id)` (cheap TOC) to discover sections before fetching.

### 7. Auto-tagger classifies 93 % of catalog

1,172 / 1,260 skills auto-categorized. Only 88 are `misc`. High-precision categories make the `category=...` filter useful — scopes can target narrow slices.

## Opt-out: skip user-scope registration

If you always launch assistants from inside a scope (`scope code && claude`), you can skip user-scope altogether:

```bash
SKIP_CLAUDE_USER_SCOPE=1 ./scripts/sync_skills.sh
```

This skips `claude mcp add --scope user skills-server` and writing `~/.copilot/mcp-config.json`. Cost: zero skills-server tokens in every session except when in a scope dir.

## Trade-offs

| Choice | Pro | Con |
|--------|-----|-----|
| Full user-scope register | catalog available everywhere | +1-2 K tokens / session always |
| Filtered user-scope (narrow category list) | lightweight discovery | incomplete view |
| Project-scope only (this repo's default) | zero cost outside scope dirs | must `cd` or `scope <name>` first |

## Raw MCP tool schema budget (current)

**3 tools, ~270 tokens** of permanent schema (down from 6 tools / ~500 tok):

```
list_skills        (8 params)    ~130 tok   # + format, group_by_prefix, include_categories
search_skills      (5 params)    ~80        # + format
get_skill          (4 params)    ~60        # + mode (outline|scripts|full)
```

Merged tools:
- `list_categories` → `list_skills(include_categories=True, limit=0)`
- `list_sections`   → `get_skill(id, mode='outline')`
- `get_skill_scripts` → `get_skill(id, mode='scripts')`

## Format flag + prefix grouping

`list_skills(format='md', group_by_prefix=True)` renders as markdown and groups
ids by their first `-` segment, stripping the repeated prefix:

| Request | Size | Δ vs pretty JSON |
|---------|------|-------------------|
| `list_skills(50)` JSON pretty (old default) | 5.9 KB | baseline |
| `list_skills(50)` JSON minified (new default) | 3.7 KB | **−38 %** |
| `list_skills(50, format='md')` | 1.6 KB | **−72 %** |
| Full catalog (1,271) JSON pretty | 151 KB | — |
| Full catalog JSON minified | 98 KB | **−35 %** |
| Full catalog `format='md', group_by_prefix=True` | 37 KB | **−75 %** |

Further reductions layered in this pass:
- Redundant `name` dropped when derivable from `id` (saves ~40 B per item × N)
- Empty / `misc` category omitted (1/3 of catalog)
- `kind` field suppressed when caller filtered by kind
- JSON minified by default (opt-in `pretty=True`)
- `skills://categories` resource — counts without tool call
- `SKILLS_SKIP_AGENTS=1` — scope can skip agent registry entirely

## Budget regression guard

`tests/test_token_budget.py` asserts:
- `list_skills(50)` minified < 5 KB
- `list_skills(50, format='md')` < 2 KB
- Full catalog `md+group` < 50 KB
- `get_skill(mode='outline')` < 1 KB
- Redundant-name / misc-category dropping works

## Outline mode

`get_skill(id, mode='outline')` returns H2 titles only — ~200 B vs ~5 KB full
content. Use to triage sections before fetching with `section=<title>`.

## Further reductions (not currently implemented)

- Content-type-specific shorten (drop frontmatter redundancy in `get_skill`)
- Server-side cache of `list_skills` payload per category
- Deferred schema loading via `tools/list` second-pass (only if tool count > 7 again)

PRs welcome.

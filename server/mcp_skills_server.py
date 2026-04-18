"""
MCP Skills Server — exposes Antigravity skills via the Model Context Protocol.

Run with:
    python server/mcp_skills_server.py              # stdio mode (default)
    python server/mcp_skills_server.py --transport sse --port 8765  # SSE/HTTP mode

Requires: pip install fastmcp pyyaml
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from fastmcp import FastMCP
from skill_registry import SkillRegistry

# ── Configuration ─────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
AGENTS_DIR = ROOT_DIR / "agents"
SKILLS_OVERLAY = ROOT_DIR / "skills_index.json"

# ── Initialize Registry ──────────────────────────────────────────────

_cat_env = os.environ.get("SKILLS_CATEGORY_FILTER", "").strip()
_cat_filter = [c for c in _cat_env.split(",") if c.strip()] if _cat_env else None

registry = SkillRegistry(
    str(SKILLS_DIR),
    overlay_index=str(SKILLS_OVERLAY),
    kind="skill",
    category_filter=_cat_filter,
)
skill_count = registry.scan()
if _cat_filter:
    print(f"🧬 Skills Registry loaded: {skill_count} skills (filter: {_cat_filter})", file=sys.stderr)
else:
    print(f"🧬 Skills Registry loaded: {skill_count} skills discovered", file=sys.stderr)

_skip_agents = os.environ.get("SKILLS_SKIP_AGENTS", "").strip() in ("1", "true", "yes")
_agent_cat_env = os.environ.get("AGENTS_CATEGORY_FILTER", "").strip()
_agent_cat_filter = [c for c in _agent_cat_env.split(",") if c.strip()] if _agent_cat_env else None

agent_registry = SkillRegistry(str(AGENTS_DIR), kind="agent", category_filter=_agent_cat_filter)
agent_count = 0
if _skip_agents:
    print("🤖 Agent registry skipped (SKILLS_SKIP_AGENTS=1)", file=sys.stderr)
elif AGENTS_DIR.exists():
    agent_count = agent_registry.scan()
    print(f"🤖 Agent Registry loaded: {agent_count} agents discovered", file=sys.stderr)


def _registries_for(kind: str) -> list[SkillRegistry]:
    """Resolve registries matching kind filter ('', 'skill', 'agent')."""
    k = (kind or "").lower()
    if k == "skill":
        return [registry]
    if k == "agent":
        return [] if _skip_agents else [agent_registry]
    return [registry] if _skip_agents else [registry, agent_registry]


def _format_output(payload: dict, format: str, pretty: bool = False) -> str:
    """Render payload as markdown or JSON. Minified by default; pretty=True indents."""
    if format == "md":
        return SkillRegistry.to_markdown(payload)
    return json.dumps(payload, indent=2 if pretty else None, separators=(",", ":") if not pretty else None)


# ── Session-scoped output cache ──────────────────────────────────────
# Skills/agents are scanned once at startup, never mutated. Cache full
# serialized responses per param set — eliminates re-serialization cost
# when clients paginate or re-query with identical args.
_LIST_CACHE: dict[tuple, str] = {}
_SEARCH_CACHE: dict[tuple, str] = {}
_GET_CACHE: dict[tuple, str] = {}
_CACHE_MAX = 256

def _cache_get(store: dict, key: tuple) -> str | None:
    return store.get(key)

def _cache_put(store: dict, key: tuple, val: str) -> str:
    if len(store) >= _CACHE_MAX:
        # Simple FIFO eviction — pop oldest
        store.pop(next(iter(store)))
    store[key] = val
    return val


# ── Create MCP Server ────────────────────────────────────────────────

mcp = FastMCP("Skills MCP Server")


# ══════════════════════════════════════════════════════════════════════
#  TOOLS — 3 consolidated tools for minimal schema footprint
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_skills(
    limit: int = 50,
    offset: int = 0,
    category: str = "",
    kind: str = "",
    compact: bool = True,
    format: str = "json",
    group_by_prefix: bool = False,
    include_categories: bool = False,
    pretty: bool = False,
) -> str:
    """List skills/agents with pagination, grouping, and category counts.

    Args:
        limit: Max entries (0 = all). Default 50.
        offset: Pagination offset.
        category: Filter by exact category.
        kind: "skill", "agent", or "" (both). When set, `kind` field is omitted per item.
        compact: Omit description (default True).
        format: "json" or "md" (markdown is ~70% smaller).
        group_by_prefix: Group compact ids by first `-` segment (saves bytes).
        include_categories: Append category counts (replaces list_categories).
        pretty: Indent JSON (default False → minified).
    """
    ckey = ("list", limit, offset, category, kind, compact, format, group_by_prefix, include_categories, pretty)
    cached = _cache_get(_LIST_CACHE, ckey)
    if cached is not None:
        return cached

    merged: list[dict] = []
    total = 0
    emit_kind = not kind  # drop redundant kind field when caller filtered
    for reg in _registries_for(kind):
        res = reg.list_skills(limit=0, offset=0, category=category, compact=compact)
        if emit_kind:
            for item in res["skills"]:
                item["kind"] = reg.kind
        merged.extend(res["skills"])
        total += res["total"]

    merged.sort(key=lambda x: (x.get("name") or x["id"]).lower())
    if limit <= 0:
        limit = total
    page = merged[offset: offset + limit]

    skills_out: list | dict = page
    if group_by_prefix and compact:
        skills_out = SkillRegistry.group_by_prefix(page)

    payload: dict = {
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(page),
        "has_more": offset + len(page) < total,
        "skills": skills_out,
    }

    if include_categories:
        from collections import Counter
        c: Counter[str] = Counter()
        for reg in _registries_for(kind):
            for cat in reg.list_categories():
                c[cat["category"]] += cat["count"]
        payload["categories"] = [
            {"category": k, "count": v}
            for k, v in sorted(c.items(), key=lambda x: -x[1])
        ]

    return _cache_put(_LIST_CACHE, ckey, _format_output(payload, format, pretty=pretty))


@mcp.tool()
def search_skills(
    query: str,
    limit: int = 20,
    kind: str = "",
    compact: bool = False,
    format: str = "json",
    pretty: bool = False,
) -> str:
    """Search skills/agents by keyword (name, description, tags, category).

    Args:
        query: Search terms (e.g., 'molecular docking', 'llm inference').
        limit: Max results (default 20).
        kind: "skill", "agent", or "" (both). When set, `kind` field omitted per item.
        compact: Omit description if True.
        format: "json" or "md".
        pretty: Indent JSON (default False).
    """
    ckey = ("search", query, limit, kind, compact, format, pretty)
    cached = _cache_get(_SEARCH_CACHE, ckey)
    if cached is not None:
        return cached

    emit_kind = not kind
    scored: list[dict] = []
    for reg in _registries_for(kind):
        for r in reg.search_skills(query, limit=limit, compact=compact):
            if emit_kind:
                r["kind"] = reg.kind
            scored.append(r)
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)
    scored = scored[:limit]
    if not scored:
        out = _format_output({"message": f"No matches for '{query}'.", "count": 0}, format, pretty)
        return _cache_put(_SEARCH_CACHE, ckey, out)
    payload = {"query": query, "count": len(scored), "results": scored}
    if format == "md":
        out = SkillRegistry.to_markdown({"skills": scored, **payload})
    else:
        out = _format_output(payload, "json", pretty=pretty)
    return _cache_put(_SEARCH_CACHE, ckey, out)


@mcp.tool()
def get_skill(
    skill_id: str,
    section: str = "",
    kind: str = "",
    mode: str = "full",
    verbose: bool = False,
    keep_frontmatter: bool = False,
) -> str:
    """Get skill/agent content in various modes.

    Args:
        skill_id: Directory name (e.g. 'molecular-docking').
        section: Substring of an H2 title (case-insensitive). Empty = full file.
        kind: "skill", "agent", or "" (auto-detect).
        mode: "full" (default: stripped SKILL.md content),
              "outline" (H2 section titles only — cheap TOC),
              "scripts" (return scripts/ subdirectory contents).
        verbose: Include path/tags/source fields (default False).
        keep_frontmatter: Keep YAML block inside content (default False, already in fields).
    """
    ckey = ("get", skill_id, section, kind, mode, verbose, keep_frontmatter)
    cached = _cache_get(_GET_CACHE, ckey)
    if cached is not None:
        return cached

    pretty_separators = (",", ":")
    for reg in _registries_for(kind):
        if mode == "outline":
            titles = reg.list_sections(skill_id)
            if titles is not None:
                out = json.dumps(
                    {"skill_id": skill_id, "kind": reg.kind, "sections": titles},
                    separators=pretty_separators,
                )
                return _cache_put(_GET_CACHE, ckey, out)
            continue
        if mode == "scripts":
            scripts = reg.get_scripts(skill_id)
            if scripts is not None:
                out = json.dumps(
                    {"skill_id": skill_id, "kind": reg.kind, "scripts": scripts},
                    separators=pretty_separators,
                )
                return _cache_put(_GET_CACHE, ckey, out)
            continue
        entry = reg.get_skill(
            skill_id, section=section,
            verbose=verbose, keep_frontmatter=keep_frontmatter,
        )
        if entry:
            if verbose:
                entry["kind"] = reg.kind
            out = json.dumps(entry, separators=pretty_separators)
            return _cache_put(_GET_CACHE, ckey, out)

    if mode == "scripts":
        return json.dumps({"message": f"No scripts found for '{skill_id}'."}, separators=pretty_separators)
    return json.dumps({
        "error": f"'{skill_id}' not found in {kind or 'skills or agents'}.",
        "suggestion": "Use search_skills(query) to find a valid id.",
    }, separators=pretty_separators)


# ══════════════════════════════════════════════════════════════════════
#  RESOURCES — data endpoints the agent can read
# ══════════════════════════════════════════════════════════════════════

@mcp.resource("skills://catalog")
def skills_catalog() -> str:
    """Compact catalog: id + name (if non-derived) + category only."""
    catalog = [
        SkillRegistry._compact_item(s)
        for s in sorted(registry._skills.values(), key=lambda s: s.id)
    ]
    return json.dumps({"count": len(catalog), "catalog": catalog}, separators=(",", ":"))


@mcp.resource("skills://categories")
def skills_categories() -> str:
    """Category counts (auto-loaded index — no tool call needed)."""
    from collections import Counter
    c: Counter[str] = Counter()
    for cat in registry.list_categories():
        c[cat["category"]] += cat["count"]
    if not _skip_agents:
        for cat in agent_registry.list_categories():
            c[cat["category"]] += cat["count"]
    return json.dumps(
        {k: v for k, v in sorted(c.items(), key=lambda x: -x[1])},
        separators=(",", ":"),
    )


@mcp.resource("skills://stats")
def skills_stats() -> str:
    """Statistics about the library."""
    cats = sorted({c["category"] for c in registry.list_categories()})
    return json.dumps({
        "total_skills": registry.count,
        "total_agents": agent_registry.count,
        "categories": cats,
        "skills_directory": str(SKILLS_DIR),
        "agents_directory": str(AGENTS_DIR),
    }, indent=2)


# ══════════════════════════════════════════════════════════════════════
#  MAIN — entry point with transport selection
# ══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="MCP Skills Server")
    parser.add_argument(
        "--transport", choices=["stdio", "sse"], default="stdio",
        help="Transport mode: 'stdio' for pipe-based (default), 'sse' for HTTP"
    )
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="localhost")
    args = parser.parse_args()

    print(f"🚀 Starting MCP Skills Server ({args.transport} mode)", file=sys.stderr)
    print(f"   📂 Skills: {SKILLS_DIR} ({registry.count} loaded)", file=sys.stderr)
    print(f"   🤖 Agents: {AGENTS_DIR} ({agent_registry.count} loaded)", file=sys.stderr)

    if args.transport == "sse":
        print(f"   🌐 HTTP: http://{args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()

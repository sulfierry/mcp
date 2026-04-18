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

# SKILLS_CATEGORY_FILTER: comma-separated categories to expose. Empty = all.
# Match against overlay index (skills_index.json) category field.
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

# Agent registry — filter only if AGENTS_CATEGORY_FILTER is set; otherwise expose all.
_agent_cat_env = os.environ.get("AGENTS_CATEGORY_FILTER", "").strip()
_agent_cat_filter = [c for c in _agent_cat_env.split(",") if c.strip()] if _agent_cat_env else None

agent_registry = SkillRegistry(str(AGENTS_DIR), kind="agent", category_filter=_agent_cat_filter)
agent_count = 0
if AGENTS_DIR.exists():
    agent_count = agent_registry.scan()
    print(f"🤖 Agent Registry loaded: {agent_count} agents discovered", file=sys.stderr)


def _registries_for(kind: str) -> list[SkillRegistry]:
    """Resolve registries matching kind filter ('', 'skill', 'agent')."""
    k = (kind or "").lower()
    if k == "skill":
        return [registry]
    if k == "agent":
        return [agent_registry]
    return [registry, agent_registry]

# ── Create MCP Server ────────────────────────────────────────────────

mcp = FastMCP("Skills MCP Server")


# ══════════════════════════════════════════════════════════════════════
#  TOOLS — callable functions for the AI agent
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_skills(
    limit: int = 50,
    offset: int = 0,
    category: str = "",
    kind: str = "",
    compact: bool = True,
) -> str:
    """List skills and agents with pagination (registry holds 1000+ entries).

    Args:
        limit: Max entries per page (default 50, 0 for all — large).
        offset: Pagination offset.
        category: Filter by exact category (use list_categories to discover).
        kind: Filter by "skill" or "agent". Empty = both.
        compact: If True (default), omits description.

    Returns JSON with {total, offset, limit, count, has_more, skills}.
    Each entry has a `kind` field. Prefer search_skills for targeted discovery.
    """
    merged: list[dict] = []
    total = 0
    for reg in _registries_for(kind):
        res = reg.list_skills(limit=0, offset=0, category=category, compact=compact)
        for item in res["skills"]:
            item["kind"] = reg.kind
        merged.extend(res["skills"])
        total += res["total"]

    merged.sort(key=lambda x: x["name"].lower())
    if limit <= 0:
        limit = total
    page = merged[offset: offset + limit]
    return json.dumps({
        "total": total,
        "offset": offset,
        "limit": limit,
        "count": len(page),
        "has_more": offset + len(page) < total,
        "skills": page,
    }, indent=2)


@mcp.tool()
def list_categories(kind: str = "") -> str:
    """Return counts per category across skills and/or agents."""
    from collections import Counter
    c: Counter[str] = Counter()
    for reg in _registries_for(kind):
        for cat in reg.list_categories():
            c[cat["category"]] += cat["count"]
    cats = [{"category": k, "count": v} for k, v in sorted(c.items(), key=lambda x: -x[1])]
    return json.dumps({"total_categories": len(cats), "categories": cats}, indent=2)


@mcp.tool()
def search_skills(
    query: str,
    limit: int = 20,
    kind: str = "",
    compact: bool = False,
) -> str:
    """Search skills and agents by keyword.

    Args:
        query: Search terms (e.g., 'molecular docking', 'python backend').
        limit: Max results (default 20).
        kind: "" (both), "skill", or "agent".
        compact: Omit description if True.
    """
    scored: list[dict] = []
    for reg in _registries_for(kind):
        for r in reg.search_skills(query, limit=limit, compact=compact):
            r["kind"] = reg.kind
            scored.append(r)
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)
    scored = scored[:limit]
    if not scored:
        return json.dumps({"message": f"No matches for '{query}'.", "count": 0})
    return json.dumps({"query": query, "count": len(scored), "results": scored}, indent=2)


@mcp.tool()
def get_skill(skill_id: str, section: str = "", kind: str = "") -> str:
    """Get SKILL.md content. Optional section filter returns one H2 block.

    Args:
        skill_id: Directory name, e.g. 'molecular-docking'.
        section: Substring of H2 title (case-insensitive). Empty = full file.
        kind: "" tries skills first then agents; "skill" or "agent" forces one.
    """
    for reg in _registries_for(kind):
        entry = reg.get_skill(skill_id, section=section)
        if entry:
            entry["kind"] = reg.kind
            return json.dumps(entry, indent=2)
    return json.dumps({
        "error": f"'{skill_id}' not found in {kind or 'skills or agents'}.",
        "suggestion": "Use search_skills(query) to find a valid id.",
    })


@mcp.tool()
def list_sections(skill_id: str, kind: str = "") -> str:
    """List H2 section titles for a skill or agent (cheap TOC — no body)."""
    for reg in _registries_for(kind):
        titles = reg.list_sections(skill_id)
        if titles is not None:
            return json.dumps({"skill_id": skill_id, "kind": reg.kind, "sections": titles})
    return json.dumps({"error": f"'{skill_id}' not found."})


@mcp.tool()
def get_skill_scripts(skill_id: str, kind: str = "") -> str:
    """Get helper scripts from scripts/ subdirectory of a skill or agent.

    Args:
        skill_id: The identifier (directory name).
        kind: "" tries skills then agents; "skill" or "agent" forces one.
    """
    for reg in _registries_for(kind):
        scripts = reg.get_scripts(skill_id)
        if scripts is not None:
            return json.dumps({"skill_id": skill_id, "kind": reg.kind, "scripts": scripts}, indent=2)
    return json.dumps({"message": f"No scripts found for '{skill_id}'."})


# ══════════════════════════════════════════════════════════════════════
#  RESOURCES — data endpoints the agent can read
# ══════════════════════════════════════════════════════════════════════

@mcp.resource("skills://catalog")
def skills_catalog() -> str:
    """Compact catalog: id + name + category only (no descriptions).

    Full SKILL.md content is available via get_skill(). Kept lean to avoid
    flooding the context window on resource auto-load.
    """
    catalog = [
        {"id": s.id, "name": s.name, "category": s.category}
        for s in sorted(registry._skills.values(), key=lambda s: s.id)
    ]
    return json.dumps({"count": len(catalog), "catalog": catalog})


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
    parser.add_argument(
        "--port", type=int, default=8765,
        help="Port for SSE transport (default: 8765)"
    )
    parser.add_argument(
        "--host", default="localhost",
        help="Host for SSE transport (default: localhost)"
    )
    args = parser.parse_args()

    print(f"🚀 Starting MCP Skills Server ({args.transport} mode)", file=sys.stderr)
    print(f"   📂 Skills: {SKILLS_DIR} ({registry.count} loaded)", file=sys.stderr)
    print(f"   🤖 Agents: {AGENTS_DIR} ({agent_registry.count} loaded)", file=sys.stderr)

    if args.transport == "sse":
        print(f"   🌐 HTTP: http://{args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        # show_banner=False is critical: FastMCP's Rich banner pollutes stdout,
        # breaking JSON-RPC communication in stdio transport mode.
        mcp.run(transport="stdio", show_banner=False)


if __name__ == "__main__":
    main()

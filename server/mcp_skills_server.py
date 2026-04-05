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
import sys
from pathlib import Path

from fastmcp import FastMCP
from skill_registry import SkillRegistry

# ── Configuration ─────────────────────────────────────────────────────

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
AGENTS_DIR = ROOT_DIR / "agents"

# ── Initialize Registry ──────────────────────────────────────────────

registry = SkillRegistry(str(SKILLS_DIR))
skill_count = registry.scan()
print(f"🧬 Skills Registry loaded: {skill_count} skills discovered", file=sys.stderr)

# ── Initialize Agent Registry (Phase 2 stub) ─────────────────────────

agent_registry = SkillRegistry(str(AGENTS_DIR))  # reuse same parser for AGENT.md
agent_count = 0
if AGENTS_DIR.exists():
    agent_count = agent_registry.scan()
    print(f"🤖 Agent Registry loaded: {agent_count} agents discovered", file=sys.stderr)

# ── Create MCP Server ────────────────────────────────────────────────

mcp = FastMCP("Skills MCP Server")


# ══════════════════════════════════════════════════════════════════════
#  TOOLS — callable functions for the AI agent
# ══════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_skills() -> str:
    """List all available skills with their name, ID, and description.
    
    Use this to discover what skills are available in the system.
    Returns a JSON array of skill summaries.
    """
    skills = registry.list_skills()
    if not skills:
        return json.dumps({"message": "No skills found. Run sync_skills.sh first.", "count": 0})
    return json.dumps({"count": len(skills), "skills": skills}, indent=2)


@mcp.tool()
def search_skills(query: str) -> str:
    """Search for skills matching a keyword or topic.
    
    Args:
        query: Search terms (e.g., 'molecular docking', 'protein structure', 'fastapi')
    
    Returns matching skills ranked by relevance score.
    """
    results = registry.search_skills(query)
    if not results:
        return json.dumps({"message": f"No skills found matching '{query}'.", "count": 0})
    return json.dumps({"query": query, "count": len(results), "results": results}, indent=2)


@mcp.tool()
def get_skill(skill_id: str) -> str:
    """Get the full SKILL.md content for a specific skill.
    
    Args:
        skill_id: The skill identifier (directory name), e.g., 'molecular-docking'
    
    Returns the complete skill documentation including instructions, 
    code examples, and best practices.
    """
    skill = registry.get_skill(skill_id)
    if not skill:
        available = [s["id"] for s in registry.list_skills()]
        return json.dumps({
            "error": f"Skill '{skill_id}' not found.",
            "suggestion": "Use list_skills() or search_skills() to find available skills.",
            "available_count": len(available),
        })
    return json.dumps(skill, indent=2)


@mcp.tool()
def get_skill_scripts(skill_id: str) -> str:
    """Get helper scripts associated with a skill.
    
    Args:
        skill_id: The skill identifier (directory name)
    
    Returns script files from the skill's scripts/ subdirectory, if any.
    """
    scripts = registry.get_scripts(skill_id)
    if scripts is None:
        return json.dumps({"message": f"No scripts found for skill '{skill_id}'."})
    return json.dumps({"skill_id": skill_id, "scripts": scripts}, indent=2)


@mcp.tool()
def list_agents() -> str:
    """List available specialist agents (Phase 2 — agent personas).
    
    Returns a JSON array of agent summaries. Agents are specialist 
    personas that combine multiple skills with an expert system prompt.
    """
    agents = agent_registry.list_skills()
    if not agents:
        return json.dumps({
            "message": "No agents configured yet. Add AGENT.md files to the agents/ directory.",
            "count": 0
        })
    return json.dumps({"count": len(agents), "agents": agents}, indent=2)


@mcp.tool()
def get_agent(agent_id: str) -> str:
    """Get the full configuration for a specialist agent.
    
    Args:
        agent_id: The agent identifier (directory name), e.g., 'bioinformatics-researcher'
    """
    agent = agent_registry.get_skill(agent_id)
    if not agent:
        available = [a["id"] for a in agent_registry.list_skills()]
        return json.dumps({
            "error": f"Agent '{agent_id}' not found.",
            "available_agents": available,
        })
    return json.dumps(agent, indent=2)


@mcp.tool()
def search_agents(query: str) -> str:
    """Search for specialist agents matching a keyword or task description.
    
    Args:
        query: Search terms (e.g., 'python backend', 'ui design', 'scientific writing')
    
    Returns matching agents ranked by relevance. Use this when you need 
    to find the right specialist persona for a task.
    """
    results = agent_registry.search_skills(query)
    if not results:
        return json.dumps({"message": f"No agents matching '{query}'.", "count": 0})
    return json.dumps({"query": query, "count": len(results), "results": results}, indent=2)


# ══════════════════════════════════════════════════════════════════════
#  RESOURCES — data endpoints the agent can read
# ══════════════════════════════════════════════════════════════════════

@mcp.resource("skills://catalog")
def skills_catalog() -> str:
    """Full JSON catalog of all available skills."""
    catalog = registry.export_catalog()
    return json.dumps({"count": len(catalog), "catalog": catalog}, indent=2)


@mcp.resource("skills://stats")
def skills_stats() -> str:
    """Statistics about the skills library."""
    skills = registry.list_skills()
    categories = set()
    for s in skills:
        if s.get("category"):
            categories.add(s["category"])

    return json.dumps({
        "total_skills": len(skills),
        "total_agents": agent_registry.count,
        "categories": sorted(categories),
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
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

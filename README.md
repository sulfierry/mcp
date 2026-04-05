# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server that exposes curated AI agent skills as callable tools. Combines development skills, bioinformatics workflows, and scientific computing capabilities from multiple reference repositories into a unified, searchable skill library.

## Architecture

```
MCP Client (Antigravity / Claude Desktop / Cursor)
        │
        ▼ (stdio or SSE)
┌─────────────────────────────────┐
│   FastMCP Server (localhost)    │
│                                 │
│  Tools:                         │
│   • list_skills()               │
│   • search_skills(query)        │
│   • get_skill(skill_id)         │
│   • get_skill_scripts(id)       │
│   • list_agents()               │
│   • get_agent(agent_id)         │
│                                 │
│  Resources:                     │
│   • skills://catalog            │
│   • skills://stats              │
└────────┬────────────────────────┘
         │
    ┌────▼────┐     ┌──────────┐
    │ skills/ │     │ agents/  │
    │ 30+ md  │     │ 2 agents │
    └─────────┘     └──────────┘
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/sulfierry/skills.git
cd skills

# 2. Sync skills from reference repositories
chmod +x scripts/sync_skills.sh start_server.sh
./scripts/sync_skills.sh

# 3. Start the server
./start_server.sh           # stdio mode (Claude Desktop / Antigravity)
./start_server.sh --sse     # HTTP mode (localhost:8765)
```

## Skills Library

### Custom Bioinformatics Skills

| Skill | Description |
|-------|-------------|
| `molecular-docking` | AutoDock Vina, DiffDock, virtual screening pipelines |
| `protein-structure-analysis` | Biotite-based 3D structure analysis, contact maps, binding sites |
| `kinase-interaction-modeling` | DT-Kinase Level 4 CNN, embedding adapters, DTI prediction |
| `drug-target-interaction` | ChEMBL data retrieval, molecular fingerprints, interaction networks |

### Synced Skills (from reference repos)

Skills are sourced from:
- [guanyang/antigravity-skills](https://github.com/guanyang/antigravity-skills) — Python, FastAPI, architecture, AI/ML
- [rmyndharis/antigravity-skills](https://github.com/rmyndharis/antigravity-skills) — MCP builder, planning, workflows
- [GPTomics/bioSkills](https://github.com/GPTomics/bioSkills) — 426 bioinformatics skills (genomics, proteomics, etc.)
- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) — 134 scientific/research skills
- [jaechang-hits/SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) — 196 life sciences skills
- [ClawBio/ClawBio](https://github.com/ClawBio/ClawBio) — 43 executable bioinformatics skills

Run `./scripts/sync_skills.sh --all` to sync everything, or use the default curated set.

## Specialist Agents (Phase 2)

| Agent | Description |
|-------|-------------|
| `bioinformatics-researcher` | Computational biology expert persona |
| `docking-specialist` | Molecular docking campaign specialist |

Agents are specialist personas that chain multiple skills together with expert system prompts. They are exposed via `list_agents()` and `get_agent()` MCP tools.

## MCP Client Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skills": {
      "command": "python",
      "args": ["/Users/sulfierry/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/sulfierry/skills/server"
      }
    }
  }
}
```

### Antigravity / Gemini

Symlink to global skills directory:

```bash
ln -s /Users/sulfierry/skills/skills ~/.gemini/antigravity/skills
```

### SSE Mode (HTTP)

For any client that supports SSE transport:

```bash
./start_server.sh --sse 8765
# Server available at http://localhost:8765
```

## Development

```bash
# Generate/update the skills catalog
python scripts/build_catalog.py

# Test the registry directly
python -c "
from server.skill_registry import SkillRegistry
r = SkillRegistry('skills')
r.scan()
print(f'Skills loaded: {r.count}')
for s in r.search_skills('protein'):
    print(f'  {s[\"id\"]}: {s[\"name\"]} (score: {s[\"score\"]})')
"
```

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP SDK](https://gofastmcp.com/)
- [Agent Skills Specification](https://agentskills.io/)

## License

MIT
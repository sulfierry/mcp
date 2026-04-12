# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server built on a **Dual-Core Architecture**: combining **Autonomous Deep Research** with **State-of-the-Art (SOTA) Engineering**. It exposes **573 curated AI agent skills** as callable tools — covering bioinformatics, drug discovery, scientific writing, polyglot algorithms (C++/Python), and complete agentic orchestration — all running on `localhost` for privacy and low latency.

## 📊 At a Glance

| Metric | Value |
|--------|-------|
| **Skills** | 573 |
| **Mega-Workflows** | 6 Core Modalities |
| **Agent Personas** | Dual-Core Squad |
| **Source Repositories** | 12 |
| **MCP Tools** | 7 |
| **Transport** | stdio + SSE (HTTP) |

---

## 🚀 Quick Start (3 steps)

### 1. Clone and install dependencies

```bash
git clone https://github.com/sulfierry/mcp.git
cd mcp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install fastmcp pyyaml
```

### 2. Sync skills and auto-configure IDEs

```bash
chmod +x scripts/sync_skills.sh start_server.sh

# Sync curated skills (recommended)
./scripts/sync_skills.sh

# OR sync ALL available skills
./scripts/sync_skills.sh --all

# List available source repos
./scripts/sync_skills.sh --list
```

The script runs **4 phases** automatically:

| Phase | What it does |
|-------|--------------|
| **1. Sync** | Clones 12 repos and copies skills into `skills/` |
| **2. Merge** | Copies agents from `agents/` → `skills/` for universal discovery |
| **3. Symlinks** | Creates links for Antigravity, Claude Code CLI, and VS Code Copilot |
| **4. Catalog** | Rebuilds `skills_index.json` with all indexed skills |

> **Do I need to run `sync_skills.sh`?** Only the **first time** (to populate `skills/`) or when you want to update. If `skills/` already contains 573 folders, **you don't need to run it again**.

### 3. Register the MCP Server in your preferred IDE

Choose one or more options below (**all** can coexist):

---

## 💡 What is MCP? (Simple explanation)

**MCP (Model Context Protocol)** is a "remote control" that gives **extra powers** to an AI. Without MCP, the AI only talks based on its training memory. With MCP, it can search databases, run scripts, access APIs — anything the server provides.

### Analogy

Imagine the AI chatting with you:

```
Without MCP:
  You:  "What's the 3D structure of the BRAF protein?"
  AI:   "I know it's a kinase..." (generic answer, from memory)

With MCP:
  You:  "What's the 3D structure of the BRAF protein?"
  AI:   → calls search_skills("protein structure")
        → finds the 'struct-predictor' skill
        → follows instructions to query the PDB
  AI:   "The crystal structure of BRAF (PDB: 6U2G) shows..."
        (specific answer, with real data)
```

### Server lifecycle

The MCP server does **NOT** run permanently in the background:

```
You are NOT using the IDE:
  MCP server? 💤 OFF (zero resources)

You open the IDE (Antigravity, Claude Code, VS Code...):
  IDE reads config → starts skills-server automatically
  MCP server? 🟢 ON (~10MB RAM)
  AI gains tools: search_skills(), get_skill(), etc.

You close the IDE:
  MCP server? 💤 OFF automatically
```

### How it works

```
          You type a prompt
                  │
                  ▼
      ┌──────────────────────┐
      │   IDE (the "brain")   │  Antigravity, Claude Code, VS Code...
      └──────────┬───────────┘
                 │ stdio (text via terminal)
                 ▼
      ┌──────────────────────┐
      │   MCP Skills Server  │  The "assistant" with extra powers
      │                      │
      │  Available tools:    │
      │  • search_skills()   │  "search 'docking' across 573 skills"
      │  • get_skill()       │  "give me the full SKILL.md for skill X"
      │  • search_agents()   │  "which agent understands proteins?"
      │  • list_skills()     │  "list all available skills"
      └──────────┬───────────┘
                 │
         ┌───────┴───────┐
         │  skills/  573 │  ← SKILL.md files from 12 repos
         │  agents/   10 │  ← Agent personas (Dual-Core)
         └───────────────┘
```

### Symlink vs MCP Server — why have both?

| | Symlink | MCP Server |
|---|---|---|
| **How it works** | AI sees all skills listed at the start of the conversation | AI has **tools** to search and read skills on demand |
| **Analogy** | Having the library catalog on your desk | Having a librarian who fetches the right book |
| **Advantage** | Automatic passive discovery | Intelligent search by keyword |
| **Limitation** | Loads many names into context | Requires a Python process running |

**Having both is the ideal setup** — the catalog shows what exists, the librarian fetches the right book when needed.

---

## 🏗 Architecture

> The ecosystem leverages exactly **573** modular skills and **10** specialized agent personas to dynamically respond to queries via the Dual-Core engine.

```
MCP Client (Antigravity / Claude Code / VS Code / Cursor)
        │
        ▼ (stdio or SSE)
┌──────────────────────────────────────────┐
│      FastMCP Server (localhost)          │
│                                          │
│  Tools:                  Resources:      │
│   • list_skills()         • skills://    │
│   • search_skills(q)        catalog      │
│   • get_skill(id)         • skills://    │
│   • get_skill_scripts(id)   stats        │
│   • list_agents()                        │
│   • search_agents(q)                     │
│   • get_agent(id)                        │
└──────────┬───────────────────────────────┘
           │
   ┌───────┴───────┐
   │  skills/ 573  │   ← SKILL.md files from 12 repos
   │  agents/ 10   │   ← Agent personas (Dual-Core)
   └───────────────┘
```

---

## 🤖 Agent Personas (Core Team)

> **Architectural Note:** The ecosystem runs under the **"Dual-Core"** paradigm, separating Cutting-Edge Scientific Research from Code Implementation (SOTA Engineering).

### 🔬 Deep Research & Scientific Discovery
| Agent | ID | Description |
|-------|-----|-------------|
| Deep Researcher | `deep-researcher` | Deep web investigation, complex literature, citations |
| Investigative Orchestrator | `investigative-orchestrator` | Breaking down complex questions via sequential/parallel thinking |
| Bioinformatics Researcher | `bioinformatics-researcher` | Computational biology, protein analysis, omics |
| Scientific Writer | `scientific-writer` | Research → writing → citation → LaTeX |

### 🚀 Elite State-of-the-Art Engineering (SOTA)
| Agent | ID | Description |
|-------|-----|-------------|
| SOTA Engineer | `state-of-the-art-engineer` | Polyglot architect (C++/Python/UI). DOD & Memory Safety. |
| Algorithmic Thinker | `algorithmic-thinker` | Chain-of-Thought approach & O(N) complexity mapping |
| Self-Improving Agent | `self-improving-agent` | Traceback-based self-healing & regression prevention |
| MCP Server Builder | `mcp-server-builder` | C++/Python infrastructure, Protocols & API Boundaries |

### 💻 Base Programming & DevOps
| Agent | ID | Description |
|-------|-----|-------------|
| Python Architect | `python-architect` | Clean architecture, async, typing, packaging |
| DevSecOps Expert | `ai-security-auditor` | Master SecOps, AI Vetting & environment protection |
| Code Reviewer | `code-reviewer` | Multi-dimensional scoring review with red flags |

---

## 📚 Skills Library

### Custom Skills (manually written)

| Skill | Category | Description |
|-------|----------|-------------|
| `scientific-paper-writer` | 📝 Writing | IMRaD, Nature/IEEE/NeurIPS/APA7 templates |
| `literature-review` | 📝 Writing | PubMed/arXiv/Semantic Scholar + PRISMA |
| `peer-reviewer` | 📝 Writing | 0-100 scoring across 8 dimensions |
| `thesis-writer` | 📝 Writing | PhD chapters, defense, LaTeX templates |
| `latex-manuscript` | 📝 Writing | Compilation, figures, latexdiff |
| `grant-proposal-writer` | 📝 Writing | NSF/NIH + FAPESP/CAPES/CNPq 🇧🇷 |
| `data-extractor` | 📝 Writing | Digitize paper figures (26+ plot types) |
| `molecular-docking` | 🧬 Bio | AutoDock Vina, DiffDock, virtual screening |
| `protein-structure-analysis` | 🧬 Bio | Biotite 3D, contact maps, binding sites |
| `kinase-interaction-modeling` | 🧬 Bio | DT-Kinase Level 4 CNN, DTI prediction |
| `drug-target-interaction` | 🧬 Bio | ChEMBL, molecular fingerprints |

### Synced Skills (from 12 repositories)

| Repository | ⭐ | Skills | Focus |
|------------|-----|--------|-------|
| VoltAgent/awesome-claude-code-subagents | 16.2K | 100+ | Full-stack, DevOps, ML, meta-orchestration |
| tech-leads-club/agent-skills | 2K | 20+ | Security-audited, multi-platform |
| ClawBio/ClawBio | — | 43 | Genomics, PGx, clinical |
| GPTomics/bioSkills | — | 426 | Proteomics, RNA-seq, single-cell |
| **K-Dense-AI/scientific-agent-skills** | **—** | **133** | **Drug discovery, scRNA-seq, genomics, ML, clinical, 78 databases, lab automation** |
| jaechang-hits/SciAgent-Skills | — | 196 | Life sciences |
| K-Dense-AI/claude-scientific-writer | 1.4K | 10 | Citation, peer review, slides |
| zhangchenhaobest/academic-research-skills | — | 4 | Deep research, pipeline |
| guanyang/antigravity-skills | — | 20+ | Python, FastAPI, architecture |
| rmyndharis/antigravity-skills | — | 20+ | MCP, planning, workflows |

---

## 🔌 IDE Setup — Step by Step

### Option A: Claude Code CLI

Claude Code discovers skills in **two** complementary ways:

#### Method 1: Symlink (passive auto-discovery)

Already created automatically by `sync_skills.sh`:

```bash
~/.claude/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Method 2: MCP Server via CLI (active search — recommended)

```bash
# Register globally (available in all projects)
claude mcp add --scope user skills-server \
  /Users/$USER/mcp/.venv/bin/python3 \
  /Users/$USER/mcp/server/mcp_skills_server.py
```

Useful commands:

```bash
claude mcp list                    # View configured servers
claude mcp get skills-server       # Server details
claude mcp remove skills-server    # Remove server
```

---

### Option B: VS Code (GitHub Copilot + MCP)

#### Method 1: Native Copilot skills (auto-discovery)

Already created automatically by `sync_skills.sh`:

```bash
.github/skills/ → /Users/$USER/mcp/skills/   # (symlink in project)
```

> **Monorepo tip:** Enable `"chat.useCustomizationsInParentRepositories": true` in `settings.json`.

#### Method 2: MCP Server (advanced search tools)

Add to `.vscode/mcp.json` (per-project) or global `settings.json` (`Cmd+Shift+P` → `Preferences: Open User Settings (JSON)`):

```json
{
  "servers": {
    "skills-server": {
      "command": "/Users/$USER/mcp/.venv/bin/python3",
      "args": ["/Users/$USER/mcp/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/mcp/server"
      }
    }
  }
}
```

---

### Option C: Google Antigravity (Gemini)

#### Method 1: Symlink (auto-discovery)

Already created automatically by `sync_skills.sh`:

```bash
~/.gemini/antigravity/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Method 2: MCP Server (recommended)

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/mcp/.venv/bin/python3",
      "args": ["/Users/$USER/mcp/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/mcp/server"
      }
    }
  }
}
```

---

### Option D: Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/mcp/.venv/bin/python3",
      "args": ["/Users/$USER/mcp/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/mcp/server"
      }
    }
  }
}
```

---

### Option E: Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/mcp/.venv/bin/python3",
      "args": ["/Users/$USER/mcp/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/mcp/server"
      }
    }
  }
}
```

---

### Option F: HTTP/SSE Mode (any client)

For clients that support SSE/HTTP transport:

```bash
# Start the HTTP server
source .venv/bin/activate
PYTHONPATH=server python3 server/mcp_skills_server.py --transport sse --port 8765
```

Server available at `http://localhost:8765/sse`. Configure your MCP client with:

```json
{
  "mcpServers": {
    "skills-server": {
      "url": "http://localhost:8765/sse"
    }
  }
}
```

---

### ✅ Verification

After configuring any option, verify:

```bash
# Claude Code CLI
claude mcp list

# Or in any IDE, ask:
"list your available MCP tools"
```

You should see 7 available tools: `list_skills`, `search_skills`, `get_skill`, `get_skill_scripts`, `list_agents`, `search_agents`, `get_agent`.

---

## 🛠 MCP Tools Reference

| Tool | Description | Example |
|------|-------------|---------|
| `list_skills()` | List all skills | "What skills do you have?" |
| `search_skills(query)` | Search by keyword | `search_skills("protein docking")` |
| `get_skill(id)` | Full skill content | `get_skill("molecular-docking")` |
| `get_skill_scripts(id)` | Helper scripts | `get_skill_scripts("seq-wrangler")` |
| `list_agents()` | List available agents | "Show me all agents" |
| `search_agents(query)` | Search agents by keyword | `search_agents("python backend")` |
| `get_agent(id)` | Full agent configuration | `get_agent("fullstack-developer")` |

---

## 🧪 Development

```bash
# Activate environment
source .venv/bin/activate

# Generate/update catalog
PYTHONPATH=server python3 scripts/build_catalog.py

# Test the registry directly
PYTHONPATH=server python3 -c "
from skill_registry import SkillRegistry
r = SkillRegistry('skills'); r.scan()
print(f'Skills: {r.count}')
for s in r.search_skills('protein'):
    print(f'  {s[\"id\"]}: {s[\"name\"]} (score: {s[\"score\"]})')
"

# Test the server (SSE mode for debug)
PYTHONPATH=server python3 server/mcp_skills_server.py --transport sse --port 8765
# → http://localhost:8765
```

### Adding a new skill

```bash
# 1. Create directory
mkdir -p skills/my-skill

# 2. Create SKILL.md with frontmatter
cat > skills/my-skill/SKILL.md << 'EOF'
---
name: My Skill
description: "Short description of the skill."
category: my-category
tags: tag1, tag2, tag3
---

# My Skill

## Use this skill when
- Use case 1
- Use case 2

## Instructions
Detailed instructions here...
EOF

# 3. Rebuild catalog
PYTHONPATH=server python3 scripts/build_catalog.py
```

### Adding a new agent

```bash
mkdir -p agents/my-agent
# Same SKILL.md format, but with a 'skills:' field in frontmatter
```

---

## 📖 References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP SDK](https://gofastmcp.com/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Agent Skills Standard](https://agentskills.io/)
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- [VoltAgent Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Tech Leads Club Agent Skills](https://github.com/tech-leads-club/agent-skills)

## 📄 License

GNU General Public License v3.0
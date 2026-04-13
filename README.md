# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server built on a **Dual-Core Architecture**: combining **Autonomous Deep Research** with **State-of-the-Art (SOTA) Engineering**. It exposes **1,176 curated AI agent skills** as callable tools — covering bioinformatics, drug discovery, scientific writing, systems programming (C/C++/CUDA), HPC, evolutionary optimization, and complete agentic orchestration — all running on `localhost` for privacy and low latency.

> **Supported IDEs:** Antigravity (Gemini) · Claude Code CLI · Claude Desktop · VS Code (Copilot) · Cursor · OpenAI Codex CLI · Qwen CLI · Any MCP-compatible client (HTTP/SSE)

## 📊 At a Glance

| Metric | Value |
|--------|-------|
| **Skills** | 1,176 |
| **Mega-Workflows** | 6 Core Modalities |
| **Agent Personas** | Dual-Core Squad + Low-Level |
| **Source Repositories** | 10 |
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
| **1. Sync** | Clones 10 repos (flat + nested scan) and copies skills into `skills/` |
| **2. Merge** | Copies agents from `agents/` → `skills/` for universal discovery |
| **3. Symlinks** | Creates links for Antigravity, Claude Code CLI, VS Code Copilot, and OpenAI Codex CLI |
| **4. Catalog** | Rebuilds `skills_index.json` with all indexed skills |

> **Do I need to run `sync_skills.sh`?** Only the **first time** (to populate `skills/`) or when you want to update. If `skills/` already has 1,000+ folders, **you don't need to run it again**.

### 3. Register the MCP Server in your preferred IDE

Choose one or more options below (**all** can coexist):

> **Do I need to activate MCP manually?** No. **All** supported IDEs and CLIs load MCP servers automatically from their config files on startup:
>
> | IDE / CLI | Config file | How to verify |
> |-----------|-------------|---------------|
> | **Antigravity (Gemini)** | `~/.gemini/settings.json` | Ask: *"list your MCP tools"* |
> | **Claude Code CLI** | `claude mcp add` (stored in `~/.claude/`) | `claude mcp list` |
> | **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` | Settings → Developer → MCP |
> | **VS Code (Copilot)** | `.vscode/mcp.json` or global `settings.json` | Copilot chat → *"list MCP tools"* |
> | **Cursor** | `~/.cursor/mcp.json` | Settings → MCP |
> | **OpenAI Codex CLI** | `~/.codex/config.toml` | Tool list in Codex TUI |
> | **Qwen CLI** | `~/.qwen/settings.json` | `/mcp` inside Qwen TUI |
>
> After running `sync_skills.sh`, just open any of these and the 7 MCP tools will be available immediately. No manual activation needed.

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
      │  • search_skills()   │  "search 'docking' across 1,176 skills"
      │  • get_skill()       │  "give me the full SKILL.md for skill X"
      │  • search_agents()   │  "which agent understands proteins?"
      │  • list_skills()     │  "list all available skills"
      └──────────┬───────────┘
                 │
         ┌───────┴───────┐
         │  skills/ 1,176 │  ← SKILL.md files from 10 repos + custom
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

> The ecosystem leverages **1,176** modular skills and **10+** specialized agent personas to dynamically respond to queries via the Dual-Core engine.

```
MCP Client (Antigravity / Claude Code / VS Code / Cursor / OpenAI Codex)
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
   ┌───────┴────────┐
   │ skills/ 1,176  │   ← SKILL.md files from 10 repos + custom
   │  agents/ 10    │   ← Agent personas (Dual-Core)
   └────────────────┘
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

### ⚙️ Low-Level & Systems
| Agent | ID | Description |
|-------|-----|-------------|
| Systems Engineer | `systems-engineer` | Orchestrates C/C++, kernel, embedded, networking, GPU skills |
| HPC Engineer | `hpc-engineer` | MPI, OpenMP, SLURM, GPU clusters, parallel algorithms |

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

### Synced Skills (from 10 repositories)

| Repository | Skills | Focus |
|------------|--------|-------|
| ClawBio/ClawBio | 47 | Genomics, PGx, clinical, pharmacogenomics |
| K-Dense-AI/scientific-agent-skills | 134 | Drug discovery, scRNA-seq, genomics, ML, clinical, 78 databases, lab automation |
| GPTomics/bioSkills | 438 | Proteomics, RNA-seq, single-cell, spatial transcriptomics, metagenomics, variant calling |
| jaechang-hits/SciAgent-Skills | 197 | Cell biology, biostatistics, drug discovery, imaging, lab automation |
| K-Dense-AI/claude-scientific-writer | 81 | Scientific writing, citation, peer review, slides |
| zhangchenhaobest/academic-research-skills | 4 | Deep research, academic pipeline |
| VoltAgent/awesome-claude-code-subagents | 100+ | Full-stack, DevOps, ML, meta-orchestration |
| tech-leads-club/agent-skills | 77 | Security-audited, multi-platform engineering |
| guanyang/antigravity-skills | 59 | Python, FastAPI, architecture, context management |
| rmyndharis/antigravity-skills | 305 | MCP, planning, workflows, polyglot programming |

### Custom Skills (low-level & optimization)

| Skill | Category | Description |
|-------|----------|-------------|
| `c-systems-programming` | ⚙️ Low-Level | POSIX syscalls, IPC, signals, fork/exec, file descriptors |
| `embedded-c` | ⚙️ Low-Level | Bare-metal, FreeRTOS/Zephyr, linker scripts, MMIO, DMA |
| `low-level-debugging` | ⚙️ Low-Level | GDB/LLDB, Valgrind, ASAN/TSAN, perf, strace, core dumps |
| `compiler-internals` | ⚙️ Low-Level | LLVM passes, IR manipulation, Clang AST, codegen |
| `gpu-cuda-programming` | ⚙️ Low-Level | CUDA kernels, shared memory, warp shuffles, streams, Nsight |
| `network-programming-c` | ⚙️ Low-Level | BSD sockets, epoll/kqueue, zero-copy I/O, protocol framing |
| `kernel-module-dev` | ⚙️ Low-Level | Linux LKMs, char drivers, netfilter hooks, eBPF |
| `genetic-algorithms` | 🧮 Optimization | GA, GP, DE, CMA-ES, fitness landscape analysis, DEAP |
| `multi-objective-optimization` | 🧮 Optimization | NSGA-II/III, MOEA/D, Pareto analysis, quality indicators |

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

### Option G: OpenAI Codex CLI

The Codex CLI uses **3 integration points**, all auto-configured by `sync_skills.sh`:

#### Method 1: Symlink (passive discovery)

Already created automatically by `sync_skills.sh`:

```bash
~/.codex/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Method 2: AGENTS.md (global instructions)

The sync script auto-generates `~/.codex/AGENTS.md` with skill catalog instructions. You can customize it:

```markdown
# ~/.codex/AGENTS.md

You have access to **1,176+ curated AI agent skills** via an MCP server.
Use the following MCP tools to discover and load skills on demand:

- `list_skills()` — list all available skills
- `search_skills(query)` — search by keyword
- `get_skill(id)` — get full SKILL.md content
- `list_agents()` — list agent personas
- `search_agents(query)` — search agents by keyword

Local skills directory: `~/.codex/skills/`
```

#### Method 3: MCP Server via config.toml (recommended)

The sync script auto-appends MCP configuration to `~/.codex/config.toml`. You can also configure it manually:

```toml
# ~/.codex/config.toml

[mcp]
servers = { skills-server = { command = "/Users/$USER/mcp/.venv/bin/python3", args = ["/Users/$USER/mcp/server/mcp_skills_server.py"] } }
```

For project-level configuration, create `.codex/config.toml` in your repo root:

```toml
# .codex/config.toml (project-level)

[mcp]
servers = { skills-server = { command = "/Users/$USER/mcp/.venv/bin/python3", args = ["/Users/$USER/mcp/server/mcp_skills_server.py"] } }
```

> **Tip:** Use `codex --help` and the `/init` command inside Codex TUI to scaffold additional `AGENTS.md` files per project.

---

### Option H: Qwen CLI

Qwen Code discovers skills in **two** complementary ways:

#### Method 1: Symlink (passive discovery)

Already created automatically by `sync_skills.sh`:

```bash
~/.qwen/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Method 2: MCP Server via settings.json (recommended)

The sync script auto-generates `~/.qwen/settings.json`. You can also configure it manually:

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

For project-level configuration, create `.qwen/settings.json` in your repo root with the same format.

> **Do I need to activate MCP manually?** No. Qwen CLI loads all servers from `~/.qwen/settings.json` automatically on startup. Just run `qwen` and the skills-server will be available immediately. No extra steps needed.

#### Verification

```bash
# Option A: CLI command to add/verify
qwen mcp add --scope user skills-server /Users/$USER/mcp/.venv/bin/python3 /Users/$USER/mcp/server/mcp_skills_server.py
qwen mcp list                    # verify server is registered

# Option B: Inside Qwen TUI
/mcp                             # list connected servers and tools
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
# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server that exposes **450+ curated AI agent skills** and **10 specialist agent personas** as callable tools. Covers bioinformatics, scientific writing, full-stack development, DevOps, and more — all running on `localhost` for privacy and low latency.

## 📊 At a Glance

| Metric | Value |
|--------|-------|
| **Skills** | 450+ |
| **Agent Personas** | 10 |
| **Source Repositories** | 12 |
| **MCP Tools** | 8 |
| **Transport** | stdio + SSE (HTTP) |

---

## 🏗 Architecture

```
MCP Client (Antigravity / VS Code / Claude Desktop / Cursor)
        │
        ▼ (stdio or SSE)
┌──────────────────────────────────────────┐
│      FastMCP Server (localhost)           │
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
   │  skills/ 450  │   ← SKILL.md files from 12 repos
   │  agents/ 10   │   ← Agent personas (SKILL.md)
   └───────────────┘
```

---

## 🚀 Quick Start (3 passos)

### 1. Clone e instale dependências

```bash
git clone https://github.com/sulfierry/skills.git
cd skills

# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install fastmcp pyyaml
```

### 2. Sincronize skills dos repositórios de referência

```bash
chmod +x scripts/sync_skills.sh start_server.sh

# Sincronizar skills curadas (recomendado)
./scripts/sync_skills.sh

# OU sincronizar TODAS as skills disponíveis
./scripts/sync_skills.sh --all

# Ver repositórios disponíveis
./scripts/sync_skills.sh --list
```

### 3. Inicie o servidor

```bash
# Modo stdio (para Antigravity, Claude Desktop, VS Code)
./start_server.sh

# Modo HTTP/SSE (para clientes web, testes, debug)
./start_server.sh --sse
# → Servidor em http://localhost:8765
```

---

## 🔌 Ativação Local — Passo a Passo

### Opção A: Google Antigravity (Gemini)

O Antigravity descobre skills automaticamente a partir do diretório `~/.gemini/antigravity/skills/`. Existem **duas formas** de ativar:

#### Método 1: Symlink (mais simples)

```bash
# Criar link simbólico para o diretório de skills
ln -sf /Users/$USER/skills/skills ~/.gemini/antigravity/skills
```

Pronto! O Antigravity vai encontrar todas as 450+ skills automaticamente ao iniciar a próxima conversa.

#### Método 2: MCP Server (mais poderoso)

Adicione ao arquivo `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/skills/.venv/bin/python3",
      "args": ["/Users/$USER/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/skills/server"
      }
    }
  }
}
```

> **Diferença**: o MCP Server expõe ferramentas de busca (`search_skills`, `search_agents`) que permitem ao Antigravity encontrar a skill certa automaticamente por keyword, enquanto o symlink apenas torna os arquivos visíveis.

---

### Opção B: VS Code (com extensão MCP)

#### Passo 1: Instalar a extensão MCP

No VS Code, instale uma das extensões compatíveis:
- **GitHub Copilot** (inclui suporte MCP nativo)
- **Continue** (extensão open-source com MCP)
- **Cline** (extensão para Claude com MCP)

#### Passo 2: Configurar o MCP Server

Adicione ao arquivo `.vscode/mcp.json` na raiz do seu projeto:

```json
{
  "servers": {
    "skills-server": {
      "command": "/Users/$USER/skills/.venv/bin/python3",
      "args": ["/Users/$USER/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/skills/server"
      }
    }
  }
}
```

Ou para configuração **global** (disponível em todos os projetos), adicione ao `settings.json` do VS Code:

```json
{
  "mcp.servers": {
    "skills-server": {
      "command": "/Users/$USER/skills/.venv/bin/python3",
      "args": ["/Users/$USER/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/skills/server"
      }
    }
  }
}
```

#### Passo 3: Verificar

Abra o painel de saída do VS Code (`Cmd+Shift+U`) e selecione "MCP" para ver os logs do servidor. Você deve ver:

```
🧬 Skills Registry loaded: 450 skills discovered
🤖 Agent Registry loaded: 10 agents discovered
🚀 Starting MCP Skills Server (stdio mode)
```

---

### Opção C: Claude Desktop

Adicione ao arquivo `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/skills/.venv/bin/python3",
      "args": ["/Users/$USER/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/skills/server"
      }
    }
  }
}
```

Reinicie o Claude Desktop. O ícone 🔌 deve aparecer indicando o MCP server conectado.

---

### Opção D: Cursor

Adicione ao arquivo `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "skills-server": {
      "command": "/Users/$USER/skills/.venv/bin/python3",
      "args": ["/Users/$USER/skills/server/mcp_skills_server.py"],
      "env": {
        "PYTHONPATH": "/Users/$USER/skills/server"
      }
    }
  }
}
```

---

### Opção E: Modo HTTP/SSE (qualquer cliente)

Para clientes que suportam transporte SSE/HTTP:

```bash
# Iniciar o servidor HTTP
source .venv/bin/activate
PYTHONPATH=server python3 server/mcp_skills_server.py --transport sse --port 8765
```

O servidor fica disponível em `http://localhost:8765/sse`. Configure seu cliente MCP com:

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

## 🤖 Agent Personas (10)

### 🧬 Bioinformatics
| Agent | ID | Descrição |
|-------|-----|-----------|
| Bioinformatics Researcher | `bioinformatics-researcher` | Computational biology, protein analysis, omics |
| Docking Specialist | `docking-specialist` | Molecular docking, virtual screening |

### 📝 Scientific Writing
| Agent | ID | Descrição |
|-------|-----|-----------|
| Scientific Writer | `scientific-writer` | Pipeline completo: pesquisa → escrita → citação → LaTeX |
| Academic Pipeline | `academic-pipeline` | 10 estágios com peer review e verificação de integridade |
| Deep Research | `deep-research` | 7 modos: full, quick, PRISMA, Socrático, fact-check |

### 💻 Programming & DevOps
| Agent | ID | Descrição |
|-------|-----|-----------|
| Full-Stack Developer | `fullstack-developer` | React/Next.js + FastAPI/Django + PostgreSQL + Docker |
| UI/UX Designer | `ui-ux-designer` | Design systems, WCAG 2.2, Figma→código |
| DevOps Engineer | `devops-engineer` | Docker, K8s, Terraform, CI/CD, monitoring |
| Python Architect | `python-architect` | Clean architecture, async, typing, packaging |
| Code Reviewer | `code-reviewer` | Review com scoring 6 dimensões, red flags de segurança |

---

## 📚 Skills Library

### Custom Skills (escritas manualmente)

| Skill | Categoria | Descrição |
|-------|-----------|-----------|
| `scientific-paper-writer` | 📝 Writing | IMRaD, templates Nature/IEEE/NeurIPS/APA7 |
| `literature-review` | 📝 Writing | PubMed/arXiv/Semantic Scholar + PRISMA |
| `peer-reviewer` | 📝 Writing | Scoring 0-100 em 8 dimensões |
| `thesis-writer` | 📝 Writing | Capítulos PhD, defesa, LaTeX templates |
| `latex-manuscript` | 📝 Writing | Compilação, figuras, latexdiff |
| `grant-proposal-writer` | 📝 Writing | NSF/NIH + FAPESP/CAPES/CNPq 🇧🇷 |
| `data-extractor` | 📝 Writing | Digitalizar figuras de papers (26+ plot types) |
| `molecular-docking` | 🧬 Bio | AutoDock Vina, DiffDock, virtual screening |
| `protein-structure-analysis` | 🧬 Bio | Biotite 3D, contact maps, binding sites |
| `kinase-interaction-modeling` | 🧬 Bio | DT-Kinase Level 4 CNN, DTI prediction |
| `drug-target-interaction` | 🧬 Bio | ChEMBL, molecular fingerprints |

### Synced Skills (de 12 repositórios)

| Repositório | ⭐ | Skills | Foco |
|-------------|-----|--------|------|
| VoltAgent/awesome-claude-code-subagents | 16.2K | 100+ | Full-stack, DevOps, ML, meta-orchestration |
| tech-leads-club/agent-skills | 2K | 20+ | Security-audited, multi-platform |
| ClawBio/ClawBio | — | 43 | Genomics, PGx, clinical |
| GPTomics/bioSkills | — | 426 | Proteomics, RNA-seq, single-cell |
| K-Dense-AI/claude-scientific-skills | — | 134 | Scientific schematics, grants |
| jaechang-hits/SciAgent-Skills | — | 196 | Life sciences |
| K-Dense-AI/claude-scientific-writer | 1.4K | 10 | Citation, peer review, slides |
| zhangchenhaobest/academic-research-skills | — | 4 | Deep research, pipeline |
| guanyang/antigravity-skills | — | 20+ | Python, FastAPI, architecture |
| rmyndharis/antigravity-skills | — | 20+ | MCP, planning, workflows |

---

## 🛠 MCP Tools Reference

| Tool | Descrição | Exemplo |
|------|-----------|---------|
| `list_skills()` | Lista todas as skills | "What skills do you have?" |
| `search_skills(query)` | Busca por keyword | `search_skills("protein docking")` |
| `get_skill(id)` | Conteúdo completo da skill | `get_skill("molecular-docking")` |
| `get_skill_scripts(id)` | Scripts auxiliares | `get_skill_scripts("seq-wrangler")` |
| `list_agents()` | Lista agentes disponíveis | "Show me all agents" |
| `search_agents(query)` | Busca agentes por keyword | `search_agents("python backend")` |
| `get_agent(id)` | Configuração completa do agente | `get_agent("fullstack-developer")` |

---

## 🧪 Desenvolvimento

```bash
# Ativar ambiente
source .venv/bin/activate

# Gerar/atualizar catálogo
PYTHONPATH=server python3 scripts/build_catalog.py

# Testar o registry diretamente
PYTHONPATH=server python3 -c "
from skill_registry import SkillRegistry
r = SkillRegistry('skills'); r.scan()
print(f'Skills: {r.count}')
for s in r.search_skills('protein'):
    print(f'  {s[\"id\"]}: {s[\"name\"]} (score: {s[\"score\"]})')
"

# Testar o servidor (modo SSE para debug)
PYTHONPATH=server python3 server/mcp_skills_server.py --transport sse --port 8765
# → http://localhost:8765
```

### Adicionar uma nova skill

```bash
# 1. Criar diretório
mkdir -p skills/minha-skill

# 2. Criar SKILL.md com frontmatter
cat > skills/minha-skill/SKILL.md << 'EOF'
---
name: Minha Skill
description: "Descrição curta da skill."
category: minha-categoria
tags: tag1, tag2, tag3
---

# Minha Skill

## Use this skill when
- Cenário de uso 1
- Cenário de uso 2

## Instructions
Instruções detalhadas aqui...
EOF

# 3. Reconstruir catálogo
PYTHONPATH=server python3 scripts/build_catalog.py
```

### Adicionar um novo agente

```bash
mkdir -p agents/meu-agente
# Mesmo formato SKILL.md, mas com campo 'skills:' no frontmatter
```

---

## 📖 References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP SDK](https://gofastmcp.com/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [VoltAgent Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Tech Leads Club Agent Skills](https://github.com/tech-leads-club/agent-skills)

## 📄 License

MIT
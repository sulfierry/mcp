# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server structured under a **Dual-Core Architecture**: combining **Autonomous Deep Research** with **State-of-the-Art (SOTA) Engineering**. It exposes **450+ curated AI agent skills** as callable tools. Covers bioinformatics, scientific writing, polyglot algorithms (C++/Python), and complete agentic orchestration — all running on `localhost` for privacy and low latency.

## 📊 At a Glance

| Metric | Value |
|--------|-------|
| **Skills** | 569 |
| **Mega-Workflows** | 6 Core Modalities |
| **Agent Personas** | Dual-Core Squad |
| **Source Repositories** | 13 |
| **MCP Tools** | 8 |
| **Transport** | stdio + SSE (HTTP) |

---

## 🏗 Architecture

> The ecosystem leverages exactly **569** modular skills and **10** specialized agent personas to dynamically respond to queries via the Dual-Core engine.

```
MCP Client (Antigravity / VS Code / Claude Desktop / Cursor)
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
   │  skills/ 450  │   ← SKILL.md files from 12 repos
   │  agents/ 10   │   ← Agent personas (Dual-Core)
   └───────────────┘
```

---

---

## 🤖 Agent Personas (Core Team)

> **Nota Arquitetural:** O ecossistema roda sob o paradigma **"Dual-Core"**, separando a Pesquisa de Ponta Científica da implementação de Código (SOTA Engineering).

### 🔬 Deep Research & Scientific Discovery
| Agent | ID | Descrição |
|-------|-----|-----------|
| Deep Researcher | `deep-researcher` | Investigação profunda de web, literatura complexa, citações |
| Investigative Orchestrator | `investigative-orchestrator` | Divisão de perguntas complexas viasequential/parallel thinking |
| Bioinformatics Researcher | `bioinformatics-researcher` | Biologia computacional, protein analysis, omics |
| Scientific Writer | `scientific-writer` | Pesquisa → escrita → citação → LaTeX |

### 🚀 Elite State-of-the-Art Engineering (SOTA)
| Agent | ID | Descrição |
|-------|-----|-----------|
| SOTA Engineer | `state-of-the-art-engineer` | Polyglot architect (C++/Python/UI). DOD e Memory Safety. |
| Algorithmic Thinker | `algorithmic-thinker` | Abordagem Chain-of-Thought e mapeamento de complexidade O(N) |
| Self-Improving Agent | `self-improving-agent` | Auto-cura baseada em Tracebacks e prevenção de regressão |
| MCP Server Builder | `mcp-server-builder` | Infraestrutura C++/Python, Protocolos e API Boundaries |

### 💻 Base Programming & DevOps
| Agent | ID | Descrição |
|-------|-----|-----------|
| Python Architect | `python-architect` | Clean architecture, async, typing, packaging |
| DevSecOps Expert| `ai-security-auditor` | Master SecOps, AI Vetting e proteção de ambiente |
| Code Reviewer | `code-reviewer` | Review com scoring multi-dimensional e red flags |

---

## 🚀 Quick Start (3 passos)

### 1. Clone e instale dependências

```bash
git clone https://github.com/sulfierry/mcp.git
cd mcp

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

> **Preciso rodar `sync_skills.sh`?** Só na **primeira vez** (para popular `skills/` a partir dos 13 repositórios de referência) ou quando quiser atualizar para versões mais recentes. Se você clonou o repo e o diretório `skills/` já contém 569 pastas, **não precisa rodar novamente**.

---

## 🔌 Ativação Local — Passo a Passo

### Opção A: Claude Code CLI

O Claude Code descobre skills automaticamente a partir do diretório `.claude/skills/` (projeto) ou `~/.claude/skills/` (global). Existem **três formas** de ativar:

#### Método 1: Symlink para skills globais (mais simples)

```bash
# Skills ficam disponíveis em TODOS os projetos
ln -sf /Users/$USER/mcp/skills ~/.claude/skills
```

Pronto! O Claude Code vai autodescobrir e usar as 569 skills em qualquer projeto.

#### Método 2: Symlink por projeto

```bash
# Dentro do diretório do seu projeto
mkdir -p .claude
ln -sf /Users/$USER/mcp/skills .claude/skills
```

#### Método 3: MCP Server via CLI (Recomendado / Mais poderoso)

```bash
# Registrar globalmente (disponível em todos os projetos)
claude mcp add --scope user skills-server \
  /Users/$USER/mcp/.venv/bin/python3 \
  /Users/$USER/mcp/server/mcp_skills_server.py

# OU registrar apenas no projeto atual
claude mcp add --scope project skills-server \
  /Users/$USER/mcp/.venv/bin/python3 \
  /Users/$USER/mcp/server/mcp_skills_server.py
```

Comandos úteis para gerenciar:

```bash
claude mcp list                    # Ver servidores configurados
claude mcp get skills-server       # Detalhes do servidor
claude mcp remove skills-server    # Remover servidor
```

> **Por que MCP Server é melhor que symlink?** O symlink entrega o texto das skills diretamente. O servidor MCP adiciona **Tools inteligentes** — `search_skills()`, `search_agents()`, `get_skill()` — que permitem ao agente caçar autonomamente a skill ideal para cada prompt, sem carregar todas na memória.

#### Verificação

```bash
# Verificar que o servidor foi registrado
claude mcp list

# Testar comunicação
claude "list your available MCP tools"
```

---

### Opção B: VS Code (GitHub Copilot + MCP)

O VS Code com GitHub Copilot suporta skills de **duas formas** complementares:

#### Método 1: Skills nativas do Copilot (autodescoberta)

O Copilot Agent Mode descobre skills em `.github/skills/` automaticamente:

```bash
# No diretório do seu projeto
ln -sf /Users/$USER/mcp/skills .github/skills
```

> **Dica para monorepos:** Ative `"chat.useCustomizationsInParentRepositories": true` no `settings.json` para autodescobrir skills de diretórios pai.

Opcionalmente, crie também um `copilot-instructions.md` para regras globais:

```bash
# Criar instruções globais do projeto
cat > .github/copilot-instructions.md << 'EOF'
Use the available skills in .github/skills/ for scientific, bioinformatics,
and engineering tasks. Search for relevant SKILL.md files when working with
specialized packages (RDKit, Scanpy, PyTorch, etc.) or databases (PubChem,
ChEMBL, UniProt, ClinVar, COSMIC, etc.).
EOF
```

#### Método 2: MCP Server (ferramentas avançadas de busca)

Adicione ao arquivo `.vscode/mcp.json` na raiz do seu projeto:

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

Ou para configuração **global** (disponível em todos os projetos), adicione ao `settings.json` do VS Code (`Cmd+Shift+P` → `Preferences: Open User Settings (JSON)`):

```json
{
  "mcp.servers": {
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

#### Verificação

Abra o painel de saída do VS Code (`Cmd+Shift+U`) e selecione "MCP" para ver os logs do servidor. Você deve ver:

```
🧬 Skills Registry loaded: 569 skills discovered
🤖 Agent Registry loaded: 10 agents discovered
🚀 Starting MCP Skills Server (stdio mode)
```

---

### Opção C: Google Antigravity (Gemini)

O Antigravity descobre skills automaticamente a partir do diretório `~/.gemini/antigravity/skills/`. Existem **duas formas** de ativar:

#### Método 1: Symlink (mais simples)

```bash
# Criar link simbólico para o diretório de skills
ln -sf /Users/$USER/mcp/skills ~/.gemini/antigravity/skills
```

Pronto! O Antigravity vai encontrar todas as 569 skills automaticamente ao iniciar a próxima conversa.

#### Método 2: MCP Server (Recomendado / Mais poderoso)

Adicione ao arquivo `~/.gemini/settings.json`:

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

> **Por que este método é melhor?** Enquanto o symlink apenas entrega o texto das 569 skills, o servidor MCP adiciona **Ferramentas Inteligentes (Tools)** ao Antigravity. Eu ganho a habilidade de rodar `search_skills()` ou `search_agents()` automaticamente para caçar e encontrar a skill perfeita para o seu prompt, além disso o próprio Antigravity inicia e desliga o servidor automaticamente em segundo plano!

---

### Opção D: Claude Desktop

Adicione ao arquivo `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Reinicie o Claude Desktop. O ícone 🔌 deve aparecer indicando o MCP server conectado.

---

### Opção E: Cursor

Adicione ao arquivo `~/.cursor/mcp.json`:

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

### Opção F: Modo HTTP/SSE (qualquer cliente)

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

### Synced Skills (de 13 repositórios)

| Repositório | ⭐ | Skills | Foco |
|-------------|-----|--------|------|
| VoltAgent/awesome-claude-code-subagents | 16.2K | 100+ | Full-stack, DevOps, ML, meta-orchestration |
| tech-leads-club/agent-skills | 2K | 20+ | Security-audited, multi-platform |
| ClawBio/ClawBio | — | 43 | Genomics, PGx, clinical |
| GPTomics/bioSkills | — | 426 | Proteomics, RNA-seq, single-cell |
| K-Dense-AI/claude-scientific-skills | — | 134 | Scientific schematics, grants |
| **K-Dense-AI/scientific-agent-skills** | **—** | **119** | **Drug discovery, scRNA-seq, genomics, ML, clinical, 78 databases, lab automation** |
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
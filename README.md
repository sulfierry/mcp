# 🧬 Skills MCP Server

A local **Model Context Protocol (MCP)** server structured under a **Dual-Core Architecture**: combining **Autonomous Deep Research** with **State-of-the-Art (SOTA) Engineering**. It exposes **573 curated AI agent skills** as callable tools. Covers bioinformatics, drug discovery, scientific writing, polyglot algorithms (C++/Python), and complete agentic orchestration — all running on `localhost` for privacy and low latency.

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

## 💡 O que é MCP? (Explicação simples)

**MCP (Model Context Protocol)** é um "controle remoto" que dá **poderes extras** a uma IA. Sem MCP, a IA só conversa baseada na memória do treinamento. Com MCP, ela pode buscar em bancos de dados, rodar scripts, acessar APIs — qualquer coisa que o servidor ofereça.

### Analogia

Imagine a IA conversando por chat:

```
Sem MCP:
  Você:  "Qual a estrutura 3D da proteína BRAF?"
  IA:    "Sei que é uma quinase..." (resposta genérica, da memória)

Com MCP:
  Você:  "Qual a estrutura 3D da proteína BRAF?"
  IA:    → chama search_skills("protein structure")
         → encontra a skill 'struct-predictor'
         → segue as instruções para consultar o PDB
  IA:    "A estrutura cristalográfica de BRAF (PDB: 6U2G) mostra..."
         (resposta específica, com dados reais)
```

### Ciclo de vida do servidor

O MCP server **NÃO** fica rodando permanentemente em background:

```
Você NÃO está usando o IDE:
  MCP server? 💤 DESLIGADO (zero recursos)

Você abre o IDE (Antigravity, Claude Code, VS Code...):
  IDE lê o config → inicia o skills-server automaticamente
  MCP server? 🟢 LIGADO (~10MB RAM)
  IA ganha ferramentas: search_skills(), get_skill(), etc.

Você fecha o IDE:
  MCP server? 💤 DESLIGADO automaticamente
```

### Como funciona

```
          Você digita um prompt
                  │
                  ▼
      ┌──────────────────────┐
      │    IDE (o "cérebro")  │  Antigravity, Claude Code, VS Code...
      └──────────┬───────────┘
                 │ stdio (texto via terminal)
                 ▼
      ┌──────────────────────┐
      │   MCP Skills Server  │  O "assistente" com poderes extras
      │                      │
      │  Tools disponíveis:  │
      │  • search_skills()   │  "busque 'docking' nas 573 skills"
      │  • get_skill()       │  "me dê o SKILL.md completo da skill X"
      │  • search_agents()   │  "qual agente entende de proteínas?"
      │  • list_skills()     │  "liste todas as skills disponíveis"
      └──────────┬───────────┘
                 │
         ┌───────┴───────┐
         │  skills/  573 │  ← SKILL.md files de 12 repos
         │  agents/   10 │  ← Agent personas (Dual-Core)
         └───────────────┘
```

### Symlink vs MCP Server — por que ter os dois?

| | Symlink | MCP Server |
|---|---|---|
| **Como funciona** | A IA vê todas as skills listadas no início da conversa | A IA tem **ferramentas** para buscar e ler skills sob demanda |
| **Analogia** | Ter o catálogo da biblioteca na mesa | Ter um bibliotecário que busca o livro certo |
| **Vantagem** | Descoberta passiva automática | Busca inteligente por keyword |
| **Limitação** | Carrega muitos nomes no contexto | Precisa do processo Python rodando |

**Ter os dois é o setup ideal** — o catálogo mostra o que existe, o bibliotecário vai buscar o livro certo quando preciso.

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

> **Nota Arquitetural:** O ecossistema roda sob o paradigma **"Dual-Core"**, separando a Pesquisa de Ponta Científica da implementação de Código (SOTA Engineering).

### 🔬 Deep Research & Scientific Discovery
| Agent | ID | Descrição |
|-------|-----|-----------| 
| Deep Researcher | `deep-researcher` | Investigação profunda de web, literatura complexa, citações |
| Investigative Orchestrator | `investigative-orchestrator` | Divisão de perguntas complexas via sequential/parallel thinking |
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

### 2. Sincronize skills e configure os IDEs automaticamente

```bash
chmod +x scripts/sync_skills.sh start_server.sh

# Sincronizar skills curadas (recomendado)
./scripts/sync_skills.sh

# OU sincronizar TODAS as skills disponíveis
./scripts/sync_skills.sh --all

# Ver repositórios disponíveis
./scripts/sync_skills.sh --list
```

O script executa **4 fases** automaticamente:

| Fase | O que faz |
|------|-----------|
| **1. Sync** | Clona 12 repos e copia skills para `skills/` |
| **2. Merge** | Copia agentes de `agents/` → `skills/` para descoberta universal |
| **3. Symlinks** | Cria links para Antigravity, Claude Code CLI e VS Code Copilot |
| **4. Catalog** | Reconstrói `skills_index.json` com todas as skills indexadas |

> **Preciso rodar `sync_skills.sh`?** Só na **primeira vez** (para popular `skills/`) ou quando quiser atualizar. Se o diretório `skills/` já contém 573 pastas, **não precisa rodar novamente**.

### 3. Registre o MCP Server no seu IDE preferido

Escolha uma ou mais opções abaixo (**todas** podem coexistir):

---

## 🔌 Ativação Local — Passo a Passo

### Opção A: Claude Code CLI

O Claude Code descobre skills de **duas formas** complementares:

#### Forma 1: Symlink (autodescoberta passiva)

Já criado automaticamente pelo `sync_skills.sh`:

```bash
~/.claude/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Forma 2: MCP Server via CLI (busca ativa — recomendado)

```bash
# Registrar globalmente (disponível em todos os projetos)
claude mcp add --scope user skills-server \
  /Users/$USER/mcp/.venv/bin/python3 \
  /Users/$USER/mcp/server/mcp_skills_server.py
```

Comandos úteis:

```bash
claude mcp list                    # Ver servidores configurados
claude mcp get skills-server       # Detalhes do servidor
claude mcp remove skills-server    # Remover servidor
```

---

### Opção B: VS Code (GitHub Copilot + MCP)

#### Forma 1: Skills nativas do Copilot (autodescoberta)

Já criado automaticamente pelo `sync_skills.sh`:

```bash
.github/skills/ → /Users/$USER/mcp/skills/   # (symlink no projeto)
```

> **Dica para monorepos:** Ative `"chat.useCustomizationsInParentRepositories": true` no `settings.json`.

#### Forma 2: MCP Server (ferramentas avançadas de busca)

Adicione ao `.vscode/mcp.json` (por projeto) ou ao `settings.json` global (`Cmd+Shift+P` → `Preferences: Open User Settings (JSON)`):

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

### Opção C: Google Antigravity (Gemini)

#### Forma 1: Symlink (autodescoberta)

Já criado automaticamente pelo `sync_skills.sh`:

```bash
~/.gemini/antigravity/skills/ → /Users/$USER/mcp/skills/   # (symlink)
```

#### Forma 2: MCP Server (recomendado)

Adicione ao `~/.gemini/settings.json`:

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

### Opção D: Claude Desktop

Adicione ao `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

### Opção E: Cursor

Adicione ao `~/.cursor/mcp.json`:

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

### ✅ Verificação

Após configurar qualquer opção, verifique:

```bash
# Claude Code CLI
claude mcp list

# Ou em qualquer IDE, peça:
"list your available MCP tools"
```

Você deve ver as 7 tools disponíveis: `list_skills`, `search_skills`, `get_skill`, `get_skill_scripts`, `list_agents`, `search_agents`, `get_agent`.

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
| **K-Dense-AI/scientific-agent-skills** | **—** | **133** | **Drug discovery, scRNA-seq, genomics, ML, clinical, 78 databases, lab automation** |
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
- [Agent Skills Standard](https://agentskills.io/)
- [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
- [VoltAgent Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [Tech Leads Club Agent Skills](https://github.com/tech-leads-club/agent-skills)

## 📄 License

GNU General Public License v3.0
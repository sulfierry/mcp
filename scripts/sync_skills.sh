#!/usr/bin/env bash
# sync_skills.sh — Pull curated skills from reference repositories
#
# Usage:
#   ./scripts/sync_skills.sh             # Sync curated skills
#   ./scripts/sync_skills.sh --all       # Sync ALL skills from all repos
#   ./scripts/sync_skills.sh --force     # Overwrite existing skills
#   ./scripts/sync_skills.sh --list      # List available sources
#
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_DIR/skills"
TMP_DIR="$PROJECT_DIR/tmp_sync"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Flags
SYNC_ALL=false
FORCE=false
LIST_ONLY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all) SYNC_ALL=true; shift ;;
        --force) FORCE=true; shift ;;
        --list) LIST_ONLY=true; shift ;;
        *) echo -e "${RED}Unknown option: $1${NC}"; exit 1 ;;
    esac
done

# Curated skill names (space-separated strings for portability)
CURATED_GUANYANG="python-pro fastapi-pro async-python-patterns test-driven-development systematic-debugging architecture-patterns api-design-principles ai-engineer prompt-engineering-patterns security-auditor code-review-ai-ai-review mcp-builder skill-creator planning-with-files writing-plans executing-plans subagent-driven-development"

# Note: GPTomics/bioSkills was removed — 438 skills exist but none are importable
# due to nested directory structure (category/subcategory/SKILL.md).

CURATED_WRITING="scientific-schematics research-lookup peer-review citation-management clinical-reports research-grants scientific-slides latex-posters hypothesis-generation market-research-reports"

CURATED_ACADEMIC="deep-research academic-paper academic-paper-reviewer academic-pipeline"

CURATED_VOLTAGENT="api-designer backend-developer frontend-developer fullstack-developer ui-designer python-pro typescript-pro fastapi-developer django-developer nextjs-developer react-specialist rust-engineer golang-pro sql-pro cloud-architect devops-engineer docker-expert kubernetes-specialist terraform-engineer security-engineer sre-engineer code-reviewer debugger error-detective qa-expert security-auditor test-automator performance-engineer ai-engineer data-engineer llm-architect ml-engineer prompt-engineer documentation-engineer mcp-developer refactoring-specialist legacy-modernizer"

# Check if a skill name is in a curated list
is_curated() {
    local name="$1"
    local list="$2"
    echo "$list" | tr ' ' '\n' | grep -qx "$name"
}

if $LIST_ONLY; then
    echo -e "${CYAN}📚 Available skill sources (10 repos):${NC}"
    echo -e ""
    echo -e "  ${BLUE}── Bioinformatics & Science ──${NC}"
    echo -e "  ${GREEN}•${NC} ClawBio/ClawBio (skills/) ★ 47 bio/pharma skills"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/scientific-agent-skills (scientific-skills/) ★ 134 scientific skills"
    echo -e "  ${GREEN}•${NC} GPTomics/bioSkills (nested scan) ★ 438 bioinformatics skills"
    echo -e "  ${GREEN}•${NC} jaechang-hits/SciAgent-Skills (nested scan) ★ 197 scientific skills"
    echo -e ""
    echo -e "  ${BLUE}── Scientific Writing ──${NC}"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/claude-scientific-writer (skills/)"
    echo -e "  ${GREEN}•${NC} zhangchenhaobest/academic-research-skills (.)"
    echo -e ""
    echo -e "  ${BLUE}── Programming & DevOps ──${NC}"
    echo -e "  ${GREEN}•${NC} VoltAgent/awesome-claude-code-subagents ⭐16K (categories/)"
    echo -e "  ${GREEN}•${NC} tech-leads-club/agent-skills ⭐2K (packages/skills-catalog/skills/)"
    echo -e "  ${GREEN}•${NC} guanyang/antigravity-skills (skills/)"
    echo -e "  ${GREEN}•${NC} rmyndharis/antigravity-skills (skills/)"
    echo -e ""
    echo -e "  ${BLUE}── Knowledge Graph / Codebase ──${NC}"
    echo -e "  ${GREEN}•${NC} safishamsi/graphify (graphify/skill.md, single-file)"
    exit 0
fi

echo -e "${CYAN}🔄 Syncing skills from reference repositories...${NC}"
echo ""

mkdir -p "$SKILLS_DIR"
mkdir -p "$TMP_DIR"

sync_count=0
skip_count=0

sync_skill() {
    local src_path="$1"
    local skill_name="$2"
    local dest="$SKILLS_DIR/$skill_name"

    # Check if SKILL.md exists in source
    if [[ ! -f "$src_path/SKILL.md" ]]; then
        return 1
    fi

    if [[ -d "$dest" ]] && ! $FORCE; then
        skip_count=$((skip_count + 1))
        return 0
    fi

    mkdir -p "$dest"
    cp -r "$src_path"/* "$dest/" 2>/dev/null || true
    sync_count=$((sync_count + 1))
    echo -e "  ${GREEN}✓${NC} $skill_name"
}

clone_and_sync() {
    local name="$1"
    local url="$2"
    local subdir="$3"
    local curated_list="$4"

    local repo_dir="$TMP_DIR/$(echo "$name" | tr '/' '_')"

    echo -e "${BLUE}📦 Cloning $name...${NC}"

    if [[ -d "$repo_dir" ]]; then
        (cd "$repo_dir" && git pull --quiet 2>/dev/null) || true
    else
        git clone --depth 1 --quiet "$url" "$repo_dir" 2>/dev/null || {
            echo -e "  ${YELLOW}⚠ Failed to clone $name (skipping)${NC}"
            return 0
        }
    fi

    local skills_src="$repo_dir/$subdir"

    if [[ ! -d "$skills_src" ]]; then
        echo -e "  ${YELLOW}⚠ Skills directory not found: $subdir (skipping)${NC}"
        return 0
    fi

    # Iterate through skill directories
    for skill_dir in "$skills_src"/*/; do
        [[ ! -d "$skill_dir" ]] && continue
        local skill_name
        skill_name="$(basename "$skill_dir")"

        # Skip non-skill directories
        case "$skill_name" in
            .git|node_modules|__pycache__|resources|workflows|bioskills-installer|.github|.claude-plugin|.cursor-plugin|.nx|assets|templates|tests|bot|docs|examples|img|scripts|slides|corpas-30x|robotary|GENOMEBOOK|commands|clawbio|demo|references|tools|libs|packages|core|\(*\)) continue ;;
        esac

        if $SYNC_ALL; then
            sync_skill "$skill_dir" "$skill_name" || true
        else
            if [[ -n "$curated_list" ]] && is_curated "$skill_name" "$curated_list"; then
                sync_skill "$skill_dir" "$skill_name" || true
            fi
        fi
    done

    echo ""
}

# clone_and_sync_nested — For repos with nested structure (category/skill/SKILL.md)
# Recursively finds all SKILL.md files and imports using the leaf directory name.
clone_and_sync_nested() {
    local name="$1"
    local url="$2"
    local subdir="$3"

    local repo_dir="$TMP_DIR/$(echo "$name" | tr '/' '_')"

    echo -e "${BLUE}📦 Cloning $name (nested scan)...${NC}"

    if [[ -d "$repo_dir" ]]; then
        (cd "$repo_dir" && git pull --quiet 2>/dev/null) || true
    else
        git clone --depth 1 --quiet "$url" "$repo_dir" 2>/dev/null || {
            echo -e "  ${YELLOW}⚠ Failed to clone $name (skipping)${NC}"
            return 0
        }
    fi

    local skills_src="$repo_dir/$subdir"

    if [[ ! -d "$skills_src" ]]; then
        echo -e "  ${YELLOW}⚠ Skills directory not found: $subdir (skipping)${NC}"
        return 0
    fi

    # Recursively find all SKILL.md files at any depth
    while IFS= read -r skill_md; do
        local skill_dir
        skill_dir="$(dirname "$skill_md")"
        local skill_name
        skill_name="$(basename "$skill_dir")"

        # Skip non-skill directories
        case "$skill_name" in
            .git|node_modules|__pycache__|bioskills-installer|.github|assets|templates|tests|docs|examples|scripts) continue ;;
        esac

        sync_skill "$skill_dir" "$skill_name" || true
    done < <(find "$skills_src" -name "SKILL.md" -type f 2>/dev/null)

    echo ""
}

# Sync from each source with appropriate curated list
# -- Bioinformatics & Science --
clone_and_sync "ClawBio/ClawBio" "https://github.com/ClawBio/ClawBio.git" "skills" ""
# Note: claude-scientific-skills was renamed to scientific-agent-skills (same repo)
clone_and_sync "K-Dense-AI/scientific-agent-skills" "https://github.com/K-Dense-AI/scientific-agent-skills.git" "scientific-skills" ""
# Nested repos: these use category/skill/SKILL.md structure
clone_and_sync_nested "GPTomics/bioSkills" "https://github.com/GPTomics/bioSkills.git" "."
clone_and_sync_nested "jaechang-hits/SciAgent-Skills" "https://github.com/jaechang-hits/SciAgent-Skills.git" "skills"

# -- Scientific Writing --
clone_and_sync "K-Dense-AI/claude-scientific-writer" "https://github.com/K-Dense-AI/claude-scientific-writer.git" "skills" "$CURATED_WRITING"
clone_and_sync "zhangchenhaobest/academic-research-skills" "https://github.com/zhangchenhaobest/academic-research-skills.git" "." "$CURATED_ACADEMIC"
# Removed: InternScience/Awesome-Scientific-Skills (git submodules not initialized — 0 files)

# -- Programming & DevOps --
# VoltAgent: 100+ subagents in categories/NN-topic/agent.md (16K+ stars)
# Scan all category subdirectories for .md agent files
sync_voltagent() {
    local repo_dir="$TMP_DIR/VoltAgent_awesome-claude-code-subagents"
    echo -e "${BLUE}📦 Cloning VoltAgent/awesome-claude-code-subagents...${NC}"
    if [[ -d "$repo_dir" ]]; then
        (cd "$repo_dir" && git pull --quiet 2>/dev/null) || true
    else
        git clone --depth 1 --quiet "https://github.com/VoltAgent/awesome-claude-code-subagents.git" "$repo_dir" 2>/dev/null || {
            echo -e "  ${YELLOW}⚠ Failed to clone VoltAgent (skipping)${NC}"
            return 0
        }
    fi

    local cats_dir="$repo_dir/categories"
    [[ ! -d "$cats_dir" ]] && return 0

    for cat_dir in "$cats_dir"/*/; do
        [[ ! -d "$cat_dir" ]] && continue
        for agent_md in "$cat_dir"/*.md; do
            [[ ! -f "$agent_md" ]] && continue
            local agent_name
            agent_name="$(basename "$agent_md" .md)"
            [[ "$agent_name" == "README" ]] && continue

            if $SYNC_ALL || is_curated "$agent_name" "$CURATED_VOLTAGENT"; then
                local dest="$SKILLS_DIR/$agent_name"
                if [[ -d "$dest" ]] && ! $FORCE; then
                    skip_count=$((skip_count + 1))
                    continue
                fi
                mkdir -p "$dest"
                # Convert .md to SKILL.md format
                cp "$agent_md" "$dest/SKILL.md" 2>/dev/null || true
                sync_count=$((sync_count + 1))
                echo -e "  ${GREEN}✓${NC} $agent_name (VoltAgent)"
            fi
        done
    done
    echo ""
}
sync_voltagent

clone_and_sync "tech-leads-club/agent-skills" "https://github.com/tech-leads-club/agent-skills.git" "packages/skills-catalog/skills" ""
clone_and_sync "guanyang/antigravity-skills" "https://github.com/guanyang/antigravity-skills.git" "skills" "$CURATED_GUANYANG"
clone_and_sync "rmyndharis/antigravity-skills" "https://github.com/rmyndharis/antigravity-skills.git" "skills" "$CURATED_GUANYANG"

# sync_graphify — Special case: single-file skill living inside a Python package.
# Upstream layout: graphify/skill.md (not a top-level SKILL.md, no per-skill dir).
# Pulled via raw.githubusercontent.com, no git clone of the 58k Python package.
sync_graphify() {
    local name="safishamsi/graphify"
    local branch="v4"
    local url="https://raw.githubusercontent.com/$name/$branch/graphify/skill.md"
    local dest="$SKILLS_DIR/graphify"

    echo -e "${BLUE}📦 Fetching $name (single-file sync)...${NC}"

    if [[ -d "$dest" ]] && [[ -f "$dest/SKILL.md" ]] && ! $FORCE; then
        # Compare remote vs local — update only if changed
        local tmp
        tmp="$(mktemp)"
        if curl -fsSL "$url" -o "$tmp" 2>/dev/null; then
            if ! diff -q "$tmp" "$dest/SKILL.md" >/dev/null 2>&1; then
                mv "$tmp" "$dest/SKILL.md"
                sync_count=$((sync_count + 1))
                echo -e "  ${GREEN}✓${NC} graphify (updated from $branch)"
            else
                skip_count=$((skip_count + 1))
                rm -f "$tmp"
            fi
        else
            rm -f "$tmp"
            echo -e "  ${YELLOW}⚠ Failed to fetch graphify skill.md${NC}"
        fi
        return 0
    fi

    mkdir -p "$dest"
    if curl -fsSL "$url" -o "$dest/SKILL.md" 2>/dev/null; then
        sync_count=$((sync_count + 1))
        echo -e "  ${GREEN}✓${NC} graphify (fetched from $branch)"
    else
        echo -e "  ${YELLOW}⚠ Failed to fetch graphify skill.md${NC}"
    fi
    echo ""
}
sync_graphify

echo -e "${GREEN}✅ Sync complete: $sync_count skills synced, $skip_count skipped (already exist)${NC}"

# ─── Phase 2: Merge agents into skills/ ───────────────────────────────────────
AGENTS_DIR="$PROJECT_DIR/agents"
if [[ -d "$AGENTS_DIR" ]]; then
    echo ""
    echo -e "${CYAN}🤖 Merging agents into skills/ for universal discovery...${NC}"
    agent_count=0
    for agent_dir in "$AGENTS_DIR"/*/; do
        [[ ! -d "$agent_dir" ]] && continue
        agent_name="$(basename "$agent_dir")"
        [[ ! -f "$agent_dir/SKILL.md" ]] && continue

        dest="$SKILLS_DIR/$agent_name"
        if [[ -d "$dest" ]] && ! $FORCE; then
            continue
        fi

        cp -R "$agent_dir" "$dest"
        agent_count=$((agent_count + 1))
        echo -e "  ${GREEN}✓${NC} $agent_name (agent → skill)"
    done

    if [[ $agent_count -gt 0 ]]; then
        echo -e "${GREEN}✅ $agent_count agents merged into skills/${NC}"
    else
        echo -e "  ${YELLOW}•${NC} All agents already present in skills/"
    fi
fi

# ─── Phase 3a: IDE Symlinks (passive skill discovery) ─────────────────────────
echo ""
echo -e "${CYAN}🔗 Setting up IDE symlinks...${NC}"

create_symlink() {
    local target="$1"
    local link_path="$2"
    local ide_name="$3"

    mkdir -p "$(dirname "$link_path")"

    if [[ -L "$link_path" ]]; then
        local current_target
        current_target="$(readlink "$link_path" 2>/dev/null || stat -f '%Y' "$link_path" 2>/dev/null)"
        if [[ "$current_target" == "$target" ]]; then
            echo -e "  ${GREEN}✓${NC} $ide_name — already linked"
            return 0
        fi
        rm "$link_path"
    elif [[ -d "$link_path" ]]; then
        echo -e "  ${YELLOW}⚠${NC} $ide_name — skipped (real directory exists at $link_path)"
        return 0
    fi

    ln -sf "$target" "$link_path"
    echo -e "  ${GREEN}✓${NC} $ide_name — linked → $link_path"
}

create_symlink "$SKILLS_DIR" "$HOME/.gemini/antigravity/skills" "Antigravity (Gemini)"
create_symlink "$SKILLS_DIR" "$HOME/.claude/skills" "Claude Code CLI"
create_symlink "$SKILLS_DIR" "$PROJECT_DIR/.github/skills" "VS Code Copilot (project)"
create_symlink "$SKILLS_DIR" "${CODEX_HOME:-$HOME/.codex}/skills" "OpenAI Codex CLI"
create_symlink "$SKILLS_DIR" "${QWEN_HOME:-$HOME/.qwen}/skills" "Qwen CLI"

# ─── Phase 3b: MCP Server Config (all IDEs) ────────────────────────────────────
echo ""
echo -e "${CYAN}⚙️  Configuring MCP server for all IDEs...${NC}"

MCP_CMD="$PROJECT_DIR/.venv/bin/python3"
MCP_ARG="$PROJECT_DIR/server/mcp_skills_server.py"
MCP_ENV_PP="$PROJECT_DIR/server"

# Generic: inject mcpServers into a JSON config file
# If file doesn't exist, creates it. If it exists, adds mcpServers key via python.
inject_mcp_json() {
    local config_file="$1"
    local ide_name="$2"

    mkdir -p "$(dirname "$config_file")"

    if [[ -f "$config_file" ]] && grep -q 'skills-server' "$config_file" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $ide_name — MCP already configured"
        return 0
    fi

    if [[ ! -f "$config_file" ]]; then
        # Create new file
        cat > "$config_file" << JSONEOF
{
  "mcpServers": {
    "skills-server": {
      "command": "$MCP_CMD",
      "args": ["$MCP_ARG"],
      "env": {
        "PYTHONPATH": "$MCP_ENV_PP"
      }
    }
  }
}
JSONEOF
        echo -e "  ${GREEN}✓${NC} $ide_name — config created with MCP server"
    else
        # File exists but no skills-server — inject via python
        python3 -c "
import json, sys
try:
    with open('$config_file', 'r') as f:
        data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    data = {}
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['skills-server'] = {
    'command': '$MCP_CMD',
    'args': ['$MCP_ARG'],
    'env': {'PYTHONPATH': '$MCP_ENV_PP'}
}
with open('$config_file', 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && \
            echo -e "  ${GREEN}✓${NC} $ide_name — MCP server injected into existing config" || \
            echo -e "  ${YELLOW}⚠${NC} $ide_name — could not inject (edit manually: $config_file)"
    fi
}

# Antigravity-specific: inject into mcp_config.json preserving existing servers
# Antigravity reads MCP config from ~/.gemini/antigravity/mcp_config.json, NOT settings.json
inject_mcp_antigravity() {
    local config_file="$HOME/.gemini/antigravity/mcp_config.json"
    local ide_name="Antigravity (Gemini)"

    mkdir -p "$(dirname "$config_file")"

    if [[ -f "$config_file" ]] && grep -q 'skills-server' "$config_file" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} $ide_name — MCP already configured in mcp_config.json"
        return 0
    fi

    if [[ ! -f "$config_file" ]]; then
        # Create new file with skills-server
        cat > "$config_file" << JSONEOF
{
  "mcpServers": {
    "skills-server": {
      "\$typeName": "exa.cascade_plugins_pb.CascadePluginCommandTemplate",
      "command": "bash",
      "args": ["$PROJECT_DIR/start_server.sh"],
      "env": {}
    }
  }
}
JSONEOF
        echo -e "  ${GREEN}✓${NC} $ide_name — mcp_config.json created with MCP server"
    else
        # File exists (user has other MCP servers) — inject skills-server preserving existing entries
        python3 -c "
import json
config_file = '$config_file'
try:
    with open(config_file, 'r') as f:
        data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    data = {}
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['skills-server'] = {
    '\$typeName': 'exa.cascade_plugins_pb.CascadePluginCommandTemplate',
    'command': 'bash',
    'args': ['$PROJECT_DIR/start_server.sh'],
    'env': {}
}
with open(config_file, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && \
            echo -e "  ${GREEN}✓${NC} $ide_name — skills-server injected into mcp_config.json" || \
            echo -e "  ${YELLOW}⚠${NC} $ide_name — could not inject (edit manually: $config_file)"
    fi

    # Also ensure settings.json has basic config for gemini CLI compatibility
    inject_mcp_json "$HOME/.gemini/settings.json" "Gemini CLI (settings.json)"
}

# 1. Google Antigravity (Gemini) — uses mcp_config.json, NOT settings.json
inject_mcp_antigravity

# 2. Claude Code CLI — uses `claude mcp add` (can't inject, explain how)
if command -v claude &>/dev/null; then
    if claude mcp list 2>/dev/null | grep -q 'skills-server'; then
        echo -e "  ${GREEN}✓${NC} Claude Code CLI — MCP already registered"
    else
        claude mcp add --scope user skills-server "$MCP_CMD" "$MCP_ARG" 2>/dev/null && \
            echo -e "  ${GREEN}✓${NC} Claude Code CLI — MCP server registered via CLI" || \
            echo -e "  ${YELLOW}⚠${NC} Claude Code CLI — run manually: claude mcp add --scope user skills-server $MCP_CMD $MCP_ARG"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} Claude Code CLI — not installed (skip). Install: npm install -g @anthropic-ai/claude-code"
fi

# 3. Claude Desktop
CLAUDE_DESKTOP_CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
inject_mcp_json "$CLAUDE_DESKTOP_CONFIG" "Claude Desktop"

# 4. VS Code — project-level .vscode/mcp.json
VSCODE_MCP="$PROJECT_DIR/.vscode/mcp.json"
mkdir -p "$PROJECT_DIR/.vscode"
if [[ -f "$VSCODE_MCP" ]] && grep -q 'skills-server' "$VSCODE_MCP" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} VS Code — MCP already configured"
else
    cat > "$VSCODE_MCP" << VSEOF
{
  "servers": {
    "skills-server": {
      "command": "$MCP_CMD",
      "args": ["$MCP_ARG"],
      "env": {
        "PYTHONPATH": "$MCP_ENV_PP"
      }
    }
  }
}
VSEOF
    echo -e "  ${GREEN}✓${NC} VS Code — .vscode/mcp.json created"
fi

# 5. Cursor
inject_mcp_json "$HOME/.cursor/mcp.json" "Cursor"

# 6. OpenAI Codex CLI
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
mkdir -p "$CODEX_HOME"

# Auto-generate ~/.codex/AGENTS.md if it doesn't exist yet
if [[ ! -f "$CODEX_HOME/AGENTS.md" ]]; then
    cat > "$CODEX_HOME/AGENTS.md" << 'AGENTSEOF'
# Skills MCP Server — Codex Integration

You have access to **1,176+ curated AI agent skills** via an MCP server.
Use the following MCP tools to discover and load skills on demand:

- `list_skills()` — list all available skills
- `search_skills(query)` — search by keyword (e.g., "protein docking")
- `get_skill(id)` — get full SKILL.md content
- `list_agents()` — list agent personas
- `search_agents(query)` — search agents by keyword

Skills cover: bioinformatics, drug discovery, scientific writing,
molecular dynamics, DevOps, full-stack engineering, and more.

Local skills directory: `~/.codex/skills/`
AGENTSEOF
    echo -e "  ${GREEN}✓${NC} OpenAI Codex CLI — AGENTS.md created"
else
    echo -e "  ${GREEN}✓${NC} OpenAI Codex CLI — AGENTS.md already exists"
fi

# Auto-generate ~/.codex/config.toml MCP section if not configured
# Codex CLI uses [mcp_servers.<name>] format, NOT [mcp] servers = {...}
if [[ -f "$CODEX_HOME/config.toml" ]] && grep -q 'mcp_servers.skills-server' "$CODEX_HOME/config.toml" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} OpenAI Codex CLI — MCP already configured in config.toml"
else
    # Prefer using `codex mcp add` if available (generates correct format)
    if command -v codex &>/dev/null; then
        codex mcp add skills-server --env PYTHONPATH="$MCP_ENV_PP" -- "$MCP_CMD" "$MCP_ARG" 2>/dev/null && \
            echo -e "  ${GREEN}✓${NC} OpenAI Codex CLI — MCP server registered via CLI" || \
            echo -e "  ${YELLOW}⚠${NC} OpenAI Codex CLI — 'codex mcp add' failed, injecting manually"
    fi
    # Verify it was added, if not inject manually with correct format
    if ! grep -q 'mcp_servers.skills-server' "$CODEX_HOME/config.toml" 2>/dev/null; then
        cat >> "$CODEX_HOME/config.toml" << MCPEOF

# ── Skills MCP Server (auto-generated by sync_skills.sh) ──
[mcp_servers.skills-server]
command = "$MCP_CMD"
args = ["$MCP_ARG"]

[mcp_servers.skills-server.env]
PYTHONPATH = "$MCP_ENV_PP"
MCPEOF
        echo -e "  ${GREEN}✓${NC} OpenAI Codex CLI — MCP server added to config.toml"
    fi
fi

# 7. Qwen CLI — inject into settings.json, preserving existing keys
QWEN_HOME="${QWEN_HOME:-$HOME/.qwen}"
mkdir -p "$QWEN_HOME"

# Qwen's settings.json may have other top-level keys (security, ide, model, $version)
# We must preserve them and only add/update mcpServers.skills-server
if [[ -f "$QWEN_HOME/settings.json" ]] && grep -q 'skills-server' "$QWEN_HOME/settings.json" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} Qwen CLI — MCP already configured"
else
    python3 -c "
import json
config_file = '$QWEN_HOME/settings.json'
try:
    with open(config_file, 'r') as f:
        data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    data = {}
if 'mcpServers' not in data:
    data['mcpServers'] = {}
data['mcpServers']['skills-server'] = {
    'command': '$MCP_CMD',
    'args': ['$MCP_ARG'],
    'env': {'PYTHONPATH': '$MCP_ENV_PP'}
}
with open(config_file, 'w') as f:
    json.dump(data, f, indent=2)
" 2>/dev/null && \
        echo -e "  ${GREEN}✓${NC} Qwen CLI — MCP server injected into settings.json" || \
        echo -e "  ${YELLOW}⚠${NC} Qwen CLI — could not inject (edit manually: $QWEN_HOME/settings.json)"
fi

# Also create per-project mcp.json if Qwen supports it
if [[ -d "$PROJECT_DIR/.qwen" ]] || true; then
    mkdir -p "$PROJECT_DIR/.qwen"
    if [[ ! -f "$PROJECT_DIR/.qwen/mcp.json" ]] || ! grep -q 'skills-server' "$PROJECT_DIR/.qwen/mcp.json" 2>/dev/null; then
        cat > "$PROJECT_DIR/.qwen/mcp.json" << QWEOF
{
  "mcpServers": {
    "skills-server": {
      "command": "$MCP_CMD",
      "args": ["$MCP_ARG"],
      "env": {
        "PYTHONPATH": "$MCP_ENV_PP"
      }
    }
  }
}
QWEOF
        echo -e "  ${GREEN}✓${NC} Qwen CLI — project-level .qwen/mcp.json created"
    fi
fi

echo ""

# ─── Phase 4: Generate catalog ────────────────────────────────────────────────
echo -e "${CYAN}📋 Generating skills catalog...${NC}"
cd "$PROJECT_DIR"
if [[ -d ".venv" ]]; then
    source .venv/bin/activate 2>/dev/null || true
fi
PYTHONPATH="$PROJECT_DIR/server" python3 "$SCRIPT_DIR/build_catalog.py" 2>/dev/null && \
    echo -e "${GREEN}✅ Catalog generated: skills_index.json${NC}" || \
    echo -e "${YELLOW}⚠ Catalog generation skipped (run build_catalog.py manually)${NC}"

echo ""
total=$(find "$SKILLS_DIR" -name "SKILL.md" | wc -l | tr -d ' ')
echo -e "${CYAN}🧬 Total skills available: $total${NC}"

# ─── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}📌 Skills are now available in:${NC}"
echo -e "  ${GREEN}•${NC} Antigravity (Gemini):  ~/.gemini/antigravity/skills/"
echo -e "  ${GREEN}•${NC} Claude Code CLI:       ~/.claude/skills/"
echo -e "  ${GREEN}•${NC} VS Code Copilot:       .github/skills/ (this project)"
echo -e "  ${GREEN}•${NC} OpenAI Codex CLI:      ~/.codex/skills/ + AGENTS.md + config.toml"
echo -e "  ${GREEN}•${NC} Qwen CLI:              ~/.qwen/skills/ + settings.json"
echo -e ""
echo -e "  ${BLUE}Tip:${NC} For MCP Server (recommended), run:"
echo -e "    ${CYAN}claude mcp add --scope user skills-server $PROJECT_DIR/.venv/bin/python3 $PROJECT_DIR/server/mcp_skills_server.py${NC}"
echo -e ""

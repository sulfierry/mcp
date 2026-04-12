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

CURATED_BIO="structural-biology proteomics chemoinformatics machine-learning pathway-analysis data-visualization database-access workflow-management differential-expression single-cell variant-calling sequence-io read-alignment read-qc"

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
    echo -e "${CYAN}📚 Available skill sources (13 repos):${NC}"
    echo -e ""
    echo -e "  ${BLUE}── Bioinformatics & Science ──${NC}"
    echo -e "  ${GREEN}•${NC} ClawBio/ClawBio (skills/)"
    echo -e "  ${GREEN}•${NC} GPTomics/bioSkills (.)"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/claude-scientific-skills (scientific-skills/)"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/scientific-agent-skills (scientific-skills/) ★ 133 scientific skills"
    echo -e "  ${GREEN}•${NC} jaechang-hits/SciAgent-Skills (skills/)"
    echo -e ""
    echo -e "  ${BLUE}── Scientific Writing ──${NC}"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/claude-scientific-writer (skills/)"
    echo -e "  ${GREEN}•${NC} zhangchenhaobest/academic-research-skills (.)"
    echo -e "  ${GREEN}•${NC} InternScience/Awesome-Scientific-Skills (skills/)"
    echo -e ""
    echo -e "  ${BLUE}── Programming & DevOps ──${NC}"
    echo -e "  ${GREEN}•${NC} VoltAgent/awesome-claude-code-subagents ⭐16K (categories/)"
    echo -e "  ${GREEN}•${NC} tech-leads-club/agent-skills ⭐2K (packages/skills-catalog/skills/)"
    echo -e "  ${GREEN}•${NC} guanyang/antigravity-skills (skills/)"
    echo -e "  ${GREEN}•${NC} rmyndharis/antigravity-skills (skills/)"
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

# Sync from each source with appropriate curated list
# -- Bioinformatics & Science --
clone_and_sync "ClawBio/ClawBio" "https://github.com/ClawBio/ClawBio.git" "skills" ""
clone_and_sync "GPTomics/bioSkills" "https://github.com/GPTomics/bioSkills.git" "." "$CURATED_BIO"
clone_and_sync "K-Dense-AI/claude-scientific-skills" "https://github.com/K-Dense-AI/claude-scientific-skills.git" "scientific-skills" ""
clone_and_sync "K-Dense-AI/scientific-agent-skills" "https://github.com/K-Dense-AI/scientific-agent-skills.git" "scientific-skills" ""
clone_and_sync "jaechang-hits/SciAgent-Skills" "https://github.com/jaechang-hits/SciAgent-Skills.git" "skills" ""

# -- Scientific Writing --
clone_and_sync "K-Dense-AI/claude-scientific-writer" "https://github.com/K-Dense-AI/claude-scientific-writer.git" "skills" "$CURATED_WRITING"
clone_and_sync "zhangchenhaobest/academic-research-skills" "https://github.com/zhangchenhaobest/academic-research-skills.git" "." "$CURATED_ACADEMIC"
clone_and_sync "InternScience/Awesome-Scientific-Skills" "https://github.com/InternScience/Awesome-Scientific-Skills.git" "skills" ""

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

# ─── Phase 3: IDE Symlinks ────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}🔗 Setting up IDE symlinks...${NC}"

create_symlink() {
    local target="$1"
    local link_path="$2"
    local ide_name="$3"

    # Create parent directory if needed
    mkdir -p "$(dirname "$link_path")"

    # Check if already correctly linked
    if [[ -L "$link_path" ]]; then
        local current_target
        current_target="$(readlink "$link_path")"
        if [[ "$current_target" == "$target" ]]; then
            echo -e "  ${GREEN}✓${NC} $ide_name — already linked"
            return 0
        fi
        # Stale symlink → remove and recreate
        rm "$link_path"
    elif [[ -d "$link_path" ]]; then
        # Real directory exists → skip (don't overwrite user data)
        echo -e "  ${YELLOW}⚠${NC} $ide_name — skipped (real directory exists at $link_path)"
        return 0
    fi

    ln -sf "$target" "$link_path"
    echo -e "  ${GREEN}✓${NC} $ide_name — linked → $link_path"
}

# Google Antigravity (Gemini)
create_symlink "$SKILLS_DIR" "$HOME/.gemini/antigravity/skills" "Antigravity (Gemini)"

# Claude Code CLI
create_symlink "$SKILLS_DIR" "$HOME/.claude/skills" "Claude Code CLI"

# VS Code — GitHub Copilot Agent Skills
# Uses .github/skills/ in the MCP project itself for dev-time discovery
create_symlink "$SKILLS_DIR" "$PROJECT_DIR/.github/skills" "VS Code Copilot (project)"

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
echo -e ""
echo -e "  ${BLUE}Tip:${NC} For MCP Server (recommended), run:"
echo -e "    ${CYAN}claude mcp add --scope user skills-server $PROJECT_DIR/.venv/bin/python3 $PROJECT_DIR/server/mcp_skills_server.py${NC}"
echo -e ""

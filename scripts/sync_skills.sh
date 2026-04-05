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

# Check if a skill name is in a curated list
is_curated() {
    local name="$1"
    local list="$2"
    echo "$list" | tr ' ' '\n' | grep -qx "$name"
}

if $LIST_ONLY; then
    echo -e "${CYAN}📚 Available skill sources:${NC}"
    echo -e "  ${GREEN}•${NC} guanyang/antigravity-skills (skills/)"
    echo -e "  ${GREEN}•${NC} rmyndharis/antigravity-skills (skills/)"
    echo -e "  ${GREEN}•${NC} GPTomics/bioSkills (.)"
    echo -e "  ${GREEN}•${NC} K-Dense-AI/claude-scientific-skills (scientific-skills/)"
    echo -e "  ${GREEN}•${NC} jaechang-hits/SciAgent-Skills (skills/)"
    echo -e "  ${GREEN}•${NC} ClawBio/ClawBio (skills/)"
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
            .git|node_modules|__pycache__|resources|workflows|bioskills-installer|.github|.claude-plugin|assets|templates|tests|bot|docs|examples|img|scripts|slides|corpas-30x|robotary|GENOMEBOOK|commands|clawbio|demo|references) continue ;;
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
clone_and_sync "guanyang/antigravity-skills" "https://github.com/guanyang/antigravity-skills.git" "skills" "$CURATED_GUANYANG"
clone_and_sync "rmyndharis/antigravity-skills" "https://github.com/rmyndharis/antigravity-skills.git" "skills" "$CURATED_GUANYANG"
clone_and_sync "GPTomics/bioSkills" "https://github.com/GPTomics/bioSkills.git" "." "$CURATED_BIO"
clone_and_sync "K-Dense-AI/claude-scientific-skills" "https://github.com/K-Dense-AI/claude-scientific-skills.git" "scientific-skills" ""
clone_and_sync "jaechang-hits/SciAgent-Skills" "https://github.com/jaechang-hits/SciAgent-Skills.git" "skills" ""
clone_and_sync "ClawBio/ClawBio" "https://github.com/ClawBio/ClawBio.git" "skills" ""

echo -e "${GREEN}✅ Sync complete: $sync_count skills synced, $skip_count skipped (already exist)${NC}"

# Generate catalog
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

#!/usr/bin/env bash
# Purge redundant skills (Phase 1 — near-duplicate aliases).
# Safe: dry-run by default. Run with --apply to delete.
# Review audit/redundant_skills.md before applying.

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DROP_LIST="$ROOT/audit/phase1_drop.txt"
SKILLS_DIR="$ROOT/skills"
INDEX="$ROOT/skills_index.json"
APPLY=0
[[ "${1:-}" == "--apply" ]] && APPLY=1

if [[ ! -f "$DROP_LIST" ]]; then
  echo "missing $DROP_LIST — run audit first" >&2
  exit 1
fi

echo "Mode: $([[ $APPLY -eq 1 ]] && echo APPLY || echo DRY-RUN)"
echo "Drop list: $DROP_LIST"
echo

count=0
while IFS= read -r id; do
  [[ -z "$id" ]] && continue
  dir="$SKILLS_DIR/$id"
  if [[ -d "$dir" ]]; then
    echo "  drop  skills/$id/"
    count=$((count+1))
    if [[ $APPLY -eq 1 ]]; then
      rm -rf "$dir"
    fi
  else
    echo "  miss  $id (already gone)"
  fi
done < "$DROP_LIST"

echo
echo "$count dirs to drop"

if [[ $APPLY -eq 1 ]]; then
  echo
  echo "Rebuilding skills_index.json (removing dropped IDs)..."
  python3 - <<PY
import json, sys
drops={l.strip() for l in open("$DROP_LIST") if l.strip()}
data=json.load(open("$INDEX"))
before=len(data)
data=[s for s in data if s["id"] not in drops]
json.dump(data, open("$INDEX","w"), indent=2, ensure_ascii=False)
print(f"index: {before} -> {len(data)}")
PY
  echo
  echo "Restart skills-server for MCP to reload."
else
  echo
  echo "Preview only. Re-run with --apply to execute."
fi

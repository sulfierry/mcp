#!/usr/bin/env python3
"""
build_catalog.py — Generate skills_index.json from SKILL.md files.

Usage:
    python scripts/build_catalog.py
"""

import sys
from pathlib import Path

# Add server/ to path for importing SkillRegistry
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))

from skill_registry import SkillRegistry


def main():
    project_dir = Path(__file__).resolve().parent.parent
    skills_dir = project_dir / "skills"
    output_path = project_dir / "skills_index.json"

    registry = SkillRegistry(str(skills_dir))
    count = registry.scan()

    if count == 0:
        print("⚠ No skills found. Run sync_skills.sh first.")
        return

    registry.export_catalog_json(str(output_path))
    print(f"✅ Catalog generated: {output_path} ({count} skills)")


if __name__ == "__main__":
    main()

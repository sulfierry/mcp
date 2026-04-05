"""
Skill Registry — parses SKILL.md files and provides search/discovery.

Scans a directory tree for SKILL.md files, extracts YAML frontmatter
(name, description), and builds an in-memory index for fast lookup.
"""

from __future__ import annotations

import os
import re
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class SkillEntry:
    """Represents a single skill parsed from a SKILL.md file."""
    id: str                         # directory name (e.g. "molecular-docking")
    name: str                       # from frontmatter
    description: str                # from frontmatter
    path: str                       # relative path to SKILL.md
    category: str = ""              # optional category tag
    tags: list[str] = field(default_factory=list)
    source: str = ""                # origin repo or "custom"


class SkillRegistry:
    """
    In-memory registry of skills discovered from the filesystem.

    Usage:
        registry = SkillRegistry("/path/to/skills")
        registry.scan()
        results = registry.search("molecular docking")
    """

    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self._skills: dict[str, SkillEntry] = {}

    # ── Scanning ──────────────────────────────────────────────────────

    def scan(self) -> int:
        """Scan the skills directory and populate the registry. Returns count."""
        self._skills.clear()
        if not self.skills_dir.exists():
            return 0

        for skill_md in self.skills_dir.rglob("SKILL.md"):
            entry = self._parse_skill_md(skill_md)
            if entry:
                self._skills[entry.id] = entry

        return len(self._skills)

    def _parse_skill_md(self, path: Path) -> Optional[SkillEntry]:
        """Parse a SKILL.md file and extract frontmatter metadata."""
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None

        # Extract YAML frontmatter between --- delimiters
        fm = self._extract_frontmatter(content)
        if not fm:
            return None

        name = fm.get("name", "")
        description = fm.get("description", "")
        if not name:
            return None

        # Determine skill ID from directory name
        skill_dir = path.parent
        skill_id = skill_dir.name

        # Extract tags if present
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        category = fm.get("category", "")

        return SkillEntry(
            id=skill_id,
            name=name,
            description=description,
            path=str(path.relative_to(self.skills_dir)),
            category=category,
            tags=tags,
            source=fm.get("source", "custom"),
        )

    @staticmethod
    def _extract_frontmatter(content: str) -> Optional[dict]:
        """Extract YAML frontmatter from markdown content (lightweight, no pyyaml dependency)."""
        # Match --- delimited block at the start of the file
        match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return None

        fm_text = match.group(1)
        result = {}

        for line in fm_text.strip().split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Simple key: value parsing (handles most SKILL.md frontmatter)
            colon_idx = line.find(":")
            if colon_idx == -1:
                continue

            key = line[:colon_idx].strip()
            value = line[colon_idx + 1:].strip()

            # Remove surrounding quotes
            if value and value[0] in ('"', "'") and value[-1] == value[0]:
                value = value[1:-1]

            result[key] = value

        return result if result else None

    # ── Queries ───────────────────────────────────────────────────────

    def list_skills(self) -> list[dict]:
        """Return all skills as a list of dicts (id, name, description)."""
        return [
            {"id": s.id, "name": s.name, "description": s.description, "category": s.category}
            for s in sorted(self._skills.values(), key=lambda s: s.name.lower())
        ]

    def get_skill(self, skill_id: str) -> Optional[dict]:
        """Get full info + content for a skill by ID."""
        entry = self._skills.get(skill_id)
        if not entry:
            return None

        skill_md_path = self.skills_dir / entry.path
        try:
            content = skill_md_path.read_text(encoding="utf-8")
        except OSError:
            content = "[Error reading SKILL.md]"

        result = asdict(entry)
        result["content"] = content
        return result

    def search_skills(self, query: str) -> list[dict]:
        """Search skills by keyword matching on name, description, tags, and category."""
        query_lower = query.lower()
        tokens = query_lower.split()
        scored: list[tuple[float, SkillEntry]] = []

        for entry in self._skills.values():
            score = self._score_match(entry, tokens, query_lower)
            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            {"id": s.id, "name": s.name, "description": s.description,
             "category": s.category, "score": round(sc, 3)}
            for sc, s in scored[:20]
        ]

    @staticmethod
    def _score_match(entry: SkillEntry, tokens: list[str], full_query: str) -> float:
        """Score a skill entry against search tokens. Higher = better match."""
        score = 0.0
        searchable = f"{entry.name} {entry.description} {entry.category} {' '.join(entry.tags)}".lower()

        # Exact phrase match in name → highest
        if full_query in entry.name.lower():
            score += 10.0
        elif full_query in entry.description.lower():
            score += 5.0

        # Token-level matching
        for token in tokens:
            if token in entry.name.lower():
                score += 3.0
            if token in entry.id.lower():
                score += 2.5
            if token in entry.description.lower():
                score += 1.5
            if any(token in t.lower() for t in entry.tags):
                score += 2.0
            if token in entry.category.lower():
                score += 1.0

        return score

    def get_scripts(self, skill_id: str) -> Optional[dict[str, str]]:
        """Get helper scripts for a skill (if any exist in scripts/ subdirectory)."""
        entry = self._skills.get(skill_id)
        if not entry:
            return None

        skill_dir = self.skills_dir / Path(entry.path).parent
        scripts_dir = skill_dir / "scripts"

        if not scripts_dir.exists():
            return None

        scripts = {}
        for script_file in scripts_dir.iterdir():
            if script_file.is_file():
                try:
                    scripts[script_file.name] = script_file.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    scripts[script_file.name] = "[Error reading file]"

        return scripts if scripts else None

    # ── Catalog Export ────────────────────────────────────────────────

    def export_catalog(self) -> list[dict]:
        """Export the full catalog as a JSON-serializable list."""
        return [asdict(s) for s in sorted(self._skills.values(), key=lambda s: s.id)]

    def export_catalog_json(self, output_path: str) -> None:
        """Write the catalog to a JSON file."""
        catalog = self.export_catalog()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)

    @property
    def count(self) -> int:
        return len(self._skills)

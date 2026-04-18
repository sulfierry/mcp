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
    kind: str = "skill"             # "skill" or "agent" — namespace marker


class SkillRegistry:
    """
    In-memory registry of skills discovered from the filesystem.

    Usage:
        registry = SkillRegistry("/path/to/skills")
        registry.scan()
        results = registry.search("molecular docking")
    """

    def __init__(
        self,
        skills_dir: str,
        overlay_index: Optional[str] = None,
        kind: str = "skill",
        category_filter: Optional[list[str]] = None,
    ):
        self.skills_dir = Path(skills_dir)
        self.overlay_index = Path(overlay_index) if overlay_index else None
        self.kind = kind
        # Lowercase set for fast membership tests; empty/None = no filter
        self.category_filter: Optional[set[str]] = (
            {c.strip().lower() for c in category_filter if c.strip()}
            if category_filter else None
        )
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

        self._apply_overlay()
        self._apply_category_filter()
        return len(self._skills)

    def _apply_category_filter(self) -> None:
        """Drop entries whose category is not in the filter (applied after overlay)."""
        if not self.category_filter:
            return
        keep = {
            sid: entry for sid, entry in self._skills.items()
            if (entry.category or "").lower() in self.category_filter
        }
        self._skills = keep

    def _apply_overlay(self) -> None:
        """Apply category/tag overrides from overlay_index JSON if present."""
        if not self.overlay_index or not self.overlay_index.is_file():
            return
        try:
            data = json.loads(self.overlay_index.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        by_id = {item.get("id"): item for item in data if isinstance(item, dict)}
        for sid, entry in self._skills.items():
            ov = by_id.get(sid)
            if not ov:
                continue
            if ov.get("category"):
                entry.category = ov["category"]
            if ov.get("tags"):
                entry.tags = ov["tags"] if isinstance(ov["tags"], list) else entry.tags

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
            kind=self.kind,
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

    MAX_DESC_CHARS = 160

    @classmethod
    def _trim_desc(cls, text: str, max_chars: int | None = None) -> str:
        if not text:
            return ""
        n = max_chars if max_chars is not None else cls.MAX_DESC_CHARS
        if n <= 0 or len(text) <= n:
            return text
        # cut on last word boundary before n
        head = text[:n].rsplit(" ", 1)[0].rstrip(" .,;:—-")
        return head + "…"

    @staticmethod
    def _name_is_derived(name: str, sid: str) -> bool:
        """True if `name` is a trivial title-case of `id` (so emission is redundant)."""
        derived = sid.replace("-", " ").replace("_", " ").lower()
        return name.strip().lower() == derived

    @classmethod
    def _compact_item(cls, s: SkillEntry) -> dict:
        """Emit compact entry dropping redundant `name` and empty/misc `category`."""
        item: dict = {"id": s.id}
        if not cls._name_is_derived(s.name, s.id):
            item["name"] = s.name
        if s.category and s.category != "misc":
            item["category"] = s.category
        return item

    def list_skills(
        self,
        limit: int = 50,
        offset: int = 0,
        category: str = "",
        compact: bool = True,
        desc_chars: int = MAX_DESC_CHARS,
    ) -> dict:
        """Return skills with pagination + optional category filter.

        compact=True omits description entirely. When compact=False,
        descriptions are truncated to `desc_chars` (default 160, 0 = full).
        Redundant `name` (derivable from id) and empty/`misc` categories are
        dropped to save bytes.
        """
        entries = sorted(self._skills.values(), key=lambda s: s.name.lower())
        if category:
            cat = category.lower()
            entries = [s for s in entries if s.category.lower() == cat]
        total = len(entries)

        if limit <= 0:
            limit = total
        sliced = entries[offset: offset + limit]

        if compact:
            items = [self._compact_item(s) for s in sliced]
        else:
            items = []
            for s in sliced:
                item = self._compact_item(s)
                desc = self._trim_desc(s.description, desc_chars)
                if desc:
                    item["description"] = desc
                items.append(item)
        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "count": len(items),
            "has_more": offset + len(items) < total,
            "skills": items,
        }

    @staticmethod
    def group_by_prefix(items: list[dict], min_group: int = 2) -> dict:
        """Group compact items by id prefix (first `-` segment).

        Singletons stay under `_`. Reduces repeated prefix bytes in large lists.
        """
        from collections import defaultdict
        buckets: dict[str, list[dict]] = defaultdict(list)
        for it in items:
            prefix = it["id"].split("-", 1)[0]
            buckets[prefix].append(it)
        groups: dict[str, list] = {"_": []}
        for prefix, bucket in buckets.items():
            if len(bucket) < min_group:
                groups["_"].extend(bucket)
                continue
            # Strip prefix from ids to save bytes
            groups[prefix] = [
                {**it, "id": it["id"][len(prefix) + 1:] or it["id"]}
                for it in bucket
            ]
        if not groups["_"]:
            groups.pop("_")
        return groups

    @staticmethod
    def to_markdown(payload: dict) -> str:
        """Render a list_skills / search_skills payload as compact markdown."""
        lines = []
        header_bits = []
        for k in ("total", "count", "has_more", "offset", "limit", "query"):
            if k in payload:
                header_bits.append(f"{k}={payload[k]}")
        if header_bits:
            lines.append("<!-- " + " ".join(header_bits) + " -->")

        skills = payload.get("skills") or payload.get("results") or []
        if isinstance(skills, dict):
            # prefix-grouped
            for prefix, bucket in skills.items():
                lines.append(f"\n## {prefix}" if prefix != "_" else "\n## misc")
                for it in bucket:
                    desc = it.get("description")
                    tail = f" — {desc}" if desc else ""
                    cat = f" [{it.get('category','')}]" if it.get("category") else ""
                    lines.append(f"- {it['id']}{cat}{tail}")
        else:
            for it in skills:
                desc = it.get("description")
                tail = f" — {desc}" if desc else ""
                cat = f" [{it.get('category','')}]" if it.get("category") else ""
                lines.append(f"- {it['id']}{cat}{tail}")

        if "categories" in payload:
            lines.append("\n## categories")
            for c in payload["categories"]:
                lines.append(f"- {c['category']}: {c['count']}")
        return "\n".join(lines)

    def list_categories(self) -> list[dict]:
        """Return counts per category for compact overview."""
        from collections import Counter
        c = Counter(s.category or "uncategorized" for s in self._skills.values())
        return [{"category": k, "count": v} for k, v in sorted(c.items(), key=lambda x: -x[1])]

    def get_skill(self, skill_id: str, section: str = "") -> Optional[dict]:
        """Get info + content for a skill.

        If `section` is provided, returns only the H2 section whose title
        contains that substring (case-insensitive). Everything before the
        first H2 is returned whenever section is empty.
        """
        entry = self._skills.get(skill_id)
        if not entry:
            return None

        skill_md_path = self.skills_dir / entry.path
        try:
            content = skill_md_path.read_text(encoding="utf-8")
        except OSError:
            content = "[Error reading SKILL.md]"

        if section:
            content = self._extract_section(content, section)

        result = asdict(entry)
        result["content"] = content
        if section:
            result["section"] = section
        return result

    @staticmethod
    def _extract_section(md: str, needle: str) -> str:
        """Return the H2 section whose title contains `needle` (case-insensitive)."""
        needle = needle.lower()
        parts = re.split(r"(?m)^## +", md)
        # parts[0] is pre-H2 preamble; skip it
        for chunk in parts[1:]:
            title_line = chunk.split("\n", 1)[0]
            if needle in title_line.lower():
                return "## " + chunk.rstrip()
        # fallback: list available sections
        titles = [c.split("\n", 1)[0] for c in parts[1:]]
        return f"[Section '{needle}' not found. Available: {titles}]"

    def list_sections(self, skill_id: str) -> Optional[list[str]]:
        """Return H2 section titles for a skill (cheap TOC without full content)."""
        entry = self._skills.get(skill_id)
        if not entry:
            return None
        try:
            md = (self.skills_dir / entry.path).read_text(encoding="utf-8")
        except OSError:
            return []
        return re.findall(r"(?m)^## +(.+?)$", md)

    def search_skills(
        self,
        query: str,
        limit: int = 20,
        compact: bool = False,
        desc_chars: int = MAX_DESC_CHARS,
    ) -> list[dict]:
        """Search skills by keyword matching on name, description, tags, and category."""
        query_lower = query.lower()
        tokens = query_lower.split()
        scored: list[tuple[float, SkillEntry]] = []

        for entry in self._skills.values():
            score = self._score_match(entry, tokens, query_lower)
            if score > 0:
                scored.append((score, entry))

        scored.sort(key=lambda x: x[0], reverse=True)

        out = []
        for sc, s in scored[:limit]:
            item = self._compact_item(s)
            item["score"] = round(sc, 3)
            if not compact:
                desc = self._trim_desc(s.description, desc_chars)
                if desc:
                    item["description"] = desc
            out.append(item)
        return out

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

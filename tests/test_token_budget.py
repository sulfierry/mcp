"""Token budget regression guard.

Asserts MCP tool outputs stay under documented thresholds. Fail loudly on
regression rather than silently bloat context on every session.

Run: PYTHONPATH=server .venv/bin/python3 -m pytest tests/test_token_budget.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "server"))

from skill_registry import SkillRegistry  # noqa: E402


def _registry() -> SkillRegistry:
    r = SkillRegistry(
        str(ROOT / "skills"),
        overlay_index=str(ROOT / "skills_index.json"),
    )
    r.scan()
    return r


def test_list_skills_default_compact_under_5kb():
    r = _registry()
    res = r.list_skills(limit=50, compact=True)
    payload = json.dumps(res, separators=(",", ":"))
    assert len(payload) < 5_000, f"list_skills(50) minified {len(payload)} B > 5 KB budget"


def test_list_skills_md_under_2kb():
    r = _registry()
    res = r.list_skills(limit=50, compact=True)
    md = SkillRegistry.to_markdown(res)
    assert len(md) < 2_000, f"list_skills(50) md {len(md)} B > 2 KB budget"


def test_full_catalog_md_grouped_under_50kb():
    r = _registry()
    full = r.list_skills(limit=0, compact=True)
    grouped = SkillRegistry.group_by_prefix(full["skills"])
    md = SkillRegistry.to_markdown({"skills": grouped})
    assert len(md) < 50_000, f"full catalog md+group {len(md)} B > 50 KB budget"


def test_outline_under_1kb():
    r = _registry()
    titles = r.list_sections("llm-inference-servers")
    payload = json.dumps({"sections": titles})
    assert len(payload) < 1_000, f"outline {len(payload)} B > 1 KB budget"


def test_get_skill_strips_frontmatter_by_default():
    r = _registry()
    entry = r.get_skill("llm-inference-servers")
    assert not entry["content"].startswith("---"), "frontmatter not stripped"
    assert "\n\n\n" not in entry["content"], "blank-line runs not collapsed"
    # Verbose path/tags fields dropped by default
    assert "path" not in entry, "path should be hidden when verbose=False"
    assert "tags" not in entry, "tags should be hidden when verbose=False"


def test_get_skill_saves_at_least_10pct_over_verbose():
    r = _registry()
    verbose = r.get_skill("llm-inference-servers", verbose=True, keep_frontmatter=True)
    compact = r.get_skill("llm-inference-servers")
    v = json.dumps(verbose, indent=2)
    c = json.dumps(compact, separators=(",", ":"))
    ratio = 1 - len(c) / len(v)
    assert ratio >= 0.10, f"only {ratio*100:.1f}% savings on get_skill (target 10%)"


def test_redundant_name_dropped():
    r = _registry()
    # Find a skill whose name equals title-cased id — should omit `name`
    for s in r._skills.values():
        if SkillRegistry._name_is_derived(s.name, s.id):
            item = SkillRegistry._compact_item(s)
            assert "name" not in item, f"derived name not dropped for {s.id}"
            return
    # If no derived names exist, skip gracefully
    try:
        import pytest
        pytest.skip("no derived-name skill in registry")
    except ImportError:
        return


def test_misc_category_dropped():
    r = _registry()
    for s in r._skills.values():
        if s.category == "misc":
            item = SkillRegistry._compact_item(s)
            assert "category" not in item, f"misc category not dropped for {s.id}"
            return
    try:
        import pytest
        pytest.skip("no misc category in registry")
    except ImportError:
        return

#!/usr/bin/env python3
"""Regenerate skill catalog tables in README.md from SKILL.md frontmatter.

Reads all skills/*/SKILL.md files, extracts name/description/category from
YAML frontmatter, and replaces the tables between marker comments in README.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"

MARKER_START_GENERAL = "<!-- TOC:START:GENERAL -->"
MARKER_END_GENERAL = "<!-- TOC:END:GENERAL -->"
MARKER_START_TAILORED = "<!-- TOC:START:TAILORED -->"
MARKER_END_TAILORED = "<!-- TOC:END:TAILORED -->"


def extract_frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    import yaml
    try:
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def build_table(skills: list[dict]) -> str:
    lines = ["| Skill | What it does |", "|---|---|"]
    for s in skills:
        name = s["name"]
        desc = s["description"]
        if len(desc) > 120:
            desc = desc[:117] + "..."
        lines.append(f"| [**{name}**](skills/{name}/) | {desc} |")
    return "\n".join(lines)


def replace_between(text: str, start_marker: str, end_marker: str, replacement: str) -> str:
    """Replace content between two markers (including the markers)."""
    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
    return re.sub(pattern, replacement, text, flags=re.DOTALL)


def main() -> int:
    readme_text = README.read_text()

    general = []
    tailored = []

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = extract_frontmatter(skill_md.read_text())
        if not fm:
            continue
        entry = {
            "name": fm.get("name", skill_dir.name),
            "description": fm.get("description", ""),
            "category": (fm.get("metadata") or {}).get("category", "general"),
        }
        if entry["category"] == "tailored":
            tailored.append(entry)
        else:
            general.append(entry)

    general_block = f"{MARKER_START_GENERAL}\n{build_table(general)}\n{MARKER_END_GENERAL}"
    tailored_block = f"{MARKER_START_TAILORED}\n{build_table(tailored)}\n{MARKER_END_TAILORED}"

    new_text = replace_between(readme_text, MARKER_START_GENERAL, MARKER_END_GENERAL, general_block)
    new_text = replace_between(new_text, MARKER_START_TAILORED, MARKER_END_TAILORED, tailored_block)

    README.write_text(new_text)

    print(f"Catalog synced:")
    print(f"  General:   {len(general)} skills")
    print(f"  Tailored:  {len(tailored)} skills")
    print(f"  Total:     {len(general) + len(tailored)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

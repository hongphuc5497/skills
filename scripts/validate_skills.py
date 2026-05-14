#!/usr/bin/env python3
"""Validate all skills in the skills/ directory."""
import sys
import os
import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"


def validate_skill(skill_path: Path) -> tuple[bool, str]:
    """Validate a single skill directory."""
    skill_name = skill_path.name
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        return False, f"SKILL.md not found"

    content = skill_md.read_text()

    # Check frontmatter exists
    if not content.startswith("---"):
        return False, "No YAML frontmatter"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)

    # Parse YAML
    try:
        import yaml
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a dictionary"
    except Exception as e:
        return False, f"Invalid YAML: {e}"

    # Check required fields
    if "name" not in frontmatter:
        return False, "Missing 'name' field"
    if "description" not in frontmatter:
        return False, "Missing 'description' field"

    # Check name matches directory
    fm_name = frontmatter.get("name", "")
    if fm_name != skill_name:
        return False, f"Name mismatch: frontmatter={fm_name}, directory={skill_name}"

    # Check line count
    line_count = len(content.splitlines())
    if line_count > 500:
        return False, f"SKILL.md exceeds 500 lines ({line_count})"

    return True, "Valid"


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"Skills directory not found: {SKILLS_DIR}")
        return 1

    skills = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if not skills:
        print("No skills found")
        return 1

    passed = 0
    failed = 0

    for skill_path in skills:
        ok, msg = validate_skill(skill_path)
        if ok:
            print(f"  ✓ {skill_path.name}")
            passed += 1
        else:
            print(f"  ✗ {skill_path.name}: {msg}")
            failed += 1

    print(f"\nTotal: {len(skills)} | ✓ {passed} passed | ✗ {failed} failed")

    if failed > 0:
        print(f"\n{failed} skill(s) failed validation")
        return 1

    print("\nAll skills valid ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())

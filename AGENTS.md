# AGENTS.md — Skills Catalog

Subagents available when working in this repo.

## skill-validator

Validates skills under `skills/` — frontmatter, naming, version, structure, anti-patterns. Read-only.

Checks:
1. Confirm `name` field equals directory name
2. Confirm version is semver
3. Confirm SKILL.md ≤ 500 lines

## skill-author

Draft or edit a single SKILL.md plus references. Bumps metadata.version.

Rules:
1. Read existing SKILL.md before editing
2. Match conventions of neighboring skills
3. Bump version: patch for wording, minor for new capability
4. Keep SKILL.md under 500 lines; spill to references/

**Never edit files outside target skill directory. Never commit.**

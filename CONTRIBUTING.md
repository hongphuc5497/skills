# CONTRIBUTING.md

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-new-skill`)
3. Make your changes
4. Commit using conventional commits
5. Push to your branch (`git push origin feature/my-new-skill`)
6. Open a Pull Request

## Skill Structure

Each skill must follow this structure:

```
skill-name/
├── SKILL.md              # Required: Skill definition
├── docs/                 # Optional: human-only docs, never auto-loaded
│   └── README.md         # Optional: catalog-browsing docs
├── references/           # Optional: docs the agent loads on demand
├── scripts/              # Optional: Executable scripts
└── assets/               # Optional: Templates and resources
```

### SKILL.md Requirements

```yaml
---
name: skill-name
version: 1.0.0
description: Clear description of what the skill does and when to use it
---
```

- `name` must match the parent directory name (lowercase, hyphens)
- `version` follows semver
- Description is a one-liner of what it does

## Commit Message Convention

- `feat:` New feature or skill
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## New Skill Checklist

- [ ] SKILL.md with valid YAML frontmatter
- [ ] Name matches directory name
- [ ] Version is semver
- [ ] SKILL.md under 500 lines
- [ ] Optional: docs/README.md for catalog

## Attribution

Skill source files in this collection are MIT licensed. See individual SKILL.md frontmatter for author details.

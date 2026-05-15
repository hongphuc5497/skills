# Changelog

## v1.1.1

- fix: add alt text to caveman-compress logo image (discovered by markdown-lint CI)
- fix: add trailing newlines to caveman, caveman-commit, caveman-review SKILL.md

## v1.1.0

### Structural Improvements
- Added Expected Output, Edge Cases, Acceptance Criteria to all 10 tailored skills
- Added negative-trigger clauses to all descriptions
- asm eval mean score: 80 → 88. Zero D-grade skills.

### Upstream Sync
- Pulled latest SKILL.md from luongnv89/skills (14 skills updated)
- Pulled latest from JuliusBrussee/caveman — all 7 skills: new README.md, caveman-compress gained scripts/ directory
- Added sources.json: dependency manifest for 22 upstream skills
- Added scripts/sync_upstreams.py: batch upstream sync (2 API calls, SHA256 comparison, dry-run/apply modes)

## v1.0.1

- Fix release workflow permissions (Actions → Read and write)
- Release workflow verified via tag push

## v1.0.0 — Initial Release

- Repo skeleton with installers, CONTRIBUTING, LICENSE, and catalog
- 15 general skills: auto-push, brand-name-checker, code-optimizer, code-review, context-hub, docs-generator, idea-validator, oss-ready, prd-generator, quick-healthy-recipes, release-manager, security-setup, seo-ai-optimizer, tasks-generator, usability-review
- 8 tailored skills: caveman, caveman-commit, caveman-compress, caveman-help, caveman-review, hermes-config, multi-agent-orchestrator, rtk
- CI/CD: validate-skills, markdown-lint, sync-toc, release workflows

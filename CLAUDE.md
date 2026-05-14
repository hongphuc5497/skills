# CLAUDE.md — Agent Skills Catalog

Project context for agents working on this repo. Skills live here; the runtime that loads them lives in `~/.hermes/skills/`, `~/.claude/skills/`, etc. (out of scope for edits).

## Commands

- Validate a skill: check frontmatter, naming, version, structure
- Scaffold a new skill: `mkdir -p skills/<name> && touch skills/<name>/SKILL.md`

This is a markdown-only repo. No npm, pnpm, make, or test commands.

## Architecture

- `skills/<name>/SKILL.md` — required skill definition with YAML frontmatter
- `skills/<name>/references/` — on-demand docs the agent loads when the skill triggers
- `skills/<name>/scripts/` — executable helpers
- `install.sh` / `remote-install.sh` — end-user installers (bash, no deps)

## Hard Rules

1. Bump `metadata.version` (semver) on every SKILL.md edit.
2. Quote any frontmatter string containing `:` `#` `-` `<` `>` `|` `,` `&` `?` `!`.
3. Keep each SKILL.md under 500 lines. Split overflow into `references/`.
4. Never edit `dist/` artifacts.
5. Never commit `*-workspace/` or local scratch files.
6. Never commit secrets or `.env`.
7. **Never add `Co-Authored-By: Claude`** to any commit message.
8. Do not commit or push without explicit user request.
9. Use Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`).
10. Skill `name` must exactly match parent directory name (lowercase, hyphens).
11. Run validation against any skill you touched before declaring done.

## Token Efficiency

- Never re-read files you just wrote. You know the contents.
- Never re-run commands to "verify" unless outcome was uncertain.
- Don't echo back large blocks of code or file contents unless asked.
- Batch related edits into single operations.
- Skip confirmations like "I'll continue..." Just do it.

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

## Agent Ops Rules for Codex

When this repo contains `.ai/protocol.md`, use Agent Ops as the coordination
protocol.

Before editing:

1. Read `.ai/protocol.md`, `TASK.md`, and `ROUTING.md`.
2. Run `scripts/agent-ops-tool.py status` when available.
3. If no task is active and the user requested implementation, start one with
   `scripts/agent-ops-tool.py start`.
4. Claim files before editing with `scripts/agent-ops-tool.py claim`.

During work:

- Keep Codex as the active owner unless ownership is explicitly transferred.
- Use Augment for codebase discovery and impact mapping.
- Use OpenClaw for product/scope review only.
- Use OpenCode only for isolated file sets.
- Do not let two agents edit the same concern simultaneously.

Before finishing:

1. Run the task-specific verification.
2. Run `scripts/agent-ops-tool.py check`.
3. Finish with `scripts/agent-ops-tool.py finish done --verification "..."`
   or explicitly park/kill the task.


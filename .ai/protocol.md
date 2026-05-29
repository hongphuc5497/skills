# Agent Ops Protocol

Version: 0.1.0

Agent Ops is a repo-native coordination protocol for AI coding agents. The
protocol answers five questions before an agent edits code:

1. Who owns the active task?
2. Which files are claimed?
3. Which workflow applies?
4. What verification is required?
5. Where should handoffs, decisions, and results be recorded?

The protocol is intentionally file-first. Any agent can read the files without
installing a daemon. Tools and MCP servers are adapters over the same state.

## Canonical Files

| File | Purpose | Generated? |
| --- | --- | --- |
| `TASK.md` | Human-readable active task lock | yes |
| `.ai/state/active-task.json` | Machine-readable active task lock | yes |
| `.ai/state/file-claims.json` | Machine-readable file ownership claims | yes |
| `.ai/state/handoffs.jsonl` | Append-only handoff log | yes |
| `.ai/tasks/*.md` | Task records | yes |
| `.ai/tasks/archive/*.json` | Finished task summaries | yes |
| `ROUTING.md` | Human-readable routing rules | no |
| `DECISIONS.md` | Durable architecture/workflow decisions | no |

## Agent Contract

Every implementation agent must:

- Call or read `agent_ops.status` before editing.
- Claim files before editing them.
- Refuse overlapping claims unless the active owner transfers ownership.
- Log handoffs when delegating or returning work.
- Run or record verification before finishing.

Advisory agents may read everything but should not claim files unless they
become the active owner.

## State Objects

### Task

Stored in `.ai/state/active-task.json` while active.

Required fields:

- `id`
- `title`
- `owner`
- `status`
- `started_at`
- `task_file`

Optional fields:

- `repo`
- `workflow`
- `verification`
- `files_in_scope`
- `out_of_scope`

### File Claims

Stored in `.ai/state/file-claims.json`.

Claims are glob-like strings. They are human-enforced in v0.1 and checked for
exact duplicate claims by scripts. Deep overlap detection can come later.

Example:

```json
{
  "claims": [
    {
      "task_id": "20260518-120000-fix-ci",
      "owner": "Codex",
      "paths": ["src/auth/**", "tests/auth/**"],
      "created_at": "2026-05-18T12:00:00+00:00",
      "reason": "active implementation"
    }
  ]
}
```

### Handoffs

Stored as JSON Lines in `.ai/state/handoffs.jsonl`.

Example:

```json
{"from":"Codex","to":"OpenCode","task_id":"20260518-120000-fix-ci","files":["scripts/check.sh"],"acceptance":"script passes shellcheck","created_at":"2026-05-18T12:30:00+00:00"}
```

## Tool Interface

The MVP tool bridge is:

```bash
scripts/agent-ops-tool.py status
scripts/agent-ops-tool.py route "debug failing playwright test"
scripts/agent-ops-tool.py start "fix CI failure" --owner Codex --repo /path/to/repo
scripts/agent-ops-tool.py claim "src/auth/**" "tests/auth/**" --owner Codex
scripts/agent-ops-tool.py handoff --to OpenCode --files "scripts/check.sh" --acceptance "passes bash -n"
scripts/agent-ops-tool.py finish done --verification "pytest tests/auth"
scripts/agent-ops-tool.py check
```

All commands print JSON so agents can consume them.

## Integration Principle

Agent Ops is not the user interface for daily coding. It is the shared protocol
agents use to coordinate safely. Humans can use the CLI, but agents should read
the repo protocol or call the tool bridge directly.


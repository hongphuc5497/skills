# Agent Routing

## Tool Roles

| Tool | Default Role | Can Edit? | Use When | Do Not Use For |
| --- | --- | --- | --- | --- |
| Codex | Brain, operator, default implementer | Yes, when owner | Planning, repo edits, verification, scripts, docs, PR prep | Long-running unattended work without a task lock |
| Augment | Codebase navigator | No by default | Symbol search, impact mapping, architecture discovery | Owning product decisions or writing active changes |
| Hermes | Automation runner, notification surface | Only in isolated task | Scheduled checks, local status, reminders, background workflows | Canonical memory or unreviewed edits |
| OpenCode | Alternate implementer | Only in delegated lane | Small isolated patches, CLI-first refactors, local experiments | Editing the same files as Codex |
| OpenClaw | Product/design/review critic | No by default | Plan challenge, product taste, PR review, scope pressure | Acting as the active implementer |
| GitHub Actions | Verification and remote signal | No | CI, regression gates, release checks | Workflow orchestration logic |
| Local LLMs | Cheap/offline draft worker | No by default | Summaries, first-pass classification, private/offline rough work | Final authority, risky code edits, security-sensitive review |

## Agent Ops Protocol

When `.ai/protocol.md` exists, agents should use Agent Ops before editing:

```bash
scripts/agent-ops-tool.py status
scripts/agent-ops-tool.py route "task description"
scripts/agent-ops-tool.py claim "path/or/glob"
```

The protocol is the product surface. The CLI and scripts are adapters.

## Brain Decision

Codex is the brain for v1.

Reason: it already has repo access, memory conventions, scripts, browser and
GitHub integrations, and can execute to completion. Making another tool the
brain adds handoff cost before there is a proven product.

## Memory Decision

Canonical memory lives in repo markdown plus Codex durable memory:

- `.ai/memory/` for project-specific patterns and weekly learning.
- `DECISIONS.md` for durable architecture choices.
- Codex memory for cross-repo user preferences.

Hermes logs and state are not canonical memory because they can contain secrets
and are harder to review.

## Notification Decision

Use Hermes for local reminders and GitHub Actions for remote signals.

Examples:

- Hermes: "daily review due", "automation failed", "stale active task".
- GitHub Actions: CI failed, lint failed, test matrix failed.

## Routing Rules

1. If the task changes files, assign exactly one active owner.
2. If the task changes files, claim the file set before editing.
3. If the task is codebase discovery, ask Augment first, then inspect files.
4. If the task is implementation, Codex owns by default.
5. If a task can be split, split by file ownership, not by vague topic.
6. If review is needed, OpenClaw reviews the plan/product angle and Codex or CI
   reviews code behavior.
7. If the work is repetitive and scheduled, Hermes can run it after the manual
   workflow has succeeded at least twice.
8. If the task is speculative, it goes to `.ai/experiments/README.md` first.

## Delegation Rules

Delegation is allowed only when all are true:

- The delegated work has a bounded file set.
- The active owner writes the acceptance criteria.
- The delegate does not touch files owned by another active task.
- The delegate reports changed files and verification.
- The active owner reviews before merging into the task narrative.

Good:

```text
OpenCode owns only scripts/task-status.sh and scripts/task-finish.sh.
Codex owns ROUTING.md and .ai/ARCHITECTURE.md.
```

Bad:

```text
Codex and OpenCode both improve "workflow docs".
```

## Handoff Protocol

Use this when transferring ownership:

```markdown
## Handoff

From: Codex
To: OpenCode
Task: Improve task status script
Files owned: `scripts/task-status.sh`
Do not touch: `TASK.md`, `.ai/ARCHITECTURE.md`
Acceptance: script prints active task, owner, status, task file
Verify: `bash -n scripts/task-status.sh && ./scripts/task-status.sh`
Return with: changed files, verification output, risks
```

## Conflict Rule

If two agents need the same file, stop and serialize the work. The current
owner finishes or parks first. No merge games for solo indie workflow.

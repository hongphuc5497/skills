# Supported Agent Ops Integrations

Agent Ops has two integration surfaces:

1. **Install integration**: files that teach an agent to follow the repo protocol.
2. **Live coordination**: runtime behavior once the agent is participating in a task.

Keep these separate. Adding an install template for an agent does not mean Agent
Ops can drive or inspect that agent's live sessions. This mirrors the useful
boundary in AI DevKit, where environment setup and live agent control are
separate systems.

## Status Legend

| Status | Meaning |
| --- | --- |
| Ready | Template exists and is wired into `scripts/install-integration.sh`. |
| Advisory | Agent is expected to read or review, not own edits by default. |
| Watcher | Agent monitors state or sends notifications, not implementation edits. |

## Matrix

| Agent | Status | Install command | Artifact | Live coordination role |
| --- | --- | --- | --- | --- |
| Codex | Ready | `agent-ops install codex` | Appends Agent Ops rules to `AGENTS.md` | Default owner, implementer, verifier |
| Claude Code | Ready | `agent-ops install claude` | Appends Agent Ops rules to `CLAUDE.md` | Brain or worker when assigned owner |
| OpenCode | Ready | `agent-ops install opencode` | Writes `.ai/integrations/opencode-instructions.md` | Isolated implementation lane only |
| Augment | Advisory | `agent-ops install augment` | Writes `.ai/integrations/augment-discovery.md` | Codebase discovery and impact mapping |
| OpenClaw | Advisory | `agent-ops install openclaw` | Writes `.ai/integrations/openclaw-review.md` | Product, scope, and review critic |
| Hermes | Watcher | `agent-ops install hermes` | Writes `.ai/integrations/hermes-monitor.md` | Stale-task monitor and notifier |

## What each agent reads and writes

This is the contract you can rely on when an agent participates in a task. If
an agent is not listed as writing a file, it should never modify that file
even with explicit user permission — that boundary is what makes Agent Ops a
coordination tool instead of a chaos tool.

| Agent | Reads | Writes (when active owner) | Never writes |
| --- | --- | --- | --- |
| Codex | `AGENTS.md`, `.ai/TASK.md`, `.ai/ROUTING.md`, `.ai/state/*` | Anything claimed for the active task, `.ai/state/*` via `ao` commands | Files claimed by another task |
| Claude Code | `CLAUDE.md`, `.ai/TASK.md`, `.ai/ROUTING.md`, `.ai/state/*` | Anything claimed for the active task, `.ai/state/*` via `ao` commands | Files claimed by another task |
| OpenCode | `.ai/integrations/opencode-instructions.md`, the delegated file set | Only the delegated file set, via `ao handoff` return | Anything outside its handoff |
| Augment | Full repo (read-only by default) | — | Implementation files, `.ai/state/*` |
| OpenClaw | The plan, the changed diff, `.ai/ROUTING.md`, `.ai/DECISIONS.md` | `.ai/integrations/openclaw-review.md` only | Implementation files, `.ai/state/*` |
| Hermes | `.ai/state/active-task.json`, `.ai/state/handoffs.jsonl` | Notification channels only | Repo files, `.ai/state/*` |

## How to learn the protocol fast

```bash
agent-ops init --interactive   # picks agents to install and seeds a tutorial
agent-ops tutorial             # add the tutorial later, post-init
agent-ops doctor               # diagnostics if anything looks off
```

The tutorial runs the actual coordination loop — claim, delegate, finish — on
a fake task so you learn the commands without risking real code.

## Routing tasks to the right agent

Built-in routing matches keywords like `bug` / `review` / `experiment` to a
default owner + workflow. To override per-repo (e.g., always route to
Claude, or add a `security` category), drop a `.ai/routing.json` file. See
[docs/routing.md](routing.md) for the schema; `agent-ops init` ships a copy
of `.ai/routing.example.json` you can adapt.

List the same support surface from the shell:

```bash
agent-ops install list
```

## Adding Another Agent

Before adding a new agent, answer these separately:

1. What install artifact does the agent read?
2. Can it claim implementation files, or is it advisory/watch-only?
3. Which files may it edit when it owns work?
4. Which verification command proves the integration works?

Then make the smallest file-first change:

1. Add `.ai/integrations/templates/<agent>/...` instructions.
2. Add one case to `scripts/install-integration.sh`.
3. Add the copied file to `scripts/init-repo.sh` if seeded repos need it.
4. Update this matrix and the quick reference in `docs/plug-and-play.md`.
5. Verify with `agent-ops install <agent> --dry-run` and `agent-ops check`.

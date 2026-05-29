# Agent Integrations

These templates make Agent Ops available inside existing AI coding agents.

The product surface is the shared protocol, not a standalone app:

- Agents read `.ai/protocol.md`.
- Agents call `scripts/agent-ops-tool.py` when they need structured state.
- Humans can still use scripts directly when needed.

## Install

Preview:

```bash
./scripts/install-integration.sh codex --dry-run
```

Install:

```bash
./scripts/install-integration.sh codex
./scripts/install-integration.sh opencode
```

## Supported MVP Integrations

| Integration | Output |
| --- | --- |
| `codex` | Appends Agent Ops rules to `AGENTS.md` |
| `claude` | Appends Agent Ops rules to `CLAUDE.md` |
| `opencode` | Writes `.ai/integrations/opencode-instructions.md` |
| `augment` | Writes `.ai/integrations/augment-discovery.md` |
| `openclaw` | Writes `.ai/integrations/openclaw-review.md` |
| `hermes` | Writes `.ai/integrations/hermes-monitor.md` |

The installer is intentionally conservative. It does not modify home-level
tooling or external config in v0.1.


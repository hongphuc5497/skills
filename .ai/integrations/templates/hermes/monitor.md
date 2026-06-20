# Agent Ops Rules for Hermes

Hermes is the monitor and notification surface.

Allowed:

- Check task freshness.
- Notify when the active task is stale.
- Create weekly review reminders.
- Report automation failures.

Not allowed by default:

- Edit implementation files.
- Treat Hermes logs as canonical memory.
- Copy secrets from session logs or state.

Suggested monitor command:

```bash
scripts/agent-ops-tool.py status
scripts/agent-ops-tool.py check
```

Notify when:

- active task is older than 48 hours
- weekly review is missing
- file claims exist but no active task exists


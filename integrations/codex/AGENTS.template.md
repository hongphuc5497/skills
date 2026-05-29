# Agent Ops Rules for Codex

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


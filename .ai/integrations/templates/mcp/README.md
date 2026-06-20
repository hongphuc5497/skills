# MCP Integration

The MVP exposes a JSON command bridge at `scripts/agent-ops-tool.py`. This is
not a full MCP server yet. It is deliberately smaller:

- no Python dependencies
- no background daemon
- JSON in, JSON out
- works from any coding agent that can run shell commands

Future MCP tools should wrap the same commands:

| MCP Tool | Bridge Command |
| --- | --- |
| `agent_ops.status` | `scripts/agent-ops-tool.py status` |
| `agent_ops.route_task` | `scripts/agent-ops-tool.py route` |
| `agent_ops.start_task` | `scripts/agent-ops-tool.py start` |
| `agent_ops.claim_files` | `scripts/agent-ops-tool.py claim` |
| `agent_ops.handoff` | `scripts/agent-ops-tool.py handoff` |
| `agent_ops.finish_task` | `scripts/agent-ops-tool.py finish` |
| `agent_ops.check` | `scripts/agent-ops-tool.py check` |

Build a true MCP server only after this bridge is useful in two real repos.


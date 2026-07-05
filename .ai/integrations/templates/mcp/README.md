# Agent Ops over MCP

`agent-ops mcp` is a stdio MCP server exposing the coordination protocol as
native tools: `status`, `route`, `start`, `claim`, `release`, `handoff`,
`finish`, `check`, `doctor`. It wraps the repo-vendored
`scripts/agent-ops-tool.py`, so tool results are exactly the CLI's JSON —
the MCP surface and the CLI can never disagree.

## Claude Code

```bash
# project scope (run inside the repo)
claude mcp add agent-ops -- npx -y @hongphuc5497/agent-ops@latest mcp
```

Or in `.mcp.json` at the repo root:

```json
{
  "mcpServers": {
    "agent-ops": {
      "command": "npx",
      "args": ["-y", "@hongphuc5497/agent-ops@latest", "mcp"]
    }
  }
}
```

## Codex

In `~/.codex/config.toml` (Codex does not guarantee cwd, so pass `--repo`):

```toml
[mcp_servers.agent-ops]
command = "npx"
args = ["-y", "@hongphuc5497/agent-ops@latest", "mcp", "--repo", "/abs/path/to/repo"]
```

## Identity

Each agent must know who it is so claims and the pre-commit hook work:

```bash
AGENT_OPS_OWNER=claude   # per-process — correct when agents share one checkout
git config agent-ops.owner <name>   # repo-wide human fallback
```

Precedence: `AGENT_OPS_OWNER` > `git config agent-ops.owner`.

## Notes

- `--repo <path>` defaults to the server's cwd; the server refuses to start
  against a repo without `.ai/protocol.md` (run `agent-ops init` first).
- If the repo's vendored tool version differs from the npm package version,
  the `status` tool result carries a warning — run `agent-ops upgrade`.
- Tool errors (claim conflicts, no active task) come back as `isError` tool
  results with the CLI's structured JSON, including `remedy` hints.

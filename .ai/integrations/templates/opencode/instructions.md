# Agent Ops Rules for OpenCode

OpenCode is an isolated implementation lane, not the default owner.

Before editing:

```bash
scripts/agent-ops-tool.py status
scripts/agent-ops-tool.py claim "path/or/glob" --owner OpenCode --reason "delegated lane"
```

Only edit files explicitly delegated to OpenCode. If a claim is denied, stop and
return a handoff request instead of editing.

Return with:

- changed files
- verification command
- result
- risks

Do not update `.ai/TASK.md`, `.ai/ROUTING.md`, or `.ai/DECISIONS.md` unless
those files are explicitly delegated.


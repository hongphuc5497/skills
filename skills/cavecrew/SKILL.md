---
name: cavecrew
description: "Decision guide for delegating to caveman-style subagents. Use when the user wants to delegate work to subagents, spawn parallel workers, save main context, or mentions cavecrew. Not for simple single-file edits the main thread can do directly."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# Cavecrew — Caveman Subagent Delegation

Three subagent presets that emit caveman-compressed output. Same job as normal subagents; difference is the tool-result they return is ~60% smaller, so main context lasts longer.

## When to use cavecrew vs main thread

| Task | Use |
|---|---|
| "Where is X defined / what calls Y / list uses of Z" | **cavecrew-investigator** |
| Same but you also want suggestions/architecture commentary | Normal subagent |
| Surgical edit, ≤2 files, scope obvious | **cavecrew-builder** |
| New feature / 3+ files / cross-cutting refactor | Main thread |
| Review diff, branch, or file for bugs | **cavecrew-reviewer** |
| Deep code review with rationale + alternatives | Normal subagent |
| One-line answer you already know | Main thread, no subagent |

**Rule of thumb:** if you'd want the subagent's output in 1/3 the tokens, pick cavecrew. If you'd want prose, pick normal.

## Subagent Presets

### cavecrew-investigator
Find code locations, trace definitions, list callers/callees. Returns file paths + line numbers + one-line purpose. No prose.

```
Output format:
  src/auth/login.ts:42 — validateSession()
  src/auth/middleware.ts:15 — calls validateSession on /api/*
  src/auth/types.ts:8 — SessionPayload interface
```

### cavecrew-builder
Surgical edits, ≤2 files. Returns diff summary in caveman-compressed format: what changed, why, line numbers.

```
Output format:
  + src/api/users.ts:23-35 — add GET /users/:id endpoint
  ~ src/api/routes.ts:12 — register new route
  Reason: mobile client needs profile without full user payload
```

### cavecrew-reviewer
Reviews diffs/branches for bugs. Returns caveman-review format: one line per finding with severity prefix.

```
Output format:
  L42: bug: user null after .find(). Add guard.
  L88: risk: no retry on 429. Wrap in backoff.
  L120: nit: 50-line fn. Extract validate/normalize/persist.
```

## When NOT to cavecrew

- The subagent output IS the deliverable (e.g., a report, a generated doc)
- Security findings that need full explanation
- User explicitly asked for detailed analysis
- Subagent needs to write 3+ files or do cross-cutting changes
- Multi-step workflows with dependencies between steps

## Boundaries

Cavecrew is a decision guide — it tells you WHEN to delegate, not HOW to spawn subagents. The actual delegation mechanism (delegate_task, subagent spawn) is tool-specific. The caveman output format is the key: shorter = more context survives.

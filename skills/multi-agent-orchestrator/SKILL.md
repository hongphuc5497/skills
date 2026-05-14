---
name: multi-agent-orchestrator
description: "Orchestrate work across multiple AI coding agents (Hermes, Codex, Claude Code) — delegate tasks in parallel, merge results, coordinate complex workflows."
license: MIT
effort: max
metadata:
  version: 1.0.0
  author: hongphuc5497
---

# Multi-Agent Orchestrator

Coordinate parallel work across Hermes, Codex, and Claude Code agents.

## When to Use

Use when a task benefits from multiple agents working in parallel — different perspectives, different model strengths, or independent sub-tasks. Trigger on phrases like "run this across agents", "orchestrate", "parallel execution", "use all agents".

## Available Agents

| Agent | Primary Use | Model |
|-------|-------------|-------|
| **Hermes** | Primary — planning, execution, fine-tuning | DeepSeek V4 Flash |
| **Codex** | Code generation, rapid prototyping | OpenAI Codex |
| **Claude Code** | Complex reasoning, code review | Claude |

## Pattern

### 1. Decompose Task
Split the work into independent sub-tasks that don't share state:
- Task A: Research/synthesis (Hermes)
- Task B: Code generation (Codex)
- Task C: Code review (Claude Code or Hermes)

### 2. Parallel Execution
Use `delegate_task` with batch mode (`tasks` array, up to 3 concurrent):
- Each subagent gets its own isolated context + terminal
- Pass all relevant context explicitly (no memory sharing)

### 3. Merge & Validate
- Collect results from all subagents
- Resolve conflicts (prefer Hermes for final decisions)
- Run validation: typecheck, lint, tests

## Instructions

1. Decide which agents suit which sub-tasks
2. Use `delegate_task` with `tasks` array for parallel execution
3. Pass full context to each subagent (they have no memory)
4. Collect results and merge
5. Validate merged output
6. Report final state to user

## Notes

- Subagents cannot use `clarify` — don't use for tasks needing user input mid-flight
- Subagent summaries are self-reports — verify file creation / side effects
- Leaf subagents cannot delegate further

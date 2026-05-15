---
name: caveman-help
description: "Quick-reference card for all caveman modes, skills, and commands. One-shot display, not a persistent mode. Use when user asks about caveman commands or how to use caveman features. Not for normal conversation, debugging, or code review tasks."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# Caveman Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in caveman style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | Tell agent "caveman lite" | Drop filler. Keep sentence structure. |
| **Full** | Tell agent "caveman" | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | Tell agent "caveman ultra" | Extreme compression. Bare fragments. Tables over prose. |

Mode stick until changed or session end.

## Skills

| Skill | What it do |
|-------|-----------|
| **caveman-commit** | Terse commit messages. Conventional Commits. Subject ≤50 chars. |
| **caveman-review** | One-line PR comments: `L42: bug: user null. Add guard.` |
| **caveman-compress** | Compress .md files to caveman prose. Saves ~46% input tokens. |
| **caveman-help** | This card. |
| **cavecrew** | Subagent delegation decision guide. |

## Deactivate

Say "stop caveman" or "normal mode". Resume anytime by telling agent to use caveman mode.

## Expected Output

When triggered, produce a markdown reference card with mode table, skill table, and deactivate instructions. Output is one-shot — do not persist mode or write flag files.

## Edge Cases

- **Already in caveman mode**: Still show the card. Don't change mode.
- **Unknown mode requested**: Show the card anyway with available modes.
- **User asks for help but also a specific task**: Show the card first, then do the task.

## Acceptance Criteria

- Mode table present with all available modes and triggers.
- Skill table present with all sub-skills.
- Deactivate instructions included.
- No mode state changed on disk or in memory.

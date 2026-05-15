---
name: caveman-help
description: "Quick-reference card for all caveman modes, skills, and commands. One-shot display, not a persistent mode. Use when user asks about caveman commands, modes, or how to use caveman features."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# Caveman Help

Display this reference card when invoked. One-shot — do NOT change mode or persist anything. Output in caveman style.

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
| **caveman-commit** | Terse commit messages. Conventional Commits. ≤50 char subject. |
| **caveman-review** | One-line PR comments: `L42: bug: user null. Add guard.` |
| **caveman-compress** | Compress .md files to caveman prose. Saves ~46% input tokens. |
| **caveman-help** | This card. |

## Deactivate

Say "stop caveman" or "normal mode". Resume anytime by telling agent to use caveman mode.

## Intensity Quick Reference

```
lite:  No filler/hedging. Keep sentence structure.
full:  Drop articles. Fragments OK. Short synonyms.
ultra: Abbreviate everything. Arrows (→). One word when possible.
```

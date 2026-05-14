---
name: caveman-commit
description: "Ultra-compressed commit message generator following caveman communication style. Cuts noise from PR descriptions and commit logs."
license: MIT
metadata:
  version: 1.0.0
  category: tailored
  author: hongphuc5497
---

# Caveman Commit

Generate ultra-compressed commit messages in caveman style.

## When to Use

Use when the user asks to commit, write a commit message, or says "caveman commit". Trigger on phrases like "caveman commit", "short message", "terse commit", "minimal commit".

## Style Guide

Caveman-lite: terse, no filler/pleasantries/hedging, fragment OK.

Examples:

```
feat: add RSS feed generation
→ "feat: RSS feed gen"

fix: resolve memory leak in batch processor
→ "fix: memory leak in batch proc"

docs: update API reference for v2 endpoints
→ "docs: API ref v2"
```

## Ultra mode (for full compression)

Drop articles (a/an/the), use abbreviations, single-word where possible:

```
fix: resolve issue with null pointer exception in user authentication when session expires
→ "fix: null ptr in auth on session expiry"
```

## Instructions

1. Read `git diff --cached` or check staged files context
2. Generate a conventional commit title (max 72 chars)
3. Apply caveman compression:
   - Remove articles (a/an/the)
   - Use abbreviations (feat→feat, fix→fix, docs→docs)
   - Drop filler words (actually, basically, literally)
   - Use short synonyms (add→add, fix→fix, remove→rm)
   - Fragments OK for body
4. Keep conventional commit prefix: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
5. Body (optional): compressed bullet points only if needed

## Caveats

- Don't sacrifice clarity for brevity on security-critical changes
- Security fixes get full conventional messages
- Breaking changes: include `!` after prefix + note in body

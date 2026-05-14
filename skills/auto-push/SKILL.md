---
name: auto-push
description: "Generate a commit message, stage all changes, and push to remote after scanning for secrets, large files, and protected-branch risks. Skip for opening PRs, code review, or cutting releases/tags."
license: MIT
metadata:
  version: 1.0.2
  author: hongphuc5497
---

# Commit and Push Everything

**CAUTION**: Stage ALL changes, commit, and push to remote. Use only when confident all changes belong together.

## When to Use

Trigger this skill when the user asks to "commit and push everything", "ship this", "auto-push", or otherwise wants a one-shot stage-commit-push for the current working tree. Skip when they want PRs, code review, releases, or tags.

## Sync Repo Before Edits
Before creating/updating/deleting files in an existing repository, sync the current branch with remote:

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If the working tree is not clean, stash first, sync, then restore:

```bash

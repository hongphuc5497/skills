---
name: auto-push
description: "Generate a commit message, stage all changes, and push to remote after scanning for secrets, large files, and protected-branch risks. Not for opening PRs, code review, or cutting releases and tags."
license: MIT
metadata:
  version: 1.0.1
  author: hongphuc5497
  category: tailored
---

# Commit and Push Everything

**CAUTION**: Stage ALL changes, commit, and push to remote. Use only when confident all changes belong together.

## When to Use

Trigger this skill when the user asks to "commit and push everything", "ship this", "auto-push", or otherwise wants a one-shot stage-commit-push for the current working tree. Skip when they want PRs, code review, releases, or tags.

## Sync Repo Before Edits

```bash
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin
git pull --rebase origin "$branch"
```

If working tree not clean:

```bash
git stash push -u -m "pre-sync"
branch="$(git rev-parse --abbrev-ref HEAD)"
git fetch origin && git pull --rebase origin "$branch"
git stash pop
```

## Pre-push Checks

### 1. Secret Scan
```bash
git diff --stat | head -5
# Check for: API keys, tokens, passwords, .env files
```

### 2. Large File Check
```bash
git diff --cached --stat | awk '{ if ($3 ~ /[0-9]+/ && $3+0 > 1000000) print "large: "$2 }'
```
Flag files >1MB. Ask user before committing large files.

### 3. Protected Branch Check
If current branch is `main` or `master`, ask for confirmation before force-push.

## Generate Commit Message

Generate a concise conventional commit message describing all changes.

## Push

```bash
git push origin "$(git rev-parse --abbrev-ref HEAD)"
```

## Expected Output

Summary of what was committed and pushed:
```
Pushed feature/add-auth  (3 files) to origin/feature/add-auth
Changes: feat(auth): implement JWT-based login middleware
```

## Edge Cases

- **No changes to commit**: Report "Working tree clean. Nothing to push."
- **Diverged remote**: Pull and rebase. Ask user if conflicts arise.
- **Git hooks fail**: Report hook output. Push stops — wait for user decision.
- **Network error**: Report the error and suggest retrying.
- **Protected branch detected**: Require explicit confirmation before force-push.

## Acceptance Criteria

- Secret/large file scan runs before any commit.
- Commit message is generated, not generic ("Updated files").
- Push succeeds or error is reported with specific reason.

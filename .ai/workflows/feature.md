# Feature Workflow

## Template

```markdown
User pain:
Acceptance:
Owner:
Files in scope:
Out of scope:
Verification:
```

## Steps

1. Start task.
2. Write acceptance criteria.
3. Ask Augment for existing code surfaces if editing another repo.
4. Add regression tests first when behavior is risky.
5. Implement smallest useful version.
6. Run matching tests/build/browser check.
7. Update `DECISIONS.md` if the workflow rule changed.
8. Finish task.

## Default Prompt

```text
You are the active owner for this feature. Keep the diff small. Do not edit
outside the listed files. Implement acceptance criteria only. Report changed
files, verification commands, and remaining risk.
```


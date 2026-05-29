# Debugging Workflow

## Rule

No fix without a reproduced failure or a clearly stated reason reproduction is
not possible.

## Steps

1. Capture the exact failure command or user action.
2. Save the observed error text in the task file.
3. Ask Augment where the behavior likely lives.
4. Read the relevant files.
5. State one root-cause hypothesis.
6. Add a regression test or minimal repro.
7. Implement the smallest fix.
8. Rerun the failing command.

## Debug Note Template

```markdown
Failure:
Command:
Expected:
Actual:
Hypothesis:
Fix:
Verified:
```


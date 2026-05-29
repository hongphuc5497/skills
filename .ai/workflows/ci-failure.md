# CI Failure Workflow

## Steps

1. Identify failing workflow, job, and step.
2. Extract only the relevant log lines.
3. Map the failure to a local command.
4. Reproduce locally.
5. Patch smallest surface.
6. Run matching local verification.
7. Rerun CI.

## Avoid

- Blind dependency upgrades.
- Rerunning CI repeatedly without a local theory.
- Fixing unrelated lint while debugging one failure.


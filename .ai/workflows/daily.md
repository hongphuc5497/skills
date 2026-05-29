# Daily Workflow

Purpose: reduce context switching and force one useful outcome.

## Start

```bash
./scripts/ao status
```

If no task is active:

```bash
./scripts/ao start "short task title" --owner Codex
```

## Pick Work

Choose from this order:

1. Active customer/user pain.
2. Broken workflow blocking shipping.
3. Follow-up from `DECISIONS.md`.
4. Highest-scoring experiment.
5. Parking-lot item only if it beats the current active bet.

## End

Before stopping:

- Verification command run.
- Durable decision logged only if reusable.
- Experiment promoted, parked, or killed.
- Active task finished or intentionally parked.

```bash
./scripts/ao finish done
```

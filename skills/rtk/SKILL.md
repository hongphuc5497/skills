---
name: rtk
description: "RTK (Rust Token Killer) — CLI proxy that compresses noisy shell output by 60-90%. Use when piping commands through rtk for token savings. Not for interactive commands (REPLs, prompts), shell composition, or when exact stdout/stderr is needed."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# RTK — Rust Token Killer

Token-optimized CLI proxy. Compresses dev operations output by 60-90%.

## Installation

```bash
cargo install rtk
# Verify:
rtk --version
```

## Meta Commands

```bash
rtk gain              # Show token savings analytics
rtk gain --history    # Show command usage history with savings
rtk discover          # Analyze history for missed opportunities
rtk proxy <cmd>       # Execute raw command without filtering (debugging)
```

## Usage

Pipe any noisy command through `rtk` to compress output:

```bash
rtk git status        # Compact status summary
rtk git diff          # Compressed diff
rtk grep              # Search with token-aware output
rtk pytest            # Test results summary
rtk npm run build     # Build output compressed
rtk tsc               # Typecheck errors compacted
rtk lint              # Lint results compressed
rtk docker            # Docker output condensed
rtk curl              # HTTP response compressed
rtk json              # JSON output compressed
```

## When to Use RTK

**Use RTK for:**
- Noisy commands where you only need the signal, not full output
- Repetitive output patterns (test suites, linters, build logs)
- Large outputs that would flood the context window
- Commands you run frequently where every token counts

**Skip RTK (use raw command) for:**
- Exact stdout/stderr needed for debugging
- Interactive commands (REPLs, prompts)
- Shell composition and piping
- Commands where output is already terse (< 100 tokens)

## Token Savings

| Command | Raw tokens | RTK tokens | Savings |
|---------|-----------|------------|---------|
| `git status` | ~500 | ~80 | 84% |
| `git diff` | ~2000 | ~200 | 90% |
| `pytest -v` | ~3000 | ~400 | 87% |
| `npm run build` | ~1500 | ~300 | 80% |
| `tsc --noEmit` | ~800 | ~150 | 81% |

## Pairing with Caveman

RTK compresses **tool output** (shell commands). Caveman compresses **conversation** (your responses). Together: full token optimization stack.

## Expected Output

Compressed command output with the signal preserved. The exact output shape depends on the command — RTK strips noise (progress bars, repeated patterns, verbose headers) and keeps the signal (errors, results, summaries).

## Edge Cases

- **Zero-length output**: Shows nothing. Rerun with `rtk proxy` to debug.
- **Command errors**: Error messages are preserved (not compressed).
- **Binary/encoded output**: Pass through unchanged.
- **rtk not installed**: Error message with install instructions.

## Acceptance Criteria

- Signal preserved (errors, warnings, test failures, build errors).
- Noise stripped (progress bars, repeated patterns, verbose headers).
- Savings measurable via `rtk gain`.

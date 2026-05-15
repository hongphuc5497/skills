---
name: caveman-stats
description: >
  Show token savings from caveman mode. Estimates savings based on communication intensity level vs baseline verbose responses. Use when user asks about caveman savings, token stats, or how much caveman helps. Not for precise token counting or debug...
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---
# Caveman Stats

Estimates token savings from caveman communication mode.

## Savings by Intensity

| Mode | Reduction | Example |
|------|-----------|---------|
| **lite** | ~40% | Drop filler, keep sentences |
| **full** | ~65% | Drop articles, fragments OK |
| **ultra** | ~80% | Abbreviations, arrows, one-word answers |

These are estimates. Actual savings depend on task type — code generation saves less (code is unchanged), conversation saves more.

## How to Calculate

Count the difference between what you said and what you would have said in verbose mode. Caveman removes:
- Articles (a, an, the)
- Filler (just, really, basically)
- Pleasantries (sure, certainly, happy to)
- Hedging (might, perhaps, could consider)
- Redundant qualifiers

## Real-World Example

Verbose response (~200 tokens):
> "I'd be happy to help you with that! Let me take a look at the issue you're experiencing. It seems like the authentication middleware is throwing a null pointer exception when the user's session has already expired. I think we should add a null check before accessing the session object."

Caveman full (~70 tokens, -65%):
> "Auth middleware throws null ptr on expired session. Missing null check before session access. Fix: add `if (!session) return 401`."

## Expected Output

Summary of estimated token savings by intensity level with example breakdown. No live session data — estimates based on communication pattern analysis.

```
Lite:  ~40%  — drop filler, keep sentences
Full:  ~65%  — drop articles, fragments OK
Ultra: ~80%  — abbreviations, arrows, one-word
```

## Edge Cases

- **Session has no caveman usage**: Report "No caveman usage detected in this session."
- **Mixed intensity levels**: Report per-phase breakdown if phases are distinguishable.
- **Zero-length response**: Not applicable — caveman only applies to non-empty responses.

## Acceptance Criteria

- Savings estimates clearly labeled as "estimated", not hard data.
- Intensity levels documented with expected reduction percentages.
- Example provided showing verbose vs caveman comparison.
- Note that real token tracking requires agent-specific hooks (caveman-stats.js).

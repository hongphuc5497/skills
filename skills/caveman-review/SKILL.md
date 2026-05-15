---
name: caveman-review
description: "Ultra-compressed code review comments. Cuts noise from PR feedback while preserving actionable signal. Each comment is one line: location, problem, fix. Use when reviewing code, PRs, or diffs."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# Caveman Code Review

Write code review comments terse and actionable. One line per finding. Location, problem, fix. No throat-clearing.

## Rules

**Format:** `L<line>: <problem>. <fix>.` — or `<file>:L<line>: ...` when reviewing multi-file diffs.

**Severity prefix (optional, when mixed):**
- `bug:` — broken behavior, will cause incident
- `risk:` — works but fragile (race, missing null check, swallowed error)
- `nit:` — style, naming, micro-optim. Author can ignore
- `q:` — genuine question, not a suggestion

**Drop:**
- "I noticed that...", "It seems like...", "You might want to consider..."
- "This is just a suggestion but..." — use `nit:` instead
- "Great work!", "Looks good overall but..." — say it once at the top, not per comment
- Restating what the line does — the reviewer can read the diff
- Hedging ("perhaps", "maybe", "I think") — if unsure use `q:`

**Keep:**
- Exact line numbers
- Exact symbol/function/variable names in backticks
- Concrete fix, not "consider refactoring this"
- The *why* if the fix isn't obvious from the problem statement

## Examples

```
Good:
  L23: bug: `user.profile.name` crashes when profile null. Add `user.profile?.name`.
  L42: risk: fetch in loop creates N queries. Batch with `Promise.all`.
  L67: nit: `data` too generic. Rename `invoiceList`.

Bad:
  L23: I noticed that on this line, it seems like there might be a potential issue with the user profile where if the profile is null, the name access could potentially throw an error. You might want to consider adding a null check or optional chaining.
```

## Auto-Clarity

Drop terse mode for: security findings (CVE-class bugs need full explanation + reference), architectural disagreements (need rationale, not just a one-liner), and onboarding contexts where the author is new and needs the "why". In those cases write a normal paragraph, then resume terse for the rest.

## Boundaries

Reviews only — does not write the code fix, does not approve/request-changes, does not run linters. Output the comment(s) ready to paste into the PR.

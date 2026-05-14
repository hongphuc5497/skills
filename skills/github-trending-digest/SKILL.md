---
name: github-trending-digest
description: "Automate GitHub Trending digest — fetch trending repos, summarize with LLM, format HTML, and publish to Substack. Cron M/W/F 9AM."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
---

# GitHub Trending Digest

Automate fetching, summarizing, and publishing GitHub Trending repos to Substack.

## When to Use

Use when working on the GitHub Trending Digest pipeline at `~/playground/github-digest/`. Trigger on phrases like "run the digest", "publish trending", "update the cron job", "fix the substack publisher".

## Project Location

```bash
~/playground/github-digest/
```

## Architecture

1. **Fetch** — Playwright scrapes `github.com/trending` via headless Chromium
2. **Summarize** — DeepSeek API generates concise HTML descriptions per repo
3. **Format** — HTML injected into Substack editor via ProseMirror `page.evaluate()`
4. **Publish** — Cron M/W/F at 9AM via Hermes cronjob system

## Substack Credentials

- Publication: `hongphuc5497.substack.com`
- Login: email-based (not OAuth)
- Note: Live publish may be blocked by onboarding checklist

## Instructions

1. Navigate to project directory
2. Run main script: review then `python3 main.py` or similar
3. Check cron status with `cronjob list`
4. If publish fails, check Substack onboarding checklist

## Cron Setup

```bash
# Schedule via Hermes cronjob
# Runs M/W/F at 9AM
```

## Troubleshooting

- **Substack login fails**: Check cookies, may need fresh headless Chromium session
- **HTML injection broken**: Check ProseMirror editor state before `page.evaluate()`
- **No trending data**: Check Playwright browser compatibility

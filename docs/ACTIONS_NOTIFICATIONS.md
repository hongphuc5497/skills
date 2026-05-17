# GitHub Actions Failure Notifications

This repo sends Slack and Telegram notifications when tracked GitHub Actions
workflows fail.

## Current Scope

- `Lint Markdown` watches `lint`
- `Validate Skills` watches `validate`
- `Sync TOC` watches `sync`
- `Release` watches `release`
- Notify on: failed watched job only
- Do not notify on: cancelled, skipped, or successful runs

## Required GitHub Secrets

Add these as repository secrets, or organization secrets scoped to this repo:

| Secret | Required for | Notes |
| --- | --- | --- |
| `SLACK_WEBHOOK_URL` | Slack | Incoming webhook URL for the target Slack channel. |
| `TELEGRAM_BOT_TOKEN` | Telegram | Bot token from BotFather or the Hermes Telegram bot. |
| `TELEGRAM_CHAT_ID` | Telegram | Target user, group, or channel chat ID. |

Missing notification secrets do not fail the workflow. The notification job
prints a skip message for the missing channel and continues.

## Message Contents

Each alert includes the repository, workflow, watched job, branch/ref, short
commit SHA, actor, triggering event, run number, and a link to the failed run.
Telegram uses HTML formatting with escaped dynamic values.

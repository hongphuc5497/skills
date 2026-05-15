---
name: hermes-config
description: "Configure Hermes Agent — providers, models, tools, skills, voice, gateway, plugins. Uses hermes CLI commands. Not for troubleshooting network issues, debugging agent responses, or customizing system prompts."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
  category: tailored
---

# Hermes Agent Configuration

Configure, extend, or troubleshoot Hermes Agent.

## When to Use

Use when the user asks to configure, set up, install, enable, disable, modify, or troubleshoot Hermes Agent — its CLI, config, models, providers, tools, skills, voice, gateway, plugins, or any feature. Always load the `hermes-agent` skill first via `skill_view(name='hermes-agent')`.

## Key Commands

```bash
hermes config set <key> <value>        # Set config values
hermes config get <key>                # Get config values
hermes tools                           # List available tools
hermes setup                           # Full setup wizard
hermes skills list                     # List installed skills
hermes skills install <name>           # Install a skill
```

## Config Locations

- Main config: `~/.hermes/config.yaml`
- Skills: `~/.hermes/skills/`
- Audio cache: `~/.hermes/audio_cache/`

## Common Tasks

### Add a Provider

```bash
hermes config set providers.<name>.api_key <key>
hermes config set providers.<name>.base_url <url>
```

### Change Model

```bash
hermes config set provider <provider>
hermes config set model <model-name>
```

### Install a Skill

```bash
hermes skills install <name>
# Or load from this repo:
hermes skills install https://github.com/hongphuc5497/skills --skill <name>
```

## Current Config (from memory)

- Provider: deepseek
- Model: deepseek-v4-flash

**Always verify actual config with `hermes config get` before making changes.**

## Expected Output

Command suggestions with exact syntax. When a config change is made, output the `hermes config set` command the user needs to run, or explain what to change in config.yaml directly.

## Edge Cases

- **Config key doesn't exist**: Output the full config path. E.g., "providers.deepseek.api_key" not just "api_key".
- **Value contains spaces or special chars**: Wrap in quotes in the command.
- **Config file locked by another process**: Wait and retry. Don't edit the file while it's being read.
- **User has no config file yet**: Suggest running `hermes setup` first.

## Acceptance Criteria

- Every command suggestion uses exact `hermes` CLI syntax.
- Config paths are fully qualified (e.g. `providers.deepseek.api_key`).
- Safety notice included when changing provider/model mid-session.

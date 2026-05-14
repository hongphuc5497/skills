---
name: hermes-config
description: "Configure Hermes Agent — providers, models, tools, skills, voice, gateway, plugins. Uses hermes CLI commands, not guesswork."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
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

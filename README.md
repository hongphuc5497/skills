<p align="center">
  <img src="assets/logo/logo-icon.svg" alt="Hong Phuc Skills" width="120">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
  <a href="https://github.com/hongphuc5497/skills/releases"><img src="https://img.shields.io/github/v/release/hongphuc5497/skills?label=version" alt="Latest Release"></a>
  <a href="https://github.com/hongphuc5497/skills"><img src="https://img.shields.io/github/stars/hongphuc5497/skills?style=social" alt="GitHub Stars"></a>
</p>

# Skills Collection — hongphuc5497

Curated agent skills for AI coding tools (Hermes, Claude Code, Codex, Cursor, Windsurf, Copilot) — a mix of community-vetted skills and personal workflow automations.

[**Browse the catalog**](#catalog) | [**Install**](#install) | [**CI notifications**](docs/ACTIONS_NOTIFICATIONS.md)

---

## Install

Pick one skill:

```bash
npx skills add https://github.com/hongphuc5497/skills --skill <name>
```

Pick several:

```bash
npx skills add https://github.com/hongphuc5497/skills --skill code-review --skill auto-push
```

Or grab everything:

```bash
npx skills add https://github.com/hongphuc5497/skills
```

### Local install

```bash
git clone https://github.com/hongphuc5497/skills.git
cd skills && bash install.sh
```

### Remote install (no clone)

Interactive TUI:

```bash
curl -sSL https://raw.githubusercontent.com/hongphuc5497/skills/main/remote-install.sh | bash
```

Non-interactive:

```bash
curl -sSL https://raw.githubusercontent.com/hongphuc5497/skills/main/remote-install.sh | bash -s -- \
  --skills "code-review,auto-push" --tools "Claude Code" --scope global
```

---

## Catalog

### 🔧 General Skills

Standalone, well-tested skills for common development workflows.

<!-- TOC:START:GENERAL -->
| Skill | What it does |
|---|---|
| [**auto-push**](skills/auto-push/) | Generate a commit message, stage all changes, and push to remote after scanning for secrets, large files, and protect... |
| [**brand-name-checker**](skills/brand-name-checker/) | Check product and brand names for conflicts across trademarks, domains, social handles, and package registries. Retur... |
| [**cavecrew**](skills/cavecrew/) | Decision guide for delegating to caveman-style subagents. Tells the main thread WHEN to spawn `cavecrew-investigator`... |
| [**caveman**](skills/caveman/) | Ultra-compressed communication mode. Cuts token usage ~75% by speaking like caveman while keeping full technical accu... |
| [**caveman-commit**](skills/caveman-commit/) | Ultra-compressed commit message generator. Cuts noise from commit messages while preserving intent and reasoning. Con... |
| [**caveman-compress**](skills/caveman-compress/) | Compress natural language memory files (CLAUDE.md, todos, preferences) into caveman format to save input tokens. Pres... |
| [**caveman-help**](skills/caveman-help/) | Quick-reference card for all caveman modes, skills, and commands. One-shot display, not a persistent mode. Trigger: /... |
| [**caveman-review**](skills/caveman-review/) | Ultra-compressed code review comments. Cuts noise from PR feedback while preserving the actionable signal. Each comme... |
| [**caveman-stats**](skills/caveman-stats/) | Show real token usage and estimated savings for the current session. Reads directly from the Claude Code session log ... |
| [**code-optimizer**](skills/code-optimizer/) | Analyze code for performance bottlenecks, memory leaks, and algorithmic inefficiencies. Use when asked to optimize, f... |
| [**code-review**](skills/code-review/) | Review code changes for bugs, security vulnerabilities, and code quality issues — producing prioritized findings with... |
| [**context-hub**](skills/context-hub/) | Fetch current API/SDK docs before writing integration code. Use whenever writing code that integrates with an externa... |
| [**docs-generator**](skills/docs-generator/) | Generate and restructure project documentation into a clear, accessible hierarchy. Use when asked to organize docs, g... |
| [**grill-me**](skills/grill-me/) | A relentless interview to sharpen a plan or design. |
| [**grilling**](skills/grilling/) | Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building... |
| [**handoff**](skills/handoff/) | Compact the current conversation into a handoff document for another agent to pick up. |
| [**idea-validator**](skills/idea-validator/) | Validate app/startup ideas with market, feasibility, commercial, and open-source competitor analysis. Use when asked ... |
| [**oss-ready**](skills/oss-ready/) | Transform a project into a professional open-source repository by adding LICENSE, README, CONTRIBUTING, CODE_OF_CONDU... |
| [**prd-generator**](skills/prd-generator/) | Generate Product Requirements Documents from `idea.md` and `validate.md` files. Use when asked to create or update a ... |
| [**quick-healthy-recipes**](skills/quick-healthy-recipes/) | Generate exactly 3 simple, fast, healthy recipes from food photos, ingredient lists, or cravings. Use for what-to-coo... |
| [**release-manager**](skills/release-manager/) | Manage software releases end-to-end: bump version, generate changelog, tag, push, GitHub release, publish to PyPI/npm... |
| [**security-setup**](skills/security-setup/) | Install local-first security hardening: pre-commit secret detection, offline dependency scans, static analysis, repor... |
| [**seo-ai-optimizer**](skills/seo-ai-optimizer/) | Audit and optimize websites for technical SEO, content SEO, and AI bot accessibility. Fixes meta tags, sitemaps, robo... |
| [**tasks-generator**](skills/tasks-generator/) | Generate development tasks from a PRD file with sprint-based planning. Use when users ask to create tasks from PRD, b... |
| [**teach**](skills/teach/) | Teach the user a new skill or concept, within this workspace. |
| [**usability-review**](skills/usability-review/) | Review UI for usability issues using Steve Krug's principles and produce a scannable report. Use when asked for a usa... |
| [**writing-great-skills**](skills/writing-great-skills/) | Reference for writing and editing skills well — the vocabulary and principles that make a skill predictable. |
<!-- TOC:END:GENERAL -->

### 🔧 Tailored Skills (hongphuc5497)

Personal skills built for my specific stack and workflows.

<!-- TOC:START:TAILORED -->
| Skill | What it does |
|---|---|
| [**hermes-config**](skills/hermes-config/) | Configure Hermes Agent — providers, models, tools, skills, voice, gateway, plugins. Uses hermes CLI commands. Not for... |
| [**multi-agent-orchestrator**](skills/multi-agent-orchestrator/) | Orchestrate work across multiple AI coding agents (Hermes, Codex, Claude Code) — delegate tasks in parallel, merge re... |
| [**rtk**](skills/rtk/) | RTK (Rust Token Killer) — CLI proxy that compresses noisy shell output by 60-90%. Use when piping commands through rt... |
<!-- TOC:END:TAILORED -->

<details>
<summary><b>Supported Tool Paths</b></summary>

| Tool | Global path | Project path |
|---|---|---|
| **Claude Code** | `~/.claude/skills/<skill>/` | `.claude/skills/<skill>/` |
| **Cursor** | `~/.agents/skills/<skill>/` + `.cursor/rules/<skill>.mdc` | same, relative |
| **Windsurf** | `~/.agents/skills/<skill>/` + `.windsurf/rules/<skill>.md` | same, relative |
| **GitHub Copilot** | `~/.agents/skills/<skill>/` + `.github/instructions/<skill>.instructions.md` | same, relative |
| **OpenAI Codex** | `~/.agents/skills/<skill>/` + `~/.codex/AGENTS.md` | same, relative |
| **OpenCode** | `~/.agents/skills/<skill>/` | same, relative |

</details>

<details>
<summary><b>Project Structure</b></summary>

```
./
├── skills/              # Skill source files
│   ├── code-review/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── auto-push/
│   └── prd-generator/
│       ├── SKILL.md
│       └── references/
├── assets/              # Logo, images
├── install.sh           # Local installer (TUI)
├── remote-install.sh    # Remote installer (curl-pipe)
├── CLAUDE.md            # Agent context for this repo
├── AGENTS.md            # Subagent definitions
├── CONTRIBUTING.md      # How to contribute
├── CHANGELOG.md         # Version history
└── LICENSE              # MIT
```

</details>

---

## FAQ

**Do I need all the skills?** No. Each skill is independent. Install only what you need.

**Can I create my own skills?** Yes. Follow the [Contributing Guide](CONTRIBUTING.md).

**Why create your own?** Tailored skills encode specific toolchains, API conventions, and failure modes battle-tested on actual hardware. General skills cover common development workflows.

---

[**View all skills**](./skills) | [**Contribute**](CONTRIBUTING.md) | MIT Licensed

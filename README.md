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

[**Browse the catalog**](#catalog) | [**Install**](#install)

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

### 🎯 Curated from luongnv89/skills

Community-vetted skills ported from [luongnv89/skills](https://github.com/luongnv89/skills) (MIT). These are standalone, well-tested skills for common workflows.

| Skill | Effort | What it does |
|---|---|---|
| [**code-review**](skills/code-review/) | medium | Reviews based on Code Smells + The Pragmatic Programmer. Structured reports by severity |
| [**auto-push**](skills/auto-push/) | low | Stage, commit, push with secret and large-file detection |
| [**code-optimizer**](skills/code-optimizer/) | medium | Finds bottlenecks, memory leaks, caching gaps, concurrency issues |
| [**usability-review**](skills/usability-review/) | medium | Usability reviews using Krug's principles with visual scorecards |
| [**docs-generator**](skills/docs-generator/) | low | Restructure scattered docs into a coherent hierarchy |
| [**seo-ai-optimizer**](skills/seo-ai-optimizer/) | high | Technical SEO, structured data, and AI bot accessibility |
| [**oss-ready**](skills/oss-ready/) | low | LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, GitHub templates |
| [**security-setup**](skills/security-setup/) | high | Local-first security hardening with pre-commit hooks, offline scanners |
| [**idea-validator**](skills/idea-validator/) | max | Feasibility and market viability feedback before you build |
| [**brand-name-checker**](skills/brand-name-checker/) | max | Trademark, domain, social, npm, PyPI, Homebrew — one pass |
| [**prd-generator**](skills/prd-generator/) | max | Structured PRDs from a description or validated idea |
| [**tasks-generator**](skills/tasks-generator/) | max | Sprint-ready task breakdowns from your PRD |
| [**release-manager**](skills/release-manager/) | max | Version bump, changelog, tags, GitHub release, PyPI/npm publish |
| [**context-hub**](skills/context-hub/) | low | Fetch current API/SDK docs before writing integration code |
| [**quick-healthy-recipes**](skills/quick-healthy-recipes/) | medium | Three simple, fast, healthy recipes from food photos or ingredients |

### 🔧 Tailored Skills (hongphuc5497)

Personal skills built for my specific stack and workflows.

| Skill | Effort | What it does |
|---|---|---|
| [**nextjs-16-tailwind**](skills/nextjs-16-tailwind/) | high | Build Next.js 16 + Tailwind CSS 4 pages following App Router patterns and Tailwind 4 v4 API conventions |
| [**github-trending-digest**](skills/github-trending-digest/) | medium | Automate GitHub Trending digest — fetch, summarize, publish to Substack |
| [**fine-tuning-gemma**](skills/fine-tuning-gemma/) | max | Fine-tune Gemma models via Unsloth on macOS — dataset prep, training, evaluation |
| [**wiki-rag-pipeline**](skills/wiki-rag-pipeline/) | high | RAG pipeline for Obsidian wiki — QMD semantic search, score fallback, context assembly |
| [**personal-landing-page**](skills/personal-landing-page/) | high | Update and deploy the personal landing page on Vercel + Route 53 |
| [**multi-agent-orchestrator**](skills/multi-agent-orchestrator/) | max | Delegate tasks across Hermes, Codex, and Claude Code agents in parallel |
| [**hermes-config**](skills/hermes-config/) | medium | Configure Hermes Agent — providers, models, tools, skills, voice |
| [**caveman-commit**](skills/caveman-commit/) | low | Ultra-compressed commit messages. Cuts noise from PR descriptions |

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
│   ├── code-review/     # Curated from luongnv89
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── auto-push/       # Curated from luongnv89
│   └── nextjs-16-tailwind/  # Tailored skills
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

**How is this different from luongnv89/skills?** This repo curates the best community skills from luongnv89 and adds personal workflow automations specific to my stack (Next.js 16, Tailwind 4, Hermes Agent, fine-tuning, multi-agent workflows).

**Why create your own?** My tailored skills encode specific toolchains, API conventions, and failure modes I've hit. They're battle-tested on my actual machine.

---

[**View all skills**](./skills) | [**Contribute**](CONTRIBUTING.md) | MIT Licensed

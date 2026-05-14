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

### 🔧 General Skills

Standalone, well-tested skills for common development workflows.

| Skill | What it does |
|---|---|
| [**code-review**](skills/code-review/) | Reviews based on Code Smells + The Pragmatic Programmer. Structured reports by severity |
| [**auto-push**](skills/auto-push/) | Stage, commit, push with secret and large-file detection |
| [**code-optimizer**](skills/code-optimizer/) | Finds bottlenecks, memory leaks, caching gaps, concurrency issues |
| [**usability-review**](skills/usability-review/) | Usability reviews using Krug's principles with visual scorecards |
| [**docs-generator**](skills/docs-generator/) | Restructure scattered docs into a coherent hierarchy |
| [**seo-ai-optimizer**](skills/seo-ai-optimizer/) | Technical SEO, structured data, and AI bot accessibility |
| [**oss-ready**](skills/oss-ready/) | LICENSE, CONTRIBUTING, CODE_OF_CONDUCT, GitHub templates |
| [**security-setup**](skills/security-setup/) | Local-first security hardening with pre-commit hooks, offline scanners |
| [**idea-validator**](skills/idea-validator/) | Feasibility and market viability feedback before you build |
| [**brand-name-checker**](skills/brand-name-checker/) | Trademark, domain, social, npm, PyPI, Homebrew — one pass |
| [**prd-generator**](skills/prd-generator/) | Structured PRDs from a description or validated idea |
| [**tasks-generator**](skills/tasks-generator/) | Sprint-ready task breakdowns from your PRD |
| [**release-manager**](skills/release-manager/) | Version bump, changelog, tags, GitHub release, PyPI/npm publish |
| [**context-hub**](skills/context-hub/) | Fetch current API/SDK docs before writing integration code |
| [**quick-healthy-recipes**](skills/quick-healthy-recipes/) | Three simple, fast, healthy recipes from food photos or ingredients |

### 🔧 Tailored Skills (hongphuc5497)

Personal skills built for my specific stack and workflows.

| Skill | What it does |
|---|---|
| [**nextjs-16-tailwind**](skills/nextjs-16-tailwind/) | Build Next.js 16 + Tailwind CSS 4 pages following App Router patterns and Tailwind 4 v4 API conventions |
| [**github-trending-digest**](skills/github-trending-digest/) | Automate GitHub Trending digest — fetch, summarize, publish to Substack |
| [**fine-tuning-gemma**](skills/fine-tuning-gemma/) | Fine-tune Gemma models via Unsloth on macOS — dataset prep, training, evaluation |
| [**wiki-rag-pipeline**](skills/wiki-rag-pipeline/) | RAG pipeline for Obsidian wiki — QMD semantic search, score fallback, context assembly |
| [**personal-landing-page**](skills/personal-landing-page/) | Update and deploy the personal landing page on Vercel + Route 53 |
| [**multi-agent-orchestrator**](skills/multi-agent-orchestrator/) | Delegate tasks across Hermes, Codex, and Claude Code agents in parallel |
| [**hermes-config**](skills/hermes-config/) | Configure Hermes Agent — providers, models, tools, skills, voice |
| [**caveman-commit**](skills/caveman-commit/) | Ultra-compressed commit messages. Cuts noise from PR descriptions |

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
│   └── nextjs-16-tailwind/
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

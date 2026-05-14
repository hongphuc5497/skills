---
name: personal-landing-page
description: "Update and deploy the personal landing page at hongphuc5497.com — Next.js 16 + Tailwind 4 on Vercel + Route 53."
license: MIT
metadata:
  version: 1.0.0
  author: hongphuc5497
---

# Personal Landing Page

Manage the personal landing page at hongphuc5497.com.

## When to Use

Use when updating, deploying, or troubleshooting the personal landing page. Trigger on phrases like "update the landing page", "deploy the site", "fix the domain", "add a project to the page".

## Project Location

```bash
~/playground/personal-landing-page/
```

## Stack

- Next.js 16 App Router + TypeScript
- Tailwind CSS 4 (CSS-first, no config file)
- Framer Motion for animations
- shadcn-style local UI primitives
- Markdown notes with RSS
- Vercel for hosting + AWS Route 53 for DNS

## Current State

- **Domain**: hongphuc5497.com (apex + www)
- **Vercel URL**: personal-landing-page-virid-psi.vercel.app
- **Vercel project**: personal-landing-page
- **DNS**: Route 53, records set
- **Alias**: Vercel alias blocked — `vcp_` token lacks domain scope, needs dashboard fix

## Instructions

### Add Content

1. Edit identity/links in `src/data/profile.ts`
2. Add blog posts as markdown in `content/notes/`
3. Add project cards via data/profile.ts

### Development

```bash
cd ~/playground/personal-landing-page/
pnpm dev          # local dev at localhost:3000
pnpm lint         # lint check
pnpm typecheck    # TypeScript check
pnpm build        # full build
pnpm check        # all gates (lint + typecheck + test + build)
```

### Deploy

```bash
pnpm deploy:production
```

### Domain Setup

- Domain: hongphuc5497.com
- WWW: www.hongphuc5497.com
- Vercel project: personal-landing-page
- Route 53 hosted zone exists, A records and CNAME set
- **Blocked**: Vercel alias needs dashboard token scope fix

## Troubleshooting

- **Deploy fails**: Check `pnpm check` first
- **Domain not resolving**: Check Route 53 records and Vercel alias status
- **Vercel auth**: May need `vercel login`

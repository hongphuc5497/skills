---
name: nextjs-16-tailwind
description: "Build Next.js 16 + Tailwind CSS 4 pages following App Router patterns and Tailwind CSS v4 API conventions. Use for creating new pages, components, or layouts. Not for general React work without Next.js."
license: MIT
metadata:
  version: 1.0.0
  category: tailored
  author: hongphuc5497
---

# Next.js 16 + Tailwind CSS 4

Build pages with Next.js 16 App Router and Tailwind CSS 4.

## When to Use

Use when the user asks to create, modify, or style a Next.js page/component using Tailwind. Trigger on phrases like "create a page", "add a component", "style this with Tailwind", "build a layout". Skip for general React apps without Next.js or projects using raw CSS.

## Critical Differences From Your Training Data

**This is NOT the Next.js you know.** Read AGENTS.md or relevant guide in `node_modules/next/dist/docs/` before writing code.

### Tailwind CSS 4 Key Changes

1. **No `tailwind.config.js`** — Configuration uses CSS-first approach via `@theme` directive:
   ```css
   @import "tailwindcss";
   @theme {
     --color-primary: #3b82f6;
     --font-heading: "Inter", sans-serif;
   }
   ```

2. **New CSS-first configuration** — Use `@theme` for design tokens, `@utility` for custom utilities, `@variant` for custom variants:
   ```css
   @utility container-main {
     max-width: 1200px;
     margin-inline: auto;
   }
   @variant dark (&:where(.dark, .dark *));
   ```

3. **`@apply` still works** but is not preferred — use components or `@utility` instead

4. **No `darkMode: "class"`** — Dark mode is class-based by default in v4

5. **Imports via `@import "tailwindcss"`** (not `@tailwind base/components/utilities`)

### Next.js 16 Key Changes

- Server Components by default in App Router
- `'use client'` directive only when you need interactivity (state, effects, event handlers)
- Layouts: `layout.tsx` wraps child pages, persists across navigations
- Loading states: `loading.tsx` for Suspense fallback
- Error handling: `error.tsx` + `global-error.tsx`
- Metadata API via `export const metadata = {}` or `generateMetadata()`

## Quick Start

```tsx
// app/page.tsx — Server Component
export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-4xl font-bold">Hello World</h1>
    </main>
  );
}
```

## Instructions

1. Check the project uses Next.js 16 + Tailwind CSS 4 (verify `package.json` and `node_modules/next/dist/docs/` or AGENTS.md)
2. Read relevant guide in `node_modules/next/dist/docs/` before implementation
3. Use Server Components by default, add `'use client'` only for interactivity
4. Use CSS-first Tailwind v4 patterns (`@theme`, `@utility`, `@variant`)
5. Place reusable UI patterns in `src/components/` as local shadcn-style primitives
6. Use `<Image>` from `next/image` for optimized images
7. Verify with `pnpm typecheck` and `pnpm lint`

## References

- [Next.js 16 Docs](https://nextjs.org/docs) (but check local `/docs` first)
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs)
- Project: `~/playground/personal-landing-page/`

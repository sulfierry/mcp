---
name: modern-frontend-frameworks
description: "Modern frontend beyond React: Astro (content-first, islands), SvelteKit 5 (runes), SolidJS (fine-grained reactivity), Qwik (resumability, zero-hydration), htmx (HTML-over-the-wire), React Server Components (RSC). Triggers on Astro, Svelte, SvelteKit, runes, SolidJS, Qwik, resumability, htmx, server components, RSC."
category: frontend
tags: [astro, svelte, sveltekit, solidjs, qwik, htmx, rsc]
---

# Modern Frontend (beyond React)

## Framework matrix

| Framework | Philosophy | Bundle / First load |
|-----------|------------|---------------------|
| **Astro 4+** | Content-first; islands of JS | Near-zero JS for static pages |
| **SvelteKit 5** | Compile-time framework; runes reactivity | Small bundles, compiled |
| **SolidJS** | React-like syntax, fine-grained reactivity | Tiny, no VDOM |
| **Qwik** | Resumability (no hydration) | Instant TTI |
| **htmx** | HTML attributes drive AJAX | <15 KB, server-rendered HTML |
| **React + RSC** | Server components + islands | Reduced client bundle |

## Astro
```bash
npm create astro@latest
```
```astro
---
// src/pages/index.astro — zero JS shipped by default
import Card from '../components/Card.svelte';
const posts = await fetchPosts();
---
<h1>Blog</h1>
{posts.map(p => <Card client:visible post={p} />)}
```
- Islands architecture: `client:load` / `client:idle` / `client:visible`
- Works with React, Vue, Svelte, Solid, Preact components
- Ideal for blogs, docs, marketing, e-commerce PLP

## SvelteKit 5 (runes)
```svelte
<script>
  let count = $state(0);           // rune: reactive state
  let doubled = $derived(count * 2);
  $effect(() => console.log(count));
</script>
<button onclick={() => count++}>{count}</button>
```
- `$state`, `$derived`, `$effect`, `$props`, `$bindable` runes
- No more `$:` labels or stores for most cases
- Load functions (`+page.server.ts`) for SSR data
- Form actions for progressive enhancement

## SolidJS
```jsx
import { createSignal, createMemo } from "solid-js";
function Counter() {
  const [count, setCount] = createSignal(0);
  const doubled = createMemo(() => count() * 2);
  return <button onClick={() => setCount(count() + 1)}>{count()}</button>;
}
```
- Signals (no VDOM, no diffing)
- Tracks at fine granularity — only changed bits re-render
- Smallest runtime among React-likes
- SolidStart for SSR framework

## Qwik
```tsx
import { component$, useSignal } from "@builder.io/qwik";
export default component$(() => {
  const count = useSignal(0);
  return <button onClick$={() => count.value++}>{count.value}</button>;
});
```
- **Resumability**: serialize app state in HTML, resume on client without hydration
- `$` marks lazy-loaded boundaries
- Zero JS until interaction
- Qwik City = framework (routing, SSR)

## htmx (anti-SPA)
```html
<button hx-get="/click" hx-target="#result" hx-swap="outerHTML">Click</button>
<div id="result"></div>
```
- Server returns HTML fragments
- No client state management
- Pairs with any backend (Go, Rails, Django, Phoenix)
- Use with Alpine.js for small client-side needs

## React Server Components (RSC)
- Next.js App Router default
- `async` components run on server; cannot use hooks / state
- Client components must have `"use client"` directive
- Server actions for mutations (progressive forms)
```tsx
// app/page.tsx (server component)
export default async function Page() {
  const data = await fetch("...");
  return <ClientInteractive data={await data.json()} />;
}
```

## Pick by scenario

| Scenario | Pick |
|----------|------|
| Content site, blog, docs | Astro |
| App with forms + progressive enhancement | SvelteKit or Rails/Phoenix + htmx |
| Dashboard with lots of reactivity | SolidJS or Svelte |
| Instant TTI critical (e-commerce) | Qwik |
| Existing React team + backend-heavy UI | Next.js + RSC |
| Minimal JS preferred, server-rendered | htmx |
| Mobile-first, max-perf | Solid or Qwik |

## References
- docs.astro.build
- svelte.dev (runes docs)
- docs.solidjs.com
- qwik.dev
- htmx.org
- react.dev (Server Components)

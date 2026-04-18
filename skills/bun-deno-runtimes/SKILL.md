---
name: bun-deno-runtimes
description: "Modern JavaScript/TypeScript runtimes: Bun (Zig, fast), Deno (Rust, secure-by-default). Replace Node for scripts, servers, bundling, package management, test running. Triggers on Bun, Deno, modern JS runtime, Node alternative, TypeScript execution, JavaScript runtime."
category: langs
tags: [bun, deno, javascript, typescript, runtime]
---

# Bun & Deno

## Bun (oven.sh)
Single binary: runtime + package manager + bundler + test runner + transpiler.

### Install
```bash
curl -fsSL https://bun.sh/install | bash
```

### Usage
```bash
bun run script.ts          # run TS directly, no tsc
bun install                # 20× faster than npm install
bun add express            # install
bun test                   # Jest-compatible tests
bun build ./src/index.ts   # bundle
bun --hot server.ts        # dev server with hot reload
```

### APIs
```typescript
// Bun-native HTTP (100k req/s)
Bun.serve({
  port: 3000,
  fetch(req) { return new Response("ok"); }
});

// Bun.file for fast IO
const f = Bun.file("./data.json");
const json = await f.json();

// SQLite built-in
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
```

Node-compatible (`node:` imports work). Some native modules fail — check bun.sh/docs/nodejs-apis.

## Deno (deno.com)
Rust-based, security-by-default runtime. Built-in TS support, formatter, linter, test runner.

### Install
```bash
curl -fsSL https://deno.land/install.sh | sh
```

### Security
```bash
deno run script.ts                      # no permissions
deno run --allow-net --allow-read script.ts   # explicit perms
```

### Usage
```bash
deno run -A server.ts                   # -A = all permissions
deno test                               # built-in test runner
deno fmt                                # format
deno lint                               # lint
deno compile --output app script.ts     # single binary
```

### Deno KV (key-value store)
```typescript
const kv = await Deno.openKv();
await kv.set(["users", "alice"], { age: 30 });
const { value } = await kv.get(["users", "alice"]);
```

## Bun vs Deno vs Node

| Feature | Bun | Deno | Node |
|---------|-----|------|------|
| TS native | ✅ | ✅ | needs tsx/ts-node |
| Package install speed | fastest | good (JSR + npm) | baseline |
| Security model | none | allow-list | none |
| Built-in bundler | ✅ | `deno bundle` (deprecated, use esbuild) | ❌ |
| Built-in test | ✅ | ✅ | `node --test` (basic) |
| Compile to binary | limited | `deno compile` | single-binary via pkg |
| NPM compat | ~95% | `npm:` specifier | 100% |
| Ecosystem size | npm | npm + JSR | npm (gold standard) |

## Pick by scenario

| Task | Tool |
|------|------|
| Max perf server / script | Bun |
| Secure sandbox script execution | Deno |
| Single-binary deploy | Deno (`deno compile`) |
| Compatibility with existing Node infra | Node |
| Fast npm install CI | Bun |
| Type-checked-everywhere team | Deno or Bun |

## References
- bun.sh/docs
- docs.deno.com

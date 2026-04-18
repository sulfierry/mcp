---
name: zig-systems
description: "Zig systems language: comptime, allocators, build system (zig build), cross-compilation, C/C++ interop, error handling, no hidden control flow. Replacement for C in systems code. Bun/Ghostty/TigerBeetle/tree-sitter wrappers use Zig. Triggers on Zig, ziglang, comptime, zig build, systems programming, C alternative."
category: langs
tags: [zig, systems, cross-compile, c-interop]
---

# Zig

## Why
Systems language with explicit allocators, `comptime` metaprogramming, no macros, no preprocessor, no hidden control flow. Seamless C interop. Built-in cross-compilation (`zig build -Dtarget=x86_64-linux-musl`).

## Install
```bash
brew install zig          # macOS
# or download from ziglang.org
zig version               # 0.13.x stable as of 2025
```

## Hello world + build
```zig
// src/main.zig
const std = @import("std");
pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}!\n", .{"world"});
}
```
```bash
zig init-exe             # scaffolds build.zig
zig build run
zig build -Doptimize=ReleaseFast
zig build -Dtarget=aarch64-macos    # cross-compile
```

## Core features

### comptime
```zig
fn max(comptime T: type, a: T, b: T) T { return if (a > b) a else b; }
const m = max(i32, 3, 7);   // specialized at compile time
```

### Allocators explicit
```zig
var gpa = std.heap.GeneralPurposeAllocator(.{}){};
const alloc = gpa.allocator();
const buf = try alloc.alloc(u8, 1024);
defer alloc.free(buf);
```

### Error unions
```zig
fn parse(s: []const u8) !u32 { ... }
const n = parse("42") catch |err| { std.debug.print("{}", .{err}); return; };
```

## C interop
```zig
const c = @cImport(@cInclude("stdio.h"));
pub fn main() void { _ = c.printf("from C\n"); }
```

Use Zig as a C/C++ compiler: `zig cc`, `zig c++` — drop-in for gcc/clang with cross-compile superpowers.

## Notable Zig projects
- **Bun** — fast JS runtime (uses Zig)
- **Ghostty** — terminal (Mitchell Hashimoto)
- **TigerBeetle** — financial DB
- **tree-sitter** Zig bindings
- **Roc** language compiler

## When Zig over Rust / C
- C-level simplicity + modern ergonomics (vs Rust's steep curve)
- Explicit control over allocations (vs Rust's borrow checker)
- Cross-compile out of the box
- Drop-in C replacement without memory-safety enforcement

## When NOT Zig
- Need memory-safety guarantees → Rust
- Large existing ecosystem → Go/Rust
- Async: Zig's async was removed in 0.11; being redesigned

## References
- ziglang.org/documentation
- Ziglearn.org

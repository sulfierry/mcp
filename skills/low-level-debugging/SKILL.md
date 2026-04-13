---
name: Low-Level Debugging
description: "Systems-level debugging mastery. GDB/LLDB, Valgrind, AddressSanitizer, perf, strace/dtrace, core dump analysis, and hardware watchpoints."
category: low-level
tags: debugging, gdb, lldb, valgrind, asan, perf, strace, dtrace, core-dump
---

# Low-Level Debugging

Expert in systems-level debugging — finding and fixing bugs that crash, corrupt, leak, or stall at the C/C++ level.

## Use this skill when

- Debugging segfaults, use-after-free, buffer overflows, or memory corruption
- Analyzing core dumps from production crashes
- Profiling CPU, memory, cache, or I/O bottlenecks with `perf`
- Tracing syscalls with `strace`/`dtrace`
- Detecting memory leaks with Valgrind or sanitizers
- Using hardware breakpoints and watchpoints
- Debugging multithreaded race conditions

## Tool Selection Matrix

| Problem | Primary Tool | Secondary |
|---|---|---|
| **Segfault / crash** | GDB + core dump | ASAN |
| **Memory leak** | Valgrind `--leak-check=full` | LSAN |
| **Buffer overflow** | AddressSanitizer (ASAN) | Valgrind |
| **Use-after-free** | ASAN | GDB watchpoint |
| **Data race** | ThreadSanitizer (TSAN) | Helgrind |
| **Undefined behavior** | UBSan | GDB |
| **Performance** | `perf stat` / `perf record` | Instruments (macOS) |
| **Syscall tracing** | `strace` (Linux) / `dtruss` (macOS) | `ltrace` |
| **Memory profiling** | `perf mem` / Massif | heaptrack |
| **Cache misses** | `perf stat -e cache-misses` | Cachegrind |

## GDB Essentials

### Core Dump Analysis

```bash
# Enable core dumps
ulimit -c unlimited
echo '/tmp/core.%e.%p' | sudo tee /proc/sys/kernel/core_pattern

# Run and crash
./my_program

# Analyze core dump
gdb ./my_program /tmp/core.my_program.12345
(gdb) bt              # Full backtrace
(gdb) bt full          # With local variables
(gdb) frame 3          # Switch to frame #3
(gdb) info locals      # Print all locals in current frame
(gdb) info registers   # CPU register state at crash
(gdb) x/16xw $sp      # Examine 16 words at stack pointer
```

### Advanced GDB Commands

```gdb
# Hardware watchpoint — break when memory changes
(gdb) watch *(int *)0x7fffe8    # Break when this address is written
(gdb) rwatch my_var             # Break on read of my_var
(gdb) awatch my_var             # Break on read OR write

# Conditional breakpoints
(gdb) break my_func if count > 100
(gdb) break file.c:42 if strcmp(name, "target") == 0

# Reverse debugging (record and replay)
(gdb) record                    # Start recording
(gdb) reverse-continue          # Run backwards to previous breakpoint
(gdb) reverse-step              # Step backwards

# Print complex structures
(gdb) set print pretty on
(gdb) set print array on
(gdb) ptype struct my_struct    # Show struct layout
(gdb) p/x *(struct header *)ptr # Cast and print hex

# Catch events
(gdb) catch syscall write       # Break on write() syscall
(gdb) catch signal SIGSEGV      # Break on segfault
(gdb) catch throw               # Break on C++ exception throw

# Multi-thread debugging
(gdb) info threads              # List all threads
(gdb) thread 3                  # Switch to thread 3
(gdb) set scheduler-locking on  # Only run current thread
(gdb) thread apply all bt       # Backtrace ALL threads
```

### GDB Python Scripting

```python
# ~/.gdbinit or inline
import gdb

class PrintListCommand(gdb.Command):
    """Walk a linked list and print elements."""
    def __init__(self):
        super().__init__("plist", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        node = gdb.parse_and_eval(arg)
        i = 0
        while node != 0:
            print(f"[{i}] data={node['data']}")
            node = node['next']
            i += 1

PrintListCommand()
```

## Sanitizers (Compile-Time Instrumentation)

```bash
# AddressSanitizer — heap/stack buffer overflow, use-after-free, double-free
gcc -fsanitize=address -fno-omit-frame-pointer -g -O1 prog.c -o prog
ASAN_OPTIONS=detect_leaks=1:halt_on_error=0 ./prog

# ThreadSanitizer — data races
gcc -fsanitize=thread -g -O1 prog.c -o prog -lpthread

# UndefinedBehaviorSanitizer — signed overflow, null deref, alignment
gcc -fsanitize=undefined -g prog.c -o prog

# MemorySanitizer (clang only) — uninitialized reads
clang -fsanitize=memory -fno-omit-frame-pointer -g prog.c -o prog

# Combine sanitizers (ASAN + UBSan)
gcc -fsanitize=address,undefined -g -O1 prog.c -o prog
```

## Valgrind

```bash
# Memory leak check
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./prog

# Helgrind — thread error detector
valgrind --tool=helgrind ./prog

# Cachegrind — cache profiling
valgrind --tool=cachegrind ./prog
cg_annotate cachegrind.out.<pid>

# Massif — heap profiler
valgrind --tool=massif --pages-as-heap=yes ./prog
ms_print massif.out.<pid>

# Callgrind — call graph profiler
valgrind --tool=callgrind --callgrind-out-file=callgrind.out ./prog
kcachegrind callgrind.out  # Visualize
```

## perf (Linux Performance Counters)

```bash
# Overview: CPU cycles, instructions, cache misses, branch misses
perf stat ./prog

# Record + flamegraph
perf record -g --call-graph dwarf ./prog
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg

# Specific events
perf stat -e cache-misses,cache-references,instructions,cycles ./prog

# Live top-like view
perf top -p $(pidof my_daemon)

# Memory access profiling
perf mem record ./prog
perf mem report

# Trace scheduling events
perf sched record ./prog
perf sched latency
```

## strace / dtrace

```bash
# Trace all syscalls
strace -f -tt -T ./prog          # -f=follow forks, -tt=timestamps, -T=time in syscall

# Only file operations
strace -e trace=file ./prog

# Only network
strace -e trace=network ./prog

# Count syscalls (summary)
strace -c ./prog

# Attach to running process
strace -p <PID> -e trace=write

# macOS equivalent
dtruss -f ./prog 2>&1 | head -100
```

## Debugging Patterns

### Pattern: Finding Memory Corruption Source

```
1. Reproduce with ASAN → get exact stack trace of invalid access
2. If ASAN can't find it → use GDB hardware watchpoint on corrupted address
3. If intermittent → use rr (record-replay debugger):
   rr record ./prog
   rr replay
   (rr) watch -l *(int *)0x...  # reverse-continue to find writer
```

### Pattern: Diagnosing a Hang

```
1. Attach GDB to running process: gdb -p <PID>
2. (gdb) thread apply all bt   → see where all threads are stuck
3. Look for: mutex deadlock, infinite loop, blocked syscall
4. For deadlocks: (gdb) info mutex (with glibc debug)
5. For syscall blocks: strace -p <PID> → see which syscall is blocking
```

### Pattern: Production Crash Analysis

```
1. Collect: core dump + binary + debug symbols (.debug or -dbg package)
2. gdb ./binary core
3. (gdb) bt → identify crash function
4. (gdb) frame N → inspect local variables
5. (gdb) info registers → check for NULL/corrupt pointers
6. (gdb) disassemble → verify instruction at crash matches source
7. Cross-reference with ASAN build in staging environment
```

## Anti-Patterns

- ❌ Adding `printf` everywhere instead of using GDB
- ❌ Running Valgrind in production (10-50x slowdown)
- ❌ Ignoring Valgrind "Conditional jump depends on uninitialised value"
- ❌ Disabling ASAN in CI "because it's too slow"
- ❌ Not preserving core dumps from production crashes
- ❌ Debugging optimized code without `-fno-omit-frame-pointer`
- ❌ Using `sleep()` to "fix" race conditions

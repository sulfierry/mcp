---
name: C Systems Programming
description: "POSIX systems programming in C. Syscalls, IPC, signals, file descriptors, process management, and portable Unix programming."
category: low-level
tags: c, posix, syscalls, ipc, signals, unix, systems-programming
---

# C Systems Programming

Expert in POSIX systems programming — the foundation layer between user-space applications and the kernel.

## Use this skill when

- Writing POSIX-compliant C code for Unix/Linux/macOS
- Implementing IPC (pipes, FIFOs, shared memory, message queues, Unix sockets)
- Handling signals (`sigaction`, signal masks, async-signal-safe functions)
- Managing processes (`fork`, `exec`, `waitpid`, process groups, sessions)
- Working with file descriptors, `epoll`/`kqueue`/`poll`, non-blocking I/O
- Implementing daemons, service processes, or CLI tools in C
- Porting code between POSIX platforms

## Core Principles

### 1. Defense Against Undefined Behavior

Every syscall can fail. Every pointer can be NULL. Every buffer has a size.

```c
// ❌ WRONG: Ignoring return values
read(fd, buf, sizeof(buf));

// ✅ CORRECT: Handle every error path
ssize_t n = read(fd, buf, sizeof(buf));
if (n < 0) {
    if (errno == EINTR) goto retry;  // interrupted by signal
    perror("read");
    return -1;
}
if (n == 0) {
    // EOF — peer closed connection
}
```

### 2. Signal Safety

Only use async-signal-safe functions inside signal handlers. Use `sig_atomic_t` for flags.

```c
static volatile sig_atomic_t got_sigterm = 0;

static void handle_sigterm(int signo) {
    (void)signo;
    got_sigterm = 1;  // ONLY set a flag — never call printf, malloc, etc.
}

// Setup with sigaction (NEVER signal())
struct sigaction sa = {
    .sa_handler = handle_sigterm,
    .sa_flags = SA_RESTART,
};
sigemptyset(&sa.sa_mask);
sigaction(SIGTERM, &sa, NULL);
```

### 3. Resource Lifecycle (RAII in C)

Use cleanup patterns: `goto cleanup`, `__attribute__((cleanup))`, or wrapper structs.

```c
int process_file(const char *path) {
    int ret = -1;
    int fd = -1;
    void *map = MAP_FAILED;

    fd = open(path, O_RDONLY);
    if (fd < 0) goto cleanup;

    struct stat st;
    if (fstat(fd, &st) < 0) goto cleanup;

    map = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (map == MAP_FAILED) goto cleanup;

    // ... process mapped data ...
    ret = 0;

cleanup:
    if (map != MAP_FAILED) munmap(map, st.st_size);
    if (fd >= 0) close(fd);
    return ret;
}
```

### 4. IPC Decision Matrix

| Mechanism | Use When | Pros | Cons |
|---|---|---|---|
| **pipe** | Parent↔child, simple streaming | Zero setup | Unidirectional, related processes only |
| **FIFO** | Unrelated processes, simple | Filesystem-visible | Sequential access only |
| **Unix socket** | Bidirectional, complex protocols | FD passing, datagrams | More setup |
| **POSIX shm** | Large data, low latency | Zero-copy | Needs synchronization |
| **mmap** | File-backed shared state | Persistent | Complex coherence |
| **POSIX mqueue** | Message-oriented, priority | Kernel-managed | Size limits |
| **eventfd/signalfd** | Event notification | Integrates with epoll | Linux-specific |

### 5. Process Management

```c
// Fork-exec pattern with proper error handling
pid_t pid = fork();
if (pid < 0) {
    perror("fork");
    return -1;
}
if (pid == 0) {
    // Child: close unneeded FDs, reset signals, exec
    close(parent_fd);
    signal(SIGPIPE, SIG_DFL);  // reset signal dispositions
    execvp(argv[0], argv);
    _exit(127);  // Use _exit() in child after fork, NEVER exit()
}
// Parent: wait for child
int status;
waitpid(pid, &status, 0);
if (WIFEXITED(status)) {
    return WEXITSTATUS(status);
}
```

### 6. Portable I/O Multiplexing

```c
// Prefer: epoll (Linux) > kqueue (macOS/BSD) > poll > select
#ifdef __linux__
    int epfd = epoll_create1(EPOLL_CLOEXEC);
    struct epoll_event ev = { .events = EPOLLIN, .data.fd = sockfd };
    epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);
#elif defined(__APPLE__) || defined(__FreeBSD__)
    int kq = kqueue();
    struct kevent kev;
    EV_SET(&kev, sockfd, EVFILT_READ, EV_ADD, 0, 0, NULL);
    kevent(kq, &kev, 1, NULL, 0, NULL);
#else
    struct pollfd fds[] = { { .fd = sockfd, .events = POLLIN } };
    poll(fds, 1, timeout_ms);
#endif
```

## Key References

- POSIX.1-2017 (IEEE Std 1003.1)
- "Advanced Programming in the UNIX Environment" (Stevens & Rago)
- "The Linux Programming Interface" (Kerrisk)
- `man 2 <syscall>`, `man 7 signal`, `man 7 epoll`

## Anti-Patterns

- ❌ Using `signal()` instead of `sigaction()`
- ❌ Calling `printf`/`malloc` inside signal handlers
- ❌ Forgetting `EINTR` retry loops on blocking syscalls
- ❌ Using `select()` with fd > `FD_SETSIZE`
- ❌ `fork()` without closing inherited file descriptors
- ❌ Assuming `read()`/`write()` transfer the full buffer (short reads/writes)
- ❌ Ignoring `SIGPIPE` in network programs

---
name: Network Programming in C
description: "Low-level network programming in C. BSD sockets, TCP/UDP, epoll/kqueue event loops, zero-copy I/O, protocol implementation, and high-performance server design."
category: low-level
tags: networking, sockets, tcp, udp, epoll, kqueue, c, server, protocol, io_uring
---

# Network Programming in C

Expert in low-level network programming — building high-performance servers, protocol implementations, and network tools in C.

## Use this skill when

- Implementing TCP/UDP servers and clients from scratch
- Building event-driven servers with epoll/kqueue/io_uring
- Implementing wire protocols (binary framing, TLV, length-prefixed)
- Writing high-performance proxies or load balancers
- Doing zero-copy I/O with `sendfile`, `splice`, `MSG_ZEROCOPY`
- Implementing DNS resolvers, HTTP parsers, or custom protocols
- Debugging network issues at the packet level

## Socket Programming Fundamentals

### TCP Server (Production Pattern)

```c
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>

int create_server(uint16_t port) {
    int fd = socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK | SOCK_CLOEXEC, 0);
    if (fd < 0) return -1;

    // Essential socket options
    int opt = 1;
    setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));
    setsockopt(fd, SOL_SOCKET, SO_REUSEPORT, &opt, sizeof(opt));  // Multi-process
    setsockopt(fd, IPPROTO_TCP, TCP_NODELAY, &opt, sizeof(opt));   // Disable Nagle

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(port),
        .sin_addr.s_addr = INADDR_ANY,
    };

    if (bind(fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) goto fail;
    if (listen(fd, SOMAXCONN) < 0) goto fail;
    return fd;

fail:
    close(fd);
    return -1;
}
```

### Event Loop with epoll (Linux)

```c
#include <sys/epoll.h>

#define MAX_EVENTS 1024

void event_loop(int listen_fd) {
    int epfd = epoll_create1(EPOLL_CLOEXEC);
    struct epoll_event ev = { .events = EPOLLIN | EPOLLET, .data.fd = listen_fd };
    epoll_ctl(epfd, EPOLL_CTL_ADD, listen_fd, &ev);

    struct epoll_event events[MAX_EVENTS];

    while (!shutdown_flag) {
        int n = epoll_wait(epfd, events, MAX_EVENTS, 1000 /*ms*/);
        if (n < 0) {
            if (errno == EINTR) continue;
            break;
        }

        for (int i = 0; i < n; i++) {
            int fd = events[i].data.fd;

            if (fd == listen_fd) {
                // Accept all pending connections (edge-triggered)
                while (1) {
                    int cfd = accept4(listen_fd, NULL, NULL,
                                       SOCK_NONBLOCK | SOCK_CLOEXEC);
                    if (cfd < 0) {
                        if (errno == EAGAIN) break;
                        continue;
                    }
                    ev.events = EPOLLIN | EPOLLET | EPOLLRDHUP;
                    ev.data.fd = cfd;
                    epoll_ctl(epfd, EPOLL_CTL_ADD, cfd, &ev);
                }
            } else if (events[i].events & (EPOLLERR | EPOLLHUP | EPOLLRDHUP)) {
                epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
                close(fd);
            } else if (events[i].events & EPOLLIN) {
                handle_read(fd);
            }
        }
    }
    close(epfd);
}
```

### Event Loop with kqueue (macOS/BSD)

```c
#include <sys/event.h>

void event_loop_kqueue(int listen_fd) {
    int kq = kqueue();
    struct kevent ev;
    EV_SET(&ev, listen_fd, EVFILT_READ, EV_ADD, 0, 0, NULL);
    kevent(kq, &ev, 1, NULL, 0, NULL);

    struct kevent events[MAX_EVENTS];

    while (!shutdown_flag) {
        struct timespec timeout = { .tv_sec = 1 };
        int n = kevent(kq, NULL, 0, events, MAX_EVENTS, &timeout);

        for (int i = 0; i < n; i++) {
            int fd = (int)events[i].ident;

            if (fd == listen_fd) {
                int cfd = accept(listen_fd, NULL, NULL);
                if (cfd >= 0) {
                    fcntl(cfd, F_SETFL, O_NONBLOCK);
                    EV_SET(&ev, cfd, EVFILT_READ, EV_ADD, 0, 0, NULL);
                    kevent(kq, &ev, 1, NULL, 0, NULL);
                }
            } else if (events[i].flags & EV_EOF) {
                close(fd);
            } else {
                handle_read(fd);
            }
        }
    }
    close(kq);
}
```

## Protocol Implementation

### Binary Frame Protocol (Length-Prefixed)

```c
// Wire format: [4-byte length][payload]
// All multi-byte values in network byte order (big-endian)

typedef struct {
    uint32_t length;  // payload length (network byte order)
    uint8_t  payload[];
} __attribute__((packed)) frame_t;

// Non-blocking frame reader with partial read handling
typedef struct {
    uint8_t  header[4];
    int      header_read;
    uint8_t *payload;
    uint32_t payload_len;
    uint32_t payload_read;
} frame_reader_t;

// Returns: 1=complete frame, 0=need more data, -1=error
int frame_read_step(frame_reader_t *r, int fd) {
    // Phase 1: Read header
    while (r->header_read < 4) {
        ssize_t n = read(fd, r->header + r->header_read, 4 - r->header_read);
        if (n <= 0) return (n == 0) ? -1 : (errno == EAGAIN ? 0 : -1);
        r->header_read += n;
    }

    // Parse length once header is complete
    if (!r->payload) {
        memcpy(&r->payload_len, r->header, 4);
        r->payload_len = ntohl(r->payload_len);
        if (r->payload_len > MAX_FRAME_SIZE) return -1;
        r->payload = malloc(r->payload_len);
    }

    // Phase 2: Read payload
    while (r->payload_read < r->payload_len) {
        ssize_t n = read(fd, r->payload + r->payload_read,
                          r->payload_len - r->payload_read);
        if (n <= 0) return (n == 0) ? -1 : (errno == EAGAIN ? 0 : -1);
        r->payload_read += n;
    }

    return 1;  // Complete frame
}
```

## Zero-Copy Techniques

```c
// sendfile — file → socket without user-space copy
off_t offset = 0;
ssize_t sent = sendfile(sock_fd, file_fd, &offset, file_size);

// splice — pipe-based zero-copy between two FDs (Linux)
int pipefd[2];
pipe(pipefd);
splice(in_fd, NULL, pipefd[1], NULL, len, SPLICE_F_MOVE);
splice(pipefd[0], NULL, out_fd, NULL, len, SPLICE_F_MOVE);

// MSG_ZEROCOPY — send without kernel copy (Linux 4.14+)
setsockopt(fd, SOL_SOCKET, SO_ZEROCOPY, &one, sizeof(one));
send(fd, buf, len, MSG_ZEROCOPY);
// Must poll SO_EE_ORIGIN_ZEROCOPY for completion notification
```

## TCP Tuning

```c
// Keep-alive (detect dead peers)
int keepalive = 1, idle = 60, interval = 10, count = 3;
setsockopt(fd, SOL_SOCKET, SO_KEEPALIVE, &keepalive, sizeof(int));
setsockopt(fd, IPPROTO_TCP, TCP_KEEPIDLE, &idle, sizeof(int));
setsockopt(fd, IPPROTO_TCP, TCP_KEEPINTVL, &interval, sizeof(int));
setsockopt(fd, IPPROTO_TCP, TCP_KEEPCNT, &count, sizeof(int));

// Send/receive buffer sizing
int bufsize = 256 * 1024;
setsockopt(fd, SOL_SOCKET, SO_SNDBUF, &bufsize, sizeof(int));
setsockopt(fd, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(int));

// TCP_CORK — batch small writes into full segments
int cork = 1;
setsockopt(fd, IPPROTO_TCP, TCP_CORK, &cork, sizeof(int));
// ... write header + body ...
cork = 0;
setsockopt(fd, IPPROTO_TCP, TCP_CORK, &cork, sizeof(int));  // Flush
```

## Anti-Patterns

- ❌ Using `select()` with >1024 FDs (FD_SETSIZE limit)
- ❌ Blocking `send()`/`recv()` in event-driven servers
- ❌ Forgetting to handle short reads/writes
- ❌ Not setting `SOCK_CLOEXEC` (FD leak on fork+exec)
- ❌ Using level-triggered epoll without draining (thundering herd)
- ❌ Ignoring `SIGPIPE` in network programs (set `MSG_NOSIGNAL` or `SO_NOSIGPIPE`)
- ❌ `strlen()` on network-received data that may not be null-terminated
- ❌ Trusting `Content-Length` without bounds checking

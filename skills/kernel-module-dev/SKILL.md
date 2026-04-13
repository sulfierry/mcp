---
name: Kernel Module Development
description: "Linux kernel module development. Device drivers, netfilter hooks, eBPF programs, character/block devices, procfs/sysfs interfaces, and kernel debugging."
category: low-level
tags: linux, kernel, modules, drivers, ebpf, netfilter, device-drivers, kprobes
---

# Kernel Module Development

Expert in Linux kernel-space programming — writing loadable kernel modules, device drivers, and eBPF programs.

## Use this skill when

- Writing Linux kernel modules (LKMs) for custom hardware or functionality
- Implementing character, block, or network device drivers
- Writing netfilter hooks for packet inspection/modification
- Building eBPF programs for observability, networking, or security
- Creating procfs/sysfs/debugfs interfaces
- Debugging kernel panics, oops, and deadlocks
- Understanding kernel memory allocation, locking, and synchronization

## Kernel Module Skeleton

```c
// my_module.c — Minimal loadable kernel module
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("Minimal kernel module");
MODULE_VERSION("1.0");

static int __init my_init(void) {
    pr_info("my_module: loaded\n");
    return 0;  // 0 = success, negative = errno
}

static void __exit my_exit(void) {
    pr_info("my_module: unloaded\n");
}

module_init(my_init);
module_exit(my_exit);
```

### Makefile

```makefile
obj-m := my_module.o

KDIR ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

install:
	$(MAKE) -C $(KDIR) M=$(PWD) modules_install
	depmod -a
```

```bash
# Build, load, and inspect
make
sudo insmod my_module.ko
dmesg | tail -5
lsmod | grep my_module
sudo rmmod my_module
```

## Character Device Driver

```c
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/uaccess.h>

#define DEVICE_NAME "mydev"
#define BUF_SIZE 1024

static dev_t dev_num;
static struct cdev my_cdev;
static struct class *my_class;
static char kbuf[BUF_SIZE];
static int data_len;

static int my_open(struct inode *inode, struct file *file) {
    pr_info("mydev: opened\n");
    return 0;
}

static ssize_t my_read(struct file *file, char __user *ubuf,
                        size_t count, loff_t *ppos) {
    if (*ppos >= data_len) return 0;
    if (count > data_len - *ppos) count = data_len - *ppos;

    if (copy_to_user(ubuf, kbuf + *ppos, count))
        return -EFAULT;

    *ppos += count;
    return count;
}

static ssize_t my_write(struct file *file, const char __user *ubuf,
                         size_t count, loff_t *ppos) {
    if (count > BUF_SIZE) count = BUF_SIZE;

    if (copy_from_user(kbuf, ubuf, count))
        return -EFAULT;

    data_len = count;
    *ppos = count;
    return count;
}

static int my_release(struct inode *inode, struct file *file) {
    return 0;
}

static const struct file_operations my_fops = {
    .owner   = THIS_MODULE,
    .open    = my_open,
    .read    = my_read,
    .write   = my_write,
    .release = my_release,
};

static int __init my_init(void) {
    // 1. Allocate device number
    if (alloc_chrdev_region(&dev_num, 0, 1, DEVICE_NAME) < 0)
        return -ENOMEM;

    // 2. Initialize and add cdev
    cdev_init(&my_cdev, &my_fops);
    if (cdev_add(&my_cdev, dev_num, 1) < 0) goto fail_cdev;

    // 3. Create device class and node (/dev/mydev)
    my_class = class_create(DEVICE_NAME);
    if (IS_ERR(my_class)) goto fail_class;
    device_create(my_class, NULL, dev_num, NULL, DEVICE_NAME);

    pr_info("mydev: registered major=%d minor=%d\n",
            MAJOR(dev_num), MINOR(dev_num));
    return 0;

fail_class:
    cdev_del(&my_cdev);
fail_cdev:
    unregister_chrdev_region(dev_num, 1);
    return -ENOMEM;
}

static void __exit my_exit(void) {
    device_destroy(my_class, dev_num);
    class_destroy(my_class);
    cdev_del(&my_cdev);
    unregister_chrdev_region(dev_num, 1);
    pr_info("mydev: unregistered\n");
}

module_init(my_init);
module_exit(my_exit);
```

## Kernel Memory & Locking

### Memory Allocation

| Function | Context | When to Use |
|---|---|---|
| `kmalloc(size, GFP_KERNEL)` | Process context only | Small allocations (<128KB) |
| `kmalloc(size, GFP_ATOMIC)` | Interrupt/atomic context | In IRQs, spinlock-held |
| `kzalloc(size, flags)` | Same as kmalloc | Zero-initialized |
| `vmalloc(size)` | Process context | Large, virtually contiguous |
| `devm_kmalloc(dev, size, flags)` | Device-managed | Auto-freed on device detach |
| `dma_alloc_coherent()` | DMA-capable | Needs physical contiguity |

### Locking Primitives

```c
// Mutex — sleeps, process context only
static DEFINE_MUTEX(my_mutex);
mutex_lock(&my_mutex);
// ... critical section (can sleep) ...
mutex_unlock(&my_mutex);

// Spinlock — busy-waits, any context
static DEFINE_SPINLOCK(my_lock);
unsigned long flags;
spin_lock_irqsave(&my_lock, flags);   // Save + disable IRQs
// ... critical section (CANNOT sleep, CANNOT call copy_to_user) ...
spin_unlock_irqrestore(&my_lock, flags);

// RW Lock — multiple readers, exclusive writer
static DEFINE_RWLOCK(my_rwlock);
read_lock(&my_rwlock);    // Multiple readers OK
read_unlock(&my_rwlock);
write_lock(&my_rwlock);   // Exclusive
write_unlock(&my_rwlock);

// RCU — read-side lock-free
rcu_read_lock();
ptr = rcu_dereference(global_ptr);
// ... read ptr ...
rcu_read_unlock();
// Writer side:
struct my_struct *new = kmalloc(sizeof(*new), GFP_KERNEL);
*new = *old;
new->field = new_value;
rcu_assign_pointer(global_ptr, new);
synchronize_rcu();  // Wait for all readers to finish
kfree(old);
```

## Netfilter Hook

```c
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/ip.h>
#include <linux/tcp.h>

static unsigned int my_hook(void *priv, struct sk_buff *skb,
                             const struct nf_hook_state *state) {
    struct iphdr *iph = ip_hdr(skb);
    if (!iph) return NF_ACCEPT;

    if (iph->protocol == IPPROTO_TCP) {
        struct tcphdr *tcph = tcp_hdr(skb);
        if (ntohs(tcph->dest) == 8080) {
            pr_info("Blocking packet to port 8080 from %pI4\n", &iph->saddr);
            return NF_DROP;
        }
    }
    return NF_ACCEPT;
}

static struct nf_hook_ops my_nfho = {
    .hook     = my_hook,
    .pf       = PF_INET,
    .hooknum  = NF_INET_PRE_ROUTING,
    .priority = NF_IP_PRI_FIRST,
};

static int __init my_init(void) {
    return nf_register_net_hook(&init_net, &my_nfho);
}
static void __exit my_exit(void) {
    nf_unregister_net_hook(&init_net, &my_nfho);
}
```

## eBPF (Modern Kernel Programming)

```c
// trace_open.bpf.c — eBPF program to trace file opens
#include <vmlinux.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>

struct event {
    u32 pid;
    char comm[16];
    char filename[256];
};

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    __uint(max_entries, 256 * 1024);
} events SEC(".maps");

SEC("tracepoint/syscalls/sys_enter_openat")
int trace_openat(struct trace_event_raw_sys_enter *ctx) {
    struct event *e = bpf_ringbuf_reserve(&events, sizeof(*e), 0);
    if (!e) return 0;

    e->pid = bpf_get_current_pid_tgid() >> 32;
    bpf_get_current_comm(&e->comm, sizeof(e->comm));
    bpf_probe_read_user_str(&e->filename, sizeof(e->filename),
                             (const char *)ctx->args[1]);

    bpf_ringbuf_submit(e, 0);
    return 0;
}

char LICENSE[] SEC("license") = "GPL";
```

```bash
# Build with libbpf + clang
clang -target bpf -g -O2 -c trace_open.bpf.c -o trace_open.bpf.o

# Or use bpftrace for rapid prototyping
bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'

# Common bpftrace one-liners
bpftrace -e 'kprobe:vfs_read { @reads[comm] = count(); }'
bpftrace -e 'tracepoint:block:block_rq_issue { @io[args->rwbs] = hist(args->bytes); }'
```

## Kernel Debugging

```bash
# Read kernel log
dmesg -w                     # Follow live
journalctl -k -f              # systemd equivalent

# Dynamic debug
echo 'module my_module +p' > /sys/kernel/debug/dynamic_debug/control

# /proc and /sys introspection
cat /proc/modules             # Loaded modules
cat /proc/interrupts           # IRQ assignments
cat /proc/kallsyms            # All kernel symbols
ls /sys/class/                # Device classes
ls /sys/bus/                  # Bus types

# KGDB (kernel debugger over serial)
# Boot with: kgdboc=ttyS0,115200 kgdbwait
# From host: gdb vmlinux -ex 'target remote /dev/ttyS0'

# ftrace — in-kernel function tracer
echo function > /sys/kernel/debug/tracing/current_tracer
echo my_function > /sys/kernel/debug/tracing/set_ftrace_filter
cat /sys/kernel/debug/tracing/trace
```

## Anti-Patterns

- ❌ Calling `copy_to_user`/`copy_from_user` with spinlock held
- ❌ Using `GFP_KERNEL` in interrupt/atomic context
- ❌ Sleeping in interrupt context (`mutex_lock` in IRQ handler)
- ❌ Not checking `IS_ERR()` return values from kernel APIs
- ❌ Forgetting to unregister hooks/devices in `__exit` (resource leak on rmmod)
- ❌ Using `printk` in hot paths (use tracepoints or dynamic debug)
- ❌ Not using `devm_*` managed resource APIs for device drivers
- ❌ Accessing `__user` pointers directly without `copy_from_user()`

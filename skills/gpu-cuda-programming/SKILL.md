---
name: GPU CUDA Programming
description: "CUDA C/C++ GPU programming. Kernel design, shared memory, warp-level primitives, memory coalescing, occupancy optimization, streams, and profiling with Nsight."
category: low-level
tags: cuda, gpu, nvidia, kernels, shared-memory, warp, streams, nsight, hpc
---

# GPU CUDA Programming

Expert in GPU-accelerated computing — writing high-performance CUDA kernels and managing the GPU execution model.

## Use this skill when

- Writing CUDA kernels for data-parallel computation
- Optimizing GPU memory access patterns (coalescing, bank conflicts)
- Using shared memory, warp-level primitives, and cooperative groups
- Managing GPU streams and asynchronous execution
- Profiling with Nsight Compute / Nsight Systems
- Implementing reduction, scan, histogram, sort, or matrix operations on GPU
- Integrating CUDA with PyTorch custom extensions or scientific computing

## GPU Execution Model

```
Grid (launched by host)
 └── Block (up to 1024 threads)
      └── Warp (32 threads — SIMT execution unit)
           └── Thread (one lane of the warp)

Memory Hierarchy:
  Registers (per-thread, fastest)
  Shared Memory (per-block, ~100 cycles, user-managed L1)
  L1 Cache (per-SM, automatic)
  L2 Cache (device-wide)
  Global Memory (DRAM, ~400-800 cycles, high bandwidth)
```

## Kernel Design Patterns

### 1. Basic Kernel with Grid-Stride Loop

```cuda
// Works for any array size, any grid configuration
__global__ void vector_add(const float *a, const float *b, float *c, int n) {
    for (int i = blockIdx.x * blockDim.x + threadIdx.x;
         i < n;
         i += blockDim.x * gridDim.x) {  // Grid-stride loop
        c[i] = a[i] + b[i];
    }
}

// Launch: auto-tune grid size
int block_size = 256;
int grid_size = min((n + block_size - 1) / block_size, max_blocks);
vector_add<<<grid_size, block_size>>>(d_a, d_b, d_c, n);
```

### 2. Shared Memory Tiled Matrix Multiply

```cuda
#define TILE 32

__global__ void matmul(const float *A, const float *B, float *C, int N) {
    __shared__ float As[TILE][TILE];
    __shared__ float Bs[TILE][TILE];

    int row = blockIdx.y * TILE + threadIdx.y;
    int col = blockIdx.x * TILE + threadIdx.x;
    float sum = 0.0f;

    for (int t = 0; t < (N + TILE - 1) / TILE; t++) {
        // Collaborative load into shared memory
        if (row < N && t * TILE + threadIdx.x < N)
            As[threadIdx.y][threadIdx.x] = A[row * N + t * TILE + threadIdx.x];
        else
            As[threadIdx.y][threadIdx.x] = 0.0f;

        if (col < N && t * TILE + threadIdx.y < N)
            Bs[threadIdx.y][threadIdx.x] = B[(t * TILE + threadIdx.y) * N + col];
        else
            Bs[threadIdx.y][threadIdx.x] = 0.0f;

        __syncthreads();

        for (int k = 0; k < TILE; k++)
            sum += As[threadIdx.y][k] * Bs[k][threadIdx.x];

        __syncthreads();
    }

    if (row < N && col < N)
        C[row * N + col] = sum;
}
```

### 3. Warp-Level Reduction

```cuda
// Warp-level reduction using shuffle — no shared memory needed
__device__ float warp_reduce_sum(float val) {
    for (int offset = warpSize / 2; offset > 0; offset >>= 1) {
        val += __shfl_down_sync(0xFFFFFFFF, val, offset);
    }
    return val;  // Result valid in lane 0
}

// Block-level reduction combining warp shuffle + shared memory
__device__ float block_reduce_sum(float val) {
    __shared__ float warp_sums[32];  // One per warp
    int lane = threadIdx.x % warpSize;
    int warp_id = threadIdx.x / warpSize;

    val = warp_reduce_sum(val);

    if (lane == 0) warp_sums[warp_id] = val;
    __syncthreads();

    // First warp reduces warp sums
    val = (threadIdx.x < blockDim.x / warpSize) ? warp_sums[lane] : 0.0f;
    if (warp_id == 0) val = warp_reduce_sum(val);

    return val;  // Result valid in thread 0
}
```

### 4. Streams and Async Execution

```cuda
// Overlap compute + transfer with multiple streams
cudaStream_t streams[NUM_STREAMS];
for (int i = 0; i < NUM_STREAMS; i++)
    cudaStreamCreate(&streams[i]);

for (int i = 0; i < num_chunks; i++) {
    int s = i % NUM_STREAMS;
    int offset = i * chunk_size;

    cudaMemcpyAsync(d_in + offset, h_in + offset,
                     chunk_bytes, cudaMemcpyHostToDevice, streams[s]);
    kernel<<<grid, block, 0, streams[s]>>>(d_in + offset, d_out + offset, chunk_size);
    cudaMemcpyAsync(h_out + offset, d_out + offset,
                     chunk_bytes, cudaMemcpyDeviceToHost, streams[s]);
}

for (int i = 0; i < NUM_STREAMS; i++)
    cudaStreamSynchronize(streams[i]);
```

## Memory Optimization

### Coalescing Rules

```
✅ Coalesced: threads in a warp access consecutive addresses
   Thread 0 → addr[0], Thread 1 → addr[1], ..., Thread 31 → addr[31]
   → One 128-byte transaction

❌ Strided: threads access every Nth element
   Thread 0 → addr[0], Thread 1 → addr[N], Thread 2 → addr[2N]
   → Multiple transactions, wasted bandwidth

Fix: Transpose data layout (AoS → SoA)
```

### Shared Memory Bank Conflicts

```
32 banks, each 4 bytes wide
✅ No conflict: each thread accesses a different bank
❌ N-way conflict: N threads access the same bank → serialized

// Pad shared memory to avoid bank conflicts in column access
__shared__ float tile[32][32 + 1];  // +1 padding eliminates conflicts
```

## Profiling

```bash
# Nsight Compute — kernel-level analysis
ncu --set full ./my_cuda_app

# Nsight Systems — timeline view
nsys profile --stats=true ./my_cuda_app

# Key metrics to check:
# - Achieved Occupancy (target: >50%)
# - Memory Throughput vs. Peak (target: >60% for bandwidth-bound)
# - Compute Throughput vs. Peak (target: >60% for compute-bound)
# - Warp Stall Reasons (memory dependency, synchronization, etc.)
```

## Error Handling

```cuda
// ALWAYS check CUDA errors
#define CUDA_CHECK(call) do { \
    cudaError_t err = call; \
    if (err != cudaSuccess) { \
        fprintf(stderr, "CUDA error at %s:%d: %s\n", \
                __FILE__, __LINE__, cudaGetErrorString(err)); \
        exit(EXIT_FAILURE); \
    } \
} while(0)

CUDA_CHECK(cudaMalloc(&d_ptr, size));
CUDA_CHECK(cudaMemcpy(d_ptr, h_ptr, size, cudaMemcpyHostToDevice));
kernel<<<grid, block>>>(d_ptr);
CUDA_CHECK(cudaGetLastError());      // Check launch errors
CUDA_CHECK(cudaDeviceSynchronize()); // Check execution errors
```

## Anti-Patterns

- ❌ Launching kernels with 1 thread per block
- ❌ Ignoring CUDA error return codes
- ❌ Using `cudaMallocManaged` in performance-critical paths without profiling
- ❌ Branch divergence within a warp (if/else where threads take different paths)
- ❌ Excessive global memory atomics (use shared memory reduction first)
- ❌ Not using pinned memory (`cudaHostAlloc`) for async transfers
- ❌ Forgetting `__syncthreads()` before reading shared memory written by other threads

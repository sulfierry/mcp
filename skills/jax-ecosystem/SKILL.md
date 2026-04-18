---
name: jax-ecosystem
description: "JAX functional numerical computing: jit/grad/vmap/pmap, Flax (nn), Equinox (PyTree modules), Optax (optimizers), Orbax (checkpointing), chex (testing), TFDS (data), Haiku. XLA compilation, sharding (pjit / jax.Array), TPU/GPU. Triggers on JAX, Flax, Optax, Equinox, pjit, pmap, XLA, JAX autograd, TPU training."
category: ml-framework
tags: [jax, flax, optax, equinox, xla, tpu, functional-ml]
---

# JAX Ecosystem

## Why JAX
Functional numerical computing with **composable function transforms**: `jit`, `grad`, `vmap`, `pmap`, `scan`. Backs Google's large-scale training (Gemini, PaLM). Excels at TPU, research, and anything expressible as pure-function math.

## Install
```bash
# GPU (CUDA 12)
pip install -U "jax[cuda12]"
# CPU
pip install -U jax
# TPU (in Colab / Cloud TPU)
pip install "jax[tpu]" -f https://storage.googleapis.com/jax-releases/libtpu_releases.html
```

## Core: transforms compose

```python
import jax, jax.numpy as jnp

def loss(params, x, y):
    pred = params["w"] @ x + params["b"]
    return jnp.mean((pred - y)**2)

grad_fn = jax.grad(loss)            # autodiff
grad_jit = jax.jit(grad_fn)          # XLA compile
grad_batched = jax.vmap(grad_fn, in_axes=(None, 0, 0))   # batch
grad_multi_gpu = jax.pmap(grad_fn)   # data-parallel across devices
```

## Ecosystem

| Lib | Purpose |
|-----|---------|
| **Flax** | Neural nets, HF-style. `flax.linen` classic; `flax.nnx` (2024+) stateful |
| **Equinox** | PyTorch-style modules as PyTrees (Patrick Kidger) |
| **Optax** | Optimizers (Adam, Lion, AdamW, LR schedules) |
| **Orbax** | Checkpointing, async save/load |
| **Chex** | Testing / asserting JAX code |
| **TFDS** | Dataset pipeline |
| **Penzai** | Model surgery, interpretability |
| **JMP** | Mixed precision (bf16 + fp32 stats) |
| **Brax** | RL environments (JAX-native MuJoCo-like) |
| **AlphaFold 2/3** | Open implementations use JAX |

## Flax (nnx) minimal example
```python
import flax.nnx as nnx
import optax

class MLP(nnx.Module):
    def __init__(self, din, dout, *, rngs):
        self.l1 = nnx.Linear(din, 128, rngs=rngs)
        self.l2 = nnx.Linear(128, dout, rngs=rngs)
    def __call__(self, x):
        return self.l2(nnx.relu(self.l1(x)))

model = MLP(784, 10, rngs=nnx.Rngs(0))
opt = nnx.Optimizer(model, optax.adamw(3e-4))

@nnx.jit
def train_step(model, opt, x, y):
    def loss_fn(m):
        return jnp.mean(optax.softmax_cross_entropy_with_integer_labels(m(x), y))
    loss, grads = nnx.value_and_grad(loss_fn)(model)
    opt.update(grads)
    return loss
```

## Equinox alternative
```python
import equinox as eqx
class MLP(eqx.Module):
    l1: eqx.nn.Linear; l2: eqx.nn.Linear
    def __init__(self, key):
        k1, k2 = jax.random.split(key)
        self.l1 = eqx.nn.Linear(784, 128, key=k1)
        self.l2 = eqx.nn.Linear(128, 10, key=k2)
    def __call__(self, x):
        return self.l2(jax.nn.relu(self.l1(x)))
```

## Sharding (multi-GPU/TPU) — `jax.Array` (2024+)

```python
from jax.sharding import Mesh, PartitionSpec as P
from jax.experimental.mesh_utils import create_device_mesh

mesh = Mesh(create_device_mesh((4,)), axis_names=("data",))
# Replicate model, shard data
x_sharded = jax.device_put(x, jax.sharding.NamedSharding(mesh, P("data")))
```

Replaces legacy `pmap` for most cases; automatic compilation of distributed programs via `jit`.

## Pitfalls

- Everything is immutable: `jax.numpy` arrays don't support in-place ops
- Python-side prints inside `jit` only run during tracing; use `jax.debug.print`
- Side effects (file I/O, random without PRNGKey) break JIT
- PRNG: always thread `jax.random.PRNGKey(seed)` explicitly
- `if` / `for` on traced arrays: use `jnp.where` / `jax.lax.scan`
- Recompilation: same function with different shapes/dtypes re-JITs each time
- Donate buffers (`donate_argnums`) for memory-efficient updates

## When JAX over PyTorch

| Scenario | Pick |
|----------|------|
| TPU workload | JAX (PyTorch/XLA exists but JAX-native) |
| Research requiring arbitrary function transforms (Hessian, vmap-grad, etc.) | JAX |
| Scientific ML (differential equations, physics-informed) | JAX (Diffrax, Lineax) |
| Foundation model training at scale | JAX (AlphaFold, MaxText, Pallas) |
| Mature production stack / inference | PyTorch |
| Custom CUDA kernels + Python loop | PyTorch |

## Pallas (GPU/TPU kernels in JAX)
Write fused kernels in Python-like DSL:
```python
from jax.experimental import pallas as pl
# TPU/GPU matmul kernels with explicit tile layouts
```

## References
- JAX docs: jax.readthedocs.io
- Flax nnx: flax.readthedocs.io/en/latest/nnx
- Equinox: docs.kidger.site/equinox
- Bradbury et al. — JAX autodiff (2018)

## Related
- `pytorch-lightning` (existing) — PyTorch alternative
- `llm-inference-servers` — deploy JAX-trained models
- `lora-peft-finetuning` — equivalent PEFT lives in PyTorch ecosystem

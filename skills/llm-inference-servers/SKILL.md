---
name: llm-inference-servers
description: "Production LLM inference: vLLM, SGLang, TensorRT-LLM, Text Generation Inference (TGI), llama.cpp, Ollama, MLX. PagedAttention, continuous batching, speculative decoding, prefix caching, KV-cache management, tensor/pipeline parallelism. Triggers on vLLM, SGLang, TGI, TensorRT-LLM, llama.cpp, inference server, continuous batching, PagedAttention, speculative decoding, KV cache."
category: llm-rag
tags: [vllm, sglang, tgi, tensorrt-llm, inference, llama-cpp, ollama]
---

# LLM Inference Servers

## Engine landscape (2024-2025)

| Engine | Strength | License |
|--------|----------|---------|
| **vLLM** | Throughput king; PagedAttention; broad model support | Apache-2.0 |
| **SGLang** | Fastest for structured output; RadixAttention prefix cache | Apache-2.0 |
| **TensorRT-LLM** | Max NVIDIA throughput; kernel-level opt | Apache-2.0 |
| **TGI** (HuggingFace) | Production-ready; great for HF ecosystem | Apache-2.0 |
| **llama.cpp** | CPU + metal + consumer GPU; GGUF native | MIT |
| **Ollama** | llama.cpp wrapper; trivial install | MIT |
| **MLX** (Apple) | M-series native; unified memory | MIT |
| **ExecuTorch** | On-device / edge | BSD |
| **DeepSpeed-MII** | Microsoft stack | Apache-2.0 |
| **Triton Inference Server** | Model-agnostic, NVIDIA | BSD |

## vLLM quick start

```bash
uv pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --tensor-parallel-size 2 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching
```

OpenAI-compatible API at `http://localhost:8000/v1`. Python client:
```python
from openai import OpenAI
c = OpenAI(base_url="http://localhost:8000/v1", api_key="sk-local")
r = c.chat.completions.create(model="...", messages=[...])
```

### Key vLLM features
- **PagedAttention**: KV cache as paged memory → no fragmentation
- **Continuous batching**: mix requests at different stages in one batch
- **Prefix caching**: shared system-prompt KV reused across requests (multi-turn, RAG)
- **Speculative decoding** (`--speculative-model`): draft-verify loop 2-3× speedup
- **Quant**: AWQ, GPTQ, FP8, INT4 via `--quantization awq`
- **LoRA adapters**: hot-swap via `--enable-lora --lora-modules`

## SGLang

```bash
pip install "sglang[all]"
python -m sglang.launch_server \
  --model-path meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 --port 30000 \
  --mem-fraction-static 0.9
```

Features:
- **RadixAttention**: tree-structured KV cache → 5× faster prefix reuse
- **Structured output via grammar** (regex/JSON schema) without regeneration
- **Python DSL** for complex flows:

```python
import sglang as sgl
@sgl.function
def multi_turn(s, q1, q2):
    s += sgl.user(q1) + sgl.assistant(sgl.gen("a1", max_tokens=200))
    s += sgl.user(q2) + sgl.assistant(sgl.gen("a2", max_tokens=200))
```

Benchmark: SGLang typically 2-5× faster than vLLM for structured output, similar for unstructured.

## TGI (HuggingFace)

```bash
docker run --gpus all -p 8080:80 \
  -v $PWD/data:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --quantize bitsandbytes-nf4 \
  --sharded true --num-shard 2
```

Integrates with HF Inference Endpoints, Spaces. Strong quantization support.

## TensorRT-LLM

Max NVIDIA speed (needs engine compilation):
```bash
# 1. Convert HF → TRT-LLM
trtllm-build --checkpoint_dir ./hf_ckpt \
  --output_dir ./trt_engines \
  --dtype bfloat16 \
  --max_input_len 4096 \
  --max_batch_size 16
# 2. Run via Triton or standalone
```

Use when: squeezing max throughput on H100/A100. Steep compile step is the trade-off.

## llama.cpp / Ollama (local / edge)

GGUF-quantized models on CPU + Metal + CUDA:

```bash
# llama.cpp
./llama-server -m model-Q4_K_M.gguf -c 4096 --host 0.0.0.0 --port 8080

# Ollama (wrapper)
ollama pull llama3.1:8b-instruct-q4_K_M
ollama serve
```

M-series Mac: Ollama is the fastest path. Benchmark: Llama 3.1 8B Q4_K_M ~50 t/s on M3 Max.

## MLX (Apple Silicon)

```bash
pip install mlx-lm
mlx_lm.server --model mlx-community/Llama-3.1-8B-Instruct-4bit \
  --host 0.0.0.0 --port 8080
```

Unified memory → run 70B+ models on M3 Ultra (192 GB).

## Choosing an engine

| Scenario | Pick |
|----------|------|
| Production A100/H100 fleet | vLLM (throughput) or TRT-LLM (max speed, compile cost) |
| Structured output / complex flow | SGLang |
| HF ecosystem / fast deploy | TGI |
| Consumer GPU / CPU | llama.cpp + Ollama |
| Apple Silicon | MLX or Ollama (both good) |
| Edge / mobile | ExecuTorch, llama.cpp |

## Continuous batching explained

Naive batching: wait until slowest sequence completes → GPU idle. Continuous batching: pre-empt completed sequences, insert new ones mid-batch → 2-4× throughput increase on variable-length workloads. vLLM and TGI do this natively.

## Prefix caching

Share system prompts / RAG context across requests. vLLM `--enable-prefix-caching`. SGLang `RadixAttention` handles this automatically via prefix tree. 10-100× faster on repeated prefixes.

## Speculative decoding

Draft model (small) proposes N tokens → target model verifies in one forward pass. Accept matches, regenerate mismatches. 2-3× speedup with minimal quality loss. vLLM: `--speculative-model <draft>` `--num-speculative-tokens 5`.

## Multi-GPU parallelism

- **Tensor parallel** (TP): shard model weights across GPUs per layer. Low latency, high bandwidth requirement.
- **Pipeline parallel** (PP): shard model across GPUs by layer stages. Higher latency, tolerates lower bandwidth.
- **Sequence parallel**: shard long contexts.
- **Hybrid TP+PP**: common for 70B+ models across nodes.

vLLM: `--tensor-parallel-size`, `--pipeline-parallel-size`.

## Benchmarks (Llama 3.1 8B, A100 80GB, batch 32)

| Engine | tok/s (output) |
|--------|---------------|
| vLLM | ~1800 |
| SGLang | ~2100 |
| TensorRT-LLM | ~2400 |
| TGI | ~1500 |
| llama.cpp (CUDA) | ~400 |

## Common pitfalls

- OOM with long contexts: set `--max-model-len` + `--gpu-memory-utilization` conservative
- Tokenizer mismatch when loading GGUF vs safetensors → test with known prompt first
- vLLM + LoRA: adapters must be same base model architecture
- Prefix caching breaks with per-request system prompts (defeats purpose)
- Speculative decoding: draft must share tokenizer with target

## Related

- `lora-peft-finetuning` — fine-tune, then deploy via vLLM `--enable-lora`
- `llm-quantization` — GGUF/AWQ/GPTQ for memory savings
- `rag-implementation` (existing) — pair inference with retrieval
- `langchain-architecture` (existing) — orchestration on top of inference

## References

- Kwon et al. — vLLM/PagedAttention (SOSP 2023)
- Zheng et al. — SGLang/RadixAttention (NeurIPS 2024)
- NVIDIA TensorRT-LLM docs (github.com/NVIDIA/TensorRT-LLM)
- HuggingFace TGI docs

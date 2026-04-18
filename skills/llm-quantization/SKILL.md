---
name: llm-quantization
description: "LLM quantization formats and tools: GGUF (llama.cpp), AWQ (Activation-aware), GPTQ, EXL2, BitsAndBytes (NF4/FP4), AQLM, HQQ, SmoothQuant. Conversion pipelines (llama.cpp convert, autoawq, auto-gptq). Accuracy-vs-size trade-offs, calibration data, INT4/INT8/FP8. Triggers on GGUF, AWQ, GPTQ, EXL2, quantization, llm compression, NF4, bitsandbytes, AQLM."
category: llm-rag
tags: [gguf, awq, gptq, quantization, llm-compression, bitsandbytes, nf4]
---

# LLM Quantization

## Format matrix (2024-2025)

| Format | Bits | Tool | Strength | Runtime |
|--------|------|------|----------|---------|
| **GGUF** | 2-8 | llama.cpp `convert_hf_to_gguf.py` | Universal CPU/GPU, best ecosystem | llama.cpp, Ollama, LM Studio |
| **AWQ** | 4 | autoawq | Activation-aware; best 4-bit quality | vLLM, TGI, SGLang |
| **GPTQ** | 3-4 | auto-gptq, gptqmodel | Fast, mature | vLLM, ExLlamaV2 |
| **EXL2** | 2-8 flex | exllamav2 | Best bpw-for-bpw on NVIDIA | ExLlamaV2, text-gen-webui |
| **NF4 / FP4** (BnB) | 4 | bitsandbytes | Training + inference | transformers, QLoRA |
| **AQLM** | 2 | aqlm | Extreme compression (2-bit usable) | transformers |
| **HQQ** | 1-8 | hqq | Calibration-free, fast quantize | transformers |
| **FP8 (E4M3/E5M2)** | 8 | transformer-engine, vLLM | H100 native, training + inference | H100/MI300 |
| **SmoothQuant / W8A8** | 8 | native tools | Activation smoothing | vLLM, TRT-LLM |

## GGUF quantization levels (llama.cpp)

| Quant | Bits/weight | Use |
|-------|-------------|-----|
| `Q2_K` | 2.6 | Extreme compression, quality loss |
| `Q3_K_M` | 3.3 | Small, degraded |
| `Q4_K_M` | 4.5 | **Recommended balance** |
| `Q5_K_M` | 5.5 | Near-FP16 quality |
| `Q6_K` | 6.6 | Minimal loss |
| `Q8_0` | 8.5 | Lossless-ish |
| `F16` | 16 | No quantization |
| `BF16` | 16 | Bfloat16 |

Rule: for 7-8B models, `Q4_K_M` runs comfortably on 8 GB VRAM or CPU with 6+ GB RAM.

## Convert HF → GGUF

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

python convert_hf_to_gguf.py meta-llama/Llama-3.1-8B-Instruct \
  --outfile llama-3.1-8b-f16.gguf --outtype f16

./llama-quantize llama-3.1-8b-f16.gguf llama-3.1-8b-Q4_K_M.gguf Q4_K_M
```

## AWQ (activation-aware)

```bash
pip install autoawq
```

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer
model = AutoAWQForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")

# Calibration data (~128 samples)
calib = load_dataset("mit-han-lab/pile-val-backup", split="validation").select(range(128))

model.quantize(tok, calib_data=calib,
               quant_config={"zero_point": True, "q_group_size": 128,
                             "w_bit": 4, "version": "GEMM"})
model.save_quantized("llama-3.1-8b-awq/")
tok.save_pretrained("llama-3.1-8b-awq/")
```

Deploy with vLLM: `--quantization awq`.

## GPTQ

```bash
pip install auto-gptq
```

```python
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
cfg = BaseQuantizeConfig(bits=4, group_size=128, damp_percent=0.01, desc_act=False)
model = AutoGPTQForCausalLM.from_pretrained(hf_model, cfg)
model.quantize(examples)
model.save_quantized("out-gptq/")
```

## BitsAndBytes (runtime, no pre-compute)

Used by QLoRA and on-the-fly inference:

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
bnb = BitsAndBytesConfig(
    load_in_4bit=True, bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16",
    bnb_4bit_use_double_quant=True,
)
model = AutoModelForCausalLM.from_pretrained(id, quantization_config=bnb)
```

NF4 (NormalFloat-4) theoretically optimal for Gaussian-distributed weights.

## EXL2 (ExLlamaV2)

Mixed-precision per-layer (some 2.5-bit, some 6-bit) targeting overall bpw budget. Best quality-per-bit on NVIDIA. Quantize via exllamav2 CLI.

## Quality benchmarks (Llama 3.1 8B)

| Format | MMLU drop (vs FP16) | Size |
|--------|---------------------|------|
| FP16 | 0 (baseline 68 %) | 16 GB |
| Q8_0 GGUF | < 0.1 % | 8.5 GB |
| AWQ 4-bit | ~0.5 % | 4.5 GB |
| GPTQ 4-bit | ~0.8 % | 4.5 GB |
| Q4_K_M | ~1 % | 4.6 GB |
| EXL2 4.0 bpw | ~1 % | 4 GB |
| NF4 BnB | ~1.5 % | 4.5 GB |
| Q3_K_M | ~3 % | 3.5 GB |
| AQLM 2-bit | ~5 % | 2.3 GB |
| Q2_K | ~8-15 % | 2.8 GB |

## Calibration data

AWQ/GPTQ need calibration samples (usually 128-512). Use domain-matched data for better results:
- **wikitext-2** — general pretraining
- **C4** — general
- **MMLU / ARC** — eval-style
- **Your own fine-tune data** — task-matched (best for your use case)

## Choose by target

| Goal | Pick |
|------|------|
| CPU / Apple Silicon / consumer GPU | **GGUF Q4_K_M** |
| Production GPU serving (vLLM) | **AWQ 4-bit** |
| Max 4-bit quality | **AWQ** > GPTQ > Q4_K_M |
| Extreme compression | **AQLM 2-bit** or `Q2_K` |
| Training + inference | **BnB NF4** (QLoRA) |
| H100 max speed | **FP8** (E4M3) |
| Running everywhere (zero effort) | **GGUF** via Ollama |

## FP8 (H100 / MI300)

```python
# transformers + transformer-engine on H100
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(id, torch_dtype="auto",
    device_map="auto", quantization_config={"quant_method": "fp8"})
```

vLLM: `--quantization fp8`. ~2× throughput vs bf16 on H100.

## Pitfalls

- **Calibration overfit**: use diverse data
- **GPTQ desc_act=True + group_size=128** may hurt accuracy; tune
- **BnB slower than pre-quantized** (AWQ/GPTQ) for inference
- **GGUF tokenizer mismatches** on base vs instruct: always test with chat template
- **Merging LoRA then quantizing** causes bigger drop than quantizing base + serving LoRA adapter atop
- **2-bit models** useful only if you have no other option
- **Group size trade-off**: smaller group (32) = higher quality, larger size; `g=128` standard

## Related
- `llm-inference-servers` — deploy AWQ/GPTQ/GGUF
- `lora-peft-finetuning` — QLoRA uses BnB NF4
- `llm-architect` (existing) — end-to-end LLM app design

## References
- Lin et al. — AWQ (MLSys 2024)
- Frantar et al. — GPTQ (ICLR 2023)
- Dettmers et al. — BitsAndBytes / NF4 (QLoRA, NeurIPS 2023)
- Egiazarian et al. — AQLM (ICML 2024)
- llama.cpp docs: github.com/ggerganov/llama.cpp

---
name: lora-peft-finetuning
description: "Parameter-efficient fine-tuning: LoRA, QLoRA, DoRA, IA³, Prefix Tuning, Prompt Tuning, Adapters. PEFT library (HuggingFace), Unsloth (2x speed), axolotl YAML configs, Flash Attention 2/3, RLHF/DPO/ORPO/KTO preference tuning, merging adapters, multi-adapter serving. Triggers on LoRA, QLoRA, PEFT, DoRA, fine-tune LLM, adapter, Unsloth, axolotl, DPO, ORPO, RLHF, preference tuning."
category: llm-rag
tags: [lora, qlora, peft, dpo, rlhf, fine-tuning, unsloth, axolotl]
---

# LoRA / PEFT Fine-tuning

## Parameter-efficient methods

| Method | Trainable params | Memory | Use case |
|--------|------------------|--------|----------|
| **LoRA** | 0.1-1 % | low | Task adaptation, general fine-tune |
| **QLoRA** | LoRA on 4-bit base | lowest | 70B model on single 48 GB GPU |
| **DoRA** | LoRA + magnitude/direction split | similar | Better accuracy than LoRA |
| **IA³** | diag scaling only | ~0.01 % | Tiny adapters, fast switching |
| **Prefix tuning** | soft prompt prefix | small | Generation tasks |
| **Prompt tuning** | input-level prompts | smallest | Very small tasks |
| **Full fine-tune** | 100 % | highest | When you have the budget |

## Stack (2024-2025)

- **peft** (HF) — standard adapter library
- **transformers** + **trl** — HF training + alignment
- **bitsandbytes** — 4/8-bit quantization for base model
- **Flash Attention 2/3** — memory-efficient attention
- **Unsloth** — 2× speed, 50 % VRAM on LoRA/QLoRA
- **axolotl** — YAML-driven fine-tune harness
- **Llamafactory** — web UI + CLI
- **torchtune** — PyTorch-native, composable

## QLoRA in 40 lines (Llama 3.1 8B on 24 GB)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset

bnb = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16",
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization_config=bnb,
    attn_implementation="flash_attention_2",
    device_map="auto",
)
model = prepare_model_for_kbit_training(model)

lora = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora)
model.print_trainable_parameters()

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tok.pad_token = tok.eos_token

ds = load_dataset("your/dataset", split="train")

args = TrainingArguments(
    output_dir="out/",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    optim="paged_adamw_8bit",
)

trainer = SFTTrainer(
    model=model, args=args, train_dataset=ds, tokenizer=tok,
    dataset_text_field="text", max_seq_length=2048, packing=True,
)
trainer.train()
model.save_pretrained("out/final")
```

## Unsloth (2× speed)

```python
from unsloth import FastLanguageModel, is_bfloat16_supported
model, tok = FastLanguageModel.from_pretrained(
    "unsloth/llama-3.1-8b-instruct-bnb-4bit",
    max_seq_length=2048, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, target_modules=[...], use_gradient_checkpointing="unsloth",
)
# Same trainer API as above, 2× faster, ~50 % VRAM
```

## axolotl (YAML config)

```yaml
# cfg.yaml
base_model: meta-llama/Llama-3.1-8B-Instruct
load_in_4bit: true
adapter: qlora
lora_r: 16
lora_alpha: 32
lora_target_modules: [q_proj, k_proj, v_proj, o_proj]
datasets:
  - path: tatsu-lab/alpaca
    type: alpaca
sequence_len: 2048
sample_packing: true
micro_batch_size: 4
gradient_accumulation_steps: 4
num_epochs: 3
learning_rate: 2e-4
flash_attention: true
bf16: auto
```

```bash
accelerate launch -m axolotl.cli.train cfg.yaml
```

## Hyperparameter guide

- **r** (rank): 8 (small), 16 (default), 64 (complex tasks) — diminishing returns beyond 64
- **lora_alpha**: typically 2 × r
- **lora_dropout**: 0.05-0.1
- **target_modules**: all linear > qkv-only (empirically better)
- **LR**: 1e-4 to 3e-4 (LoRA); 1e-5 to 5e-5 (full FT)
- **Warmup**: 0.03 × total steps
- **Batch size**: effective 32-128 (device × grad_accum)
- **Epochs**: 1-3 typical (watch eval loss)

## Preference tuning (after SFT)

### DPO (Direct Preference Optimization)
```python
from trl import DPOTrainer
trainer = DPOTrainer(
    model=model_sft, ref_model=None,   # uses base adapter
    beta=0.1, loss_type="sigmoid",
    train_dataset=preference_ds,       # {prompt, chosen, rejected}
    tokenizer=tok, args=args,
)
trainer.train()
```

### ORPO (2024) — no reference model
- Combines SFT + preference in one step
- `trl.ORPOTrainer`
- Simpler, often matches DPO

### KTO (Kahneman-Tversky) — binary preference
- Works with {prompt, output, label ∈ {desirable, undesirable}}
- `trl.KTOTrainer`
- Easier to collect data than pairwise

### PPO (classical RLHF)
- Separate reward model + rollouts
- `trl.PPOTrainer`
- More complex; use when DPO/ORPO plateau

## Merging adapters

```python
model = AutoModelForCausalLM.from_pretrained(base)
model = PeftModel.from_pretrained(model, "out/final")
merged = model.merge_and_unload()
merged.save_pretrained("merged/")
```

Produces full-weight model. Use for: deploy with vLLM/TGI, share on HuggingFace, continue fine-tuning.

## Multi-adapter serving (vLLM)

Keep base model loaded; hot-swap adapters per request:
```bash
python -m vllm.entrypoints.openai.api_server \
  --model base_model \
  --enable-lora \
  --lora-modules sql=./sql_adapter chat=./chat_adapter
# Request with model=sql or model=chat routes to adapter
```

## DoRA (2024)

Decomposes LoRA update into magnitude + direction. Marginal improvement over LoRA (~1-2 %) with minimal overhead:
```python
LoraConfig(... use_dora=True)
```

## Pitfalls

- **Forgetting base model tokenizer quirks** (Llama vs Mistral chat templates differ)
- **Not packing** sequences → wasted batch padding
- **Too-high LR** → base knowledge collapse (check with held-out MMLU)
- **Adapter on wrong modules**: start with all linear layers
- **Catastrophic forgetting**: mix domain data with 5-10 % general data
- **Evaluation on training distribution only** → overstates quality
- **Merging DoRA adapters changes numerics** — test inference before/after

## Related
- `llm-inference-servers` — deploy fine-tuned adapters via vLLM/SGLang
- `llm-quantization` — deploy QLoRA with GGUF post-merge
- `claude-api`, `prompt-engineer` (existing) — alternative to fine-tuning

## References
- Hu et al. — LoRA (ICLR 2022)
- Dettmers et al. — QLoRA (NeurIPS 2023)
- Liu et al. — DoRA (ICML 2024)
- Rafailov et al. — DPO (NeurIPS 2023)
- Hong et al. — ORPO (arXiv 2024)
- Unsloth docs: github.com/unslothai/unsloth
- axolotl docs: github.com/OpenAccess-AI-Collective/axolotl

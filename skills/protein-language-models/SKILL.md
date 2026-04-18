---
name: protein-language-models
description: "Protein language models (pLMs): ESM-1/2/3, ESMFold, ProtBERT, ProtT5, Ankh, SaProt, ProstT5, ProteinBERT. Embeddings for function prediction, zero-shot mutation effect, representation learning for downstream ML tasks. Triggers on ESM, ProtBERT, ProtT5, Ankh, SaProt, protein language model, pLM, protein embeddings, ESMFold."
category: scientific-writing
tags: [esm, protbert, prott5, ankh, saprot, protein-embeddings, pLM]
---

# Protein Language Models

## Model zoo (2020-2025)

| Model | Params | Context | Notable |
|-------|--------|---------|---------|
| **ESM-1b / 1v** | 650M | 1024 AA | Earlier-gen, still used |
| **ESM-2** | 8M-15B | 1024 AA | Standard embeddings; ESMFold (3B backbone) |
| **ESM-3** | 1.4B-98B | 2048 AA | Multimodal (seq + struct + function) |
| **ESMFold** | 3B | 1024 AA | Fast structure from ESM-2 embeddings |
| **ProtBERT** | 420M | 512 AA | BERT-style, simpler |
| **ProtT5** | 3B | 1024 AA | T5 encoder-decoder; strong per-residue |
| **Ankh** | 450M-1.1B | 1024 AA | Encoder; best per-param |
| **SaProt** | 650M | 1024 AA | Struct-aware tokens (3Di from Foldseek) |
| **ProstT5** | 3B | 1024 AA | Bilingual seq ↔ 3Di struct |
| **ProGen2** | 151M-6.4B | 1024 AA | Autoregressive (generation) |

## Install (HuggingFace)

```bash
pip install transformers torch accelerate fair-esm
# ESM official
pip install fair-esm
# SaProt, ProstT5 via HuggingFace
```

## Use cases

### 1. Embeddings for ML downstream
```python
import torch, esm
model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
batch_converter = alphabet.get_batch_converter()
data = [("prot1", "MKVFLKQ..."),]
_, _, tokens = batch_converter(data)
with torch.no_grad():
    out = model(tokens, repr_layers=[33])
embeddings = out["representations"][33]  # (1, L+2, 1280)
# per-protein mean embedding
protein_emb = embeddings[0, 1:-1].mean(0)  # (1280,)
```

### 2. Zero-shot mutation effect
```python
# Use ESM-1v or ESM-2 masked-likelihood
# Position 42, mutate L→V
logit_wt_at_42 = model_logits[42]["L"]
logit_mut_at_42 = model_logits[42]["V"]
effect = logit_mut_at_42 - logit_wt_at_42  # > 0: favorable
```

Use `esm-variants.nyu.edu` or `ESM-Scan` Python package.

### 3. ESMFold (structure prediction)
```python
from esm import pretrained
model = pretrained.esmfold_v1()
model = model.eval().cuda()
output = model.infer_pdb("MKVFLKQ...")
open("prediction.pdb", "w").write(output)
```
~10× faster than AF2 (no MSA). Lower accuracy than AF2 with MSA. Great for: orphan proteins, high-throughput.

### 4. ESM-3 (2024, EvolutionaryScale) — multimodal
Encoding: sequence + structure tokens (3Di) + function annotations. Generative + predictive in one. Code: `github.com/evolutionaryscale/esm`.

### 5. SaProt (struct-aware)
Foldseek 3Di tokens give pLM structural context. Better on structure-dependent tasks (binding site, allostery).

## Comparison: which model when

| Task | Best model |
|------|-----------|
| General-purpose embeddings | ESM-2 650M or Ankh (best per-param) |
| Structure-aware tasks | SaProt, ProstT5, ESM-3 |
| Fast structure prediction | ESMFold (MSA-free) |
| Mutation effect zero-shot | ESM-1v or ESM-2 |
| Generation of new sequences | ProGen2, ESM-3 |
| Long proteins (>1024) | ESM-3 (2048 ctx) or sliding window |
| CPU-only | Ankh (smallest) |

## ProtT5 (Elnaggar et al.)

```python
from transformers import T5Tokenizer, T5EncoderModel
tok = T5Tokenizer.from_pretrained("Rostlab/prot_t5_xl_uniref50")
model = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_uniref50")
# Input: space-separated residues
seq = " ".join("MKVFLKQ")
tokens = tok(seq, return_tensors="pt")
emb = model(**tokens).last_hidden_state  # (1, L+1, 1024)
```

## ProtBERT

Older, simpler BERT encoder. Rostlab/prot_bert. Use only when memory very constrained.

## Downstream applications

- **Variant effect** (pathogenicity, function): zero-shot pLL or fine-tune
- **Subcellular localization**: classification head on ESM embeddings
- **Protein-protein interaction**: concat embeddings, classifier
- **Binding site prediction**: per-residue classifier
- **Thermostability**: regressor on embeddings
- **Structure prediction**: ESMFold direct; or ESM/ProtT5 embeddings → structure module
- **Sequence design**: ProGen2 generation or ESM MLM filling

## Performance tips

- Use GPU + mixed precision (`torch.cuda.amp`)
- Batch similar-length sequences (padding waste)
- For embeddings: extract from middle layers (e.g., layer 33 of 36) — often better than final
- Cache embeddings (reuse across experiments)
- `torch.compile` for 1.5-2× speedup (PyTorch 2.0+)

## Integration

- ESM + AF2: ESMFold quick screen → AF2 validate top 10%
- ESM embeddings + RFdiffusion: embedding as conditioning signal
- pLM + LigandMPNN: sequence design with PLM prior

## Citation

- Rives et al. — ESM-1b (PNAS 2021)
- Lin et al. — ESM-2 / ESMFold (Science 2023)
- Hayes et al. — ESM-3 (Science 2025)
- Elnaggar et al. — ProtTrans / ProtBERT / ProtT5 (IEEE TPAMI 2021)
- Elnaggar et al. — Ankh (Nat Comm 2023)
- Su et al. — SaProt (ICLR 2024)

## Related
- `alphafold-suite` — AF2 comparison + MSA strategies
- `boltz-structure-prediction`, `chai-1-rosettafold` — use ESM embeddings internally
- `rfdiffusion-design`, `proteinmpnn-suite` — integrate pLM signals

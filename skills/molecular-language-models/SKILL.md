---
name: molecular-language-models
description: "Molecular language models for SMILES/SELFIES: MolFormer / MoLFormer-XL (IBM), ChemBERTa / ChemBERTa-2, SMI-TED, MolT5, ChemGPT, Uni-Mol / Uni-Mol 2, MolGPT, GROVER. Embeddings for property prediction, virtual screening, reaction prediction, generative chemistry. Triggers on MolFormer, ChemBERTa, SMI-TED, Uni-Mol, molecular language model, SMILES embeddings, chemical LM."
category: scientific-writing
tags: [molformer, chemberta, smi-ted, molecular-language-model, smiles, cheminformatics]
---

# Molecular Language Models

## Model zoo (2020-2025)

| Model | Institution | Tokens | Strengths |
|-------|-------------|--------|-----------|
| **ChemBERTa** | Seyone (UChicago) | SMILES | First BERT-style on MoleculeNet |
| **ChemBERTa-2** | DeepChem | SMILES | Improved training; MLM + MTR |
| **MolFormer** | IBM | SMILES + rotation invariance | Linear attention; 1.1B molecules trained |
| **MoLFormer-XL** | IBM | SMILES | 100M parameter, MIT-licensed HF release |
| **SMI-TED** (289M) | IBM | SMILES | Encoder-decoder; state-of-art 2024 |
| **MolT5** | Christofidellis et al. | SMILES ↔ text | Bidirectional SMILES ↔ captions |
| **Uni-Mol** | DP Technology | 3D coordinates | Equivariant; conformer-aware |
| **Uni-Mol 2** | DP Technology | 3D | 884M params; proteins + ligands |
| **ChemGPT** | Frey et al. | SELFIES | Generative, decoder-only |
| **MolGPT** | Krenn et al. | SELFIES | Small generative |
| **GROVER** | Tencent | SMILES | Graph transformer |
| **GraphMVP** | self-supervised | 3D+2D | Contrastive |

## Install + usage

### ChemBERTa-2 (HF)
```python
from transformers import AutoTokenizer, AutoModel
import torch

tok = AutoTokenizer.from_pretrained("DeepChem/ChemBERTa-77M-MTR")
model = AutoModel.from_pretrained("DeepChem/ChemBERTa-77M-MTR")

smiles = "CC(=O)Oc1ccccc1C(=O)O"  # aspirin
inputs = tok(smiles, return_tensors="pt")
out = model(**inputs)
embedding = out.last_hidden_state.mean(dim=1)  # (1, 384)
```

### MolFormer / MoLFormer-XL (IBM)
```python
# pip install transformers
from transformers import AutoModel, AutoTokenizer
tok = AutoTokenizer.from_pretrained("ibm/MoLFormer-XL-both-10pct",
                                      trust_remote_code=True)
model = AutoModel.from_pretrained("ibm/MoLFormer-XL-both-10pct",
                                    deterministic_eval=True,
                                    trust_remote_code=True)
# Batch encode
smiles_list = ["CCO", "c1ccccc1O", "CC(=O)O"]
inputs = tok(smiles_list, padding=True, return_tensors="pt")
with torch.no_grad():
    out = model(**inputs)
emb = out.pooler_output  # (3, 768)
```

### SMI-TED (2024, IBM)
```python
# Encoder-decoder; best-in-class property prediction
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
tok = AutoTokenizer.from_pretrained("ibm/smi-ted-large")
model = AutoModelForSeq2SeqLM.from_pretrained("ibm/smi-ted-large")
# Or use for: embedding extraction, SMILES → properties via fine-tune,
# SMILES → SMILES generation
```

### Uni-Mol 2 (3D-aware)
```bash
pip install unimol-tools
```
```python
from unimol_tools import UniMolRepr
clf = UniMolRepr(data_type='molecule', remove_hs=False)
# Input list of SMILES or SDF
smiles = ['CCO', 'c1ccccc1O']
reprs = clf.get_repr(smiles)  # uses auto-generated 3D conformers
```

## Use cases

### 1. Property prediction (fine-tune)
- Solubility (ESOL), lipophilicity, BBBP, Tox21, ClinTox (MoleculeNet benchmark)
- Small dataset: linear probe on frozen embeddings
- Large dataset: fine-tune last 2-4 layers + classifier head

### 2. Virtual screening embeddings
- Embed library (ChEMBL, ZINC, Enamine REAL) with MoLFormer-XL
- Cosine similarity search against hit query
- Faster than fingerprint-based search for large libraries

### 3. Generative chemistry
- MolT5 for SMILES↔description
- MolGPT / ChemGPT for de novo generation
- Reinforcement learning with pLM reward

### 4. Reaction prediction
- Molecular Transformer (Schwaller) — reactant + reagent → product
- RXN-chemistry (IBM) — forward + retrosynthesis

## When to use which

| Task | Model |
|------|-------|
| General-purpose 1D embedding | MoLFormer-XL or ChemBERTa-2 |
| 3D-aware embeddings | Uni-Mol 2 |
| State-of-art property prediction 2024+ | SMI-TED |
| Tiny compute budget | ChemBERTa-77M-MTR |
| Generative SMILES | MolT5 (conditional) or ChemGPT |
| SMILES↔text | MolT5 |
| Reaction prediction | Molecular Transformer / RXN |

## Benchmark (MoleculeNet, AUROC higher=better)

| Model | BBBP | Tox21 | ClinTox | HIV |
|-------|------|-------|---------|-----|
| ChemBERTa | 0.64 | 0.73 | 0.73 | 0.62 |
| MoLFormer-XL | 0.84 | 0.80 | 0.97 | 0.82 |
| SMI-TED | 0.86 | 0.81 | 0.98 | 0.83 |
| Uni-Mol (3D) | 0.86 | 0.79 | 0.92 | 0.81 |

MoLFormer-XL and SMI-TED are currently (2024-2025) top performers for 1D SMILES input.

## SELFIES encoding
For robust generation (100% valid molecules):
```python
import selfies as sf
selfies = sf.encoder("CC(=O)O")  # → "[C][C][=Branch1][C][=O][O]"
back = sf.decoder(selfies)
```
ChemGPT uses SELFIES. Prevents invalid SMILES from random generation.

## Integration

- Combine with RDKit descriptors (concat features)
- Use for ligand featurization → ML pipeline (scikit-learn, XGBoost)
- Input to downstream DeepChem models
- Couple with Uni-Mol for 3D tasks (pose, QSAR)
- Embed candidates for DiffDock-L virtual screening

## Fine-tuning tips
- Learning rate: 1e-5 to 5e-5 for fine-tune; 1e-3 for linear probe
- Batch size: 32-128 depending on sequence length
- SMILES canonicalization: use RDKit before tokenization
- Data augmentation: SMILES enumeration (10× multiple SMILES per molecule) boosts small-data performance
- Early stopping: watch val loss; transformers overfit quickly

## Failure modes
- Invalid SMILES input → tokenizer warning; canonicalize first
- Out-of-distribution molecules (very large, metallics) → low-quality embeddings
- Property prediction on very small data (<100 examples) → fingerprints + Random Forest may beat LM
- Stereo chemistry: canonical SMILES drops some info; use isomeric SMILES explicitly

## Citation
- Chithrananda et al. — ChemBERTa (2020)
- Ahmad et al. — ChemBERTa-2 (2022)
- Ross et al. — MolFormer / MoLFormer-XL (Nat Mach Intell 2022)
- Soares et al. — SMI-TED (IBM 2024)
- Christofidellis et al. — MolT5 (ICML 2023)
- Zhou et al. — Uni-Mol (ICLR 2023) / Uni-Mol 2 (NeurIPS 2024)

## Related
- `rdkit`, `datamol`, `molfeat` — classical fingerprints and descriptors
- `deepchem`, `torchdrug` — unified ML-chem frameworks
- `protein-language-models` — protein side (ESM, ProtBERT)
- `modern-ai-docking` — uses molecular embeddings
- `boltz-structure-prediction` — ligand input

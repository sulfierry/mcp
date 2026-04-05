---
name: Kinase Interaction Modeling
description: "Expert skill for kinase-drug interaction modeling using deep learning. Covers DT-Kinase Level 4 CNN architecture, embedding adapters, drug-target interaction prediction, and benchmarking against DrugBAN/GraphBAN."
category: drug-discovery
tags: kinase, drug-target, dti, cnn, embedding, drugban, graphban, deep-learning, interaction
source: custom
---

# Kinase Interaction Modeling

## Use this skill when

- Building drug-target interaction (DTI) prediction models for kinase targets
- Working with the DT-Kinase Level 4 CNN architecture
- Using pre-trained protein/molecule embeddings with adapter layers
- Benchmarking DTI models against DrugBAN and GraphBAN baselines
- Processing kinase-specific datasets (human and non-human kinases)
- Evaluating binary classification performance with MCC, AUROC, and AUPRC
- Implementing Platt Scaling for probability calibration

## Do not use this skill when

- Performing molecular docking (use molecular-docking skill)
- Doing molecular dynamics simulations
- Working with protein-protein interactions (not drug-protein)

## Instructions

### Architecture Overview

The DT-Kinase system uses a multi-level architecture:

```
Level 1: Sequence → Embedding (ESM-2 for proteins, MolBERT for drugs)
Level 2: Embedding → Adapted Embedding (trainable adapter layers)
Level 3: Adapted Embeddings → Interaction Features (bilinear attention)
Level 4: Features → Binary Prediction (CNN classifier)
```

### Prerequisites

```bash
pip install torch numpy pandas scikit-learn
pip install fair-esm  # ESM-2 protein embeddings
pip install transformers  # MolBERT drug embeddings
```

### Embedding Adapter Pattern

```python
import torch
import torch.nn as nn

class EmbeddingAdapter(nn.Module):
    """Lightweight adapter to project pre-trained embeddings to 
    a shared interaction space. Uses residual connection to preserve
    pre-trained signal while learning task-specific features."""
    
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, 
                 dropout: float = 0.1):
        super().__init__()
        self.projection = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim),
            nn.LayerNorm(output_dim),
        )
        # Residual if dimensions match
        self.residual = nn.Linear(input_dim, output_dim) if input_dim != output_dim else nn.Identity()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.projection(x) + self.residual(x)


class DTKinaseLevel4(nn.Module):
    """Level 4 CNN for drug-target interaction prediction.
    
    Takes adapted drug and protein embeddings, computes a bilinear 
    attention-based interaction map, then classifies via 1D CNN.
    """
    
    def __init__(self, drug_dim: int = 768, protein_dim: int = 1280,
                 hidden_dim: int = 256, n_filters: int = 128):
        super().__init__()
        
        # Adapters
        self.drug_adapter = EmbeddingAdapter(drug_dim, hidden_dim, hidden_dim)
        self.protein_adapter = EmbeddingAdapter(protein_dim, hidden_dim, hidden_dim)
        
        # Bilinear attention
        self.bilinear = nn.Bilinear(hidden_dim, hidden_dim, n_filters)
        
        # CNN classifier
        self.classifier = nn.Sequential(
            nn.Conv1d(n_filters, n_filters, kernel_size=3, padding=1),
            nn.BatchNorm1d(n_filters),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1),
            nn.Flatten(),
            nn.Linear(n_filters, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1),
        )
    
    def forward(self, drug_emb: torch.Tensor, protein_emb: torch.Tensor) -> torch.Tensor:
        d = self.drug_adapter(drug_emb)    # (B, hidden)
        p = self.protein_adapter(protein_emb)  # (B, hidden)
        
        # Bilinear interaction
        interaction = self.bilinear(d, p)  # (B, n_filters)
        
        # Reshape for CNN: (B, n_filters, 1)
        x = interaction.unsqueeze(-1)
        
        return self.classifier(x).squeeze(-1)
```

### Training Loop with Platt Scaling

```python
import torch
from sklearn.metrics import matthews_corrcoef, roc_auc_score, average_precision_score
from sklearn.linear_model import LogisticRegression
import numpy as np

def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    for drug, protein, label in loader:
        drug, protein, label = drug.to(device), protein.to(device), label.to(device)
        
        optimizer.zero_grad()
        logits = model(drug, protein)
        loss = criterion(logits, label.float())
        loss.backward()
        
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        total_loss += loss.item()
    
    return total_loss / len(loader)


def evaluate_with_platt(model, loader, device):
    """Two-pass evaluation: collect logits, then calibrate with Platt Scaling."""
    model.eval()
    all_logits, all_labels = [], []
    
    with torch.no_grad():
        for drug, protein, label in loader:
            logits = model(drug.to(device), protein.to(device))
            all_logits.extend(logits.cpu().numpy())
            all_labels.extend(label.numpy())
    
    logits = np.array(all_logits).reshape(-1, 1)
    labels = np.array(all_labels)
    
    # Platt Scaling: fit logistic regression on logits → calibrated probabilities
    platt = LogisticRegression(C=1.0, solver='lbfgs')
    platt.fit(logits, labels)
    probs = platt.predict_proba(logits)[:, 1]
    
    # Sweep thresholds for optimal MCC
    best_mcc, best_thresh = -1, 0.5
    for thresh in np.arange(0.1, 0.9, 0.01):
        preds = (probs >= thresh).astype(int)
        mcc = matthews_corrcoef(labels, preds)
        if mcc > best_mcc:
            best_mcc, best_thresh = mcc, thresh
    
    preds = (probs >= best_thresh).astype(int)
    
    return {
        "mcc": matthews_corrcoef(labels, preds),
        "auroc": roc_auc_score(labels, probs),
        "auprc": average_precision_score(labels, probs),
        "threshold": best_thresh,
        "platt_model": platt,
    }
```

### Benchmarking Protocol

```python
def benchmark_comparison(results: dict):
    """Compare DT-Kinase against DrugBAN and GraphBAN baselines."""
    
    baselines = {
        "DrugBAN": {"mcc": 0.45, "auroc": 0.82, "auprc": 0.78},
        "GraphBAN": {"mcc": 0.43, "auroc": 0.80, "auprc": 0.76},
    }
    
    print(f"{'Model':<20} {'MCC':>8} {'AUROC':>8} {'AUPRC':>8}")
    print("-" * 48)
    print(f"{'DT-Kinase L4':<20} {results['mcc']:>8.3f} {results['auroc']:>8.3f} {results['auprc']:>8.3f}")
    
    for name, base in baselines.items():
        print(f"{name:<20} {base['mcc']:>8.3f} {base['auroc']:>8.3f} {base['auprc']:>8.3f}")
    
    # Target: MCC > 0.5
    if results['mcc'] > 0.5:
        print(f"\n✅ Target MCC > 0.5 ACHIEVED ({results['mcc']:.3f})")
    else:
        gap = 0.5 - results['mcc']
        print(f"\n⚠ Target MCC > 0.5 not met (gap: {gap:.3f})")
```

### Key Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `hidden_dim` | 256 | 128-512 | Shared embedding dimension |
| `n_filters` | 128 | 64-256 | CNN filter count |
| `dropout` | 0.3 | 0.1-0.5 | Regularization strength |
| `learning_rate` | 1e-4 | 1e-5 to 1e-3 | Adam optimizer LR |
| `grad_clip` | 1.0 | 0.5-5.0 | Gradient clipping norm |
| `platt_C` | 1.0 | 0.01-100 | Platt Scaling regularization |

### Version Compatibility

- PyTorch: 2.0+
- scikit-learn: 1.3+
- fair-esm: 2.0+
- transformers: 4.30+

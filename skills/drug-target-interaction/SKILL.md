---
name: Drug-Target Interaction Analysis
description: "Expert skill for drug-target interaction (DTI) data processing, feature engineering, and interaction analysis. Covers ChEMBL data retrieval, molecular fingerprints, protein descriptors, and interaction network analysis."
category: drug-discovery
tags: dti, chembl, fingerprints, drug-target, interaction-network, cheminformatics
source: custom
---

# Drug-Target Interaction Analysis

## Use this skill when

- Retrieving drug-target bioactivity data from ChEMBL
- Computing molecular fingerprints (Morgan/ECFP, MACCS, topological)
- Generating protein sequence descriptors for ML models
- Building interaction networks between drugs and targets
- Curating positive/negative DTI datasets for ML training
- Analyzing SAR (Structure-Activity Relationships) across kinase families

## Do not use this skill when

- Running docking simulations (use molecular-docking skill)
- Training deep learning DTI models (use kinase-interaction-modeling skill)
- Analyzing protein 3D structures (use protein-structure-analysis skill)

## Instructions

### Prerequisites

```bash
pip install chembl_webresource_client rdkit-pypi pandas numpy networkx
pip install biopython  # for protein sequence processing
```

### ChEMBL Data Retrieval

```python
from chembl_webresource_client.new_client import new_client
import pandas as pd

def get_kinase_bioactivities(target_chembl_id: str, 
                              activity_type: str = "IC50",
                              max_nm: float = 10000) -> pd.DataFrame:
    """Retrieve bioactivity data for a kinase target from ChEMBL."""
    
    activity = new_client.activity
    results = activity.filter(
        target_chembl_id=target_chembl_id,
        standard_type=activity_type,
        standard_units="nM",
        standard_relation="=",
    ).only([
        "molecule_chembl_id", "canonical_smiles",
        "standard_value", "standard_type",
        "pchembl_value", "assay_chembl_id",
    ])
    
    df = pd.DataFrame(results)
    df["standard_value"] = pd.to_numeric(df["standard_value"], errors="coerce")
    df = df[df["standard_value"] <= max_nm].dropna(subset=["canonical_smiles"])
    
    # Binary label: active if IC50 < 1000 nM
    df["active"] = (df["standard_value"] < 1000).astype(int)
    
    print(f"Retrieved {len(df)} bioactivities for {target_chembl_id}")
    print(f"  Active: {df['active'].sum()}, Inactive: {(~df['active'].astype(bool)).sum()}")
    
    return df


# Example: EGFR kinase
egfr_data = get_kinase_bioactivities("CHEMBL203")
```

### Molecular Fingerprints

```python
from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys
import numpy as np

def compute_fingerprints(smiles_list: list, fp_type: str = "morgan",
                          radius: int = 2, n_bits: int = 2048) -> np.ndarray:
    """Compute molecular fingerprints for a list of SMILES."""
    fps = []
    
    for smiles in smiles_list:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            fps.append(np.zeros(n_bits))
            continue
        
        if fp_type == "morgan":
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        elif fp_type == "maccs":
            fp = MACCSkeys.GenMACCSKeys(mol)
            n_bits = 167  # MACCS has fixed 167 keys
        elif fp_type == "topological":
            fp = Chem.RDKFingerprint(mol, fpSize=n_bits)
        else:
            raise ValueError(f"Unknown fingerprint type: {fp_type}")
        
        arr = np.zeros(n_bits)
        fp_bits = fp.GetOnBits()
        arr[list(fp_bits)] = 1
        fps.append(arr)
    
    return np.array(fps)
```

### Protein Sequence Descriptors

```python
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import numpy as np

def compute_protein_descriptors(sequence: str) -> dict:
    """Compute physicochemical descriptors from protein sequence."""
    analysis = ProteinAnalysis(sequence)
    
    # AAC: Amino Acid Composition
    aac = analysis.get_amino_acids_percent()
    
    descriptors = {
        "molecular_weight": analysis.molecular_weight(),
        "aromaticity": analysis.aromaticity(),
        "instability_index": analysis.instability_index(),
        "isoelectric_point": analysis.isoelectric_point(),
        "gravy": analysis.gravy(),  # Grand Average of Hydropathy
        "helix_fraction": analysis.secondary_structure_fraction()[0],
        "sheet_fraction": analysis.secondary_structure_fraction()[1],
        "coil_fraction": analysis.secondary_structure_fraction()[2],
        "sequence_length": len(sequence),
    }
    
    # Add amino acid composition
    for aa, pct in aac.items():
        descriptors[f"aac_{aa}"] = pct
    
    return descriptors
```

### Interaction Network Analysis

```python
import networkx as nx
import pandas as pd

def build_dti_network(interactions: pd.DataFrame,
                      drug_col: str = "molecule_chembl_id",
                      target_col: str = "target_chembl_id",
                      weight_col: str = "pchembl_value") -> nx.Graph:
    """Build a bipartite drug-target interaction network."""
    
    G = nx.Graph()
    
    for _, row in interactions.iterrows():
        drug = row[drug_col]
        target = row[target_col]
        weight = row.get(weight_col, 1.0)
        
        G.add_node(drug, bipartite=0, node_type="drug")
        G.add_node(target, bipartite=1, node_type="target")
        G.add_edge(drug, target, weight=float(weight) if pd.notna(weight) else 1.0)
    
    drugs = {n for n, d in G.nodes(data=True) if d.get("node_type") == "drug"}
    targets = {n for n, d in G.nodes(data=True) if d.get("node_type") == "target"}
    
    print(f"Network: {len(drugs)} drugs, {len(targets)} targets, {G.number_of_edges()} interactions")
    print(f"Avg drug degree: {sum(G.degree(d) for d in drugs)/len(drugs):.1f}")
    print(f"Avg target degree: {sum(G.degree(t) for t in targets)/len(targets):.1f}")
    
    return G
```

### Version Compatibility

- chembl_webresource_client: 0.10+
- RDKit: 2023.09+
- BioPython: 1.81+
- NetworkX: 3.1+

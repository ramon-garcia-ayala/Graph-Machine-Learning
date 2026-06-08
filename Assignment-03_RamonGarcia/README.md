# Assignment 03 — Building-Ground Relationship Graph Classification

**Student:** Ramon Garcia  
**Course:** Graph Machine Learning — IAAC  

---

## Building Model

The building was modeled in Rhino and exported as four OBJ layers:

| Layer | Cell type | Color | Count |
|-------|-----------|-------|-------|
| Ground slab / podium | `0` — Separation | Red | 20 |
| Office volumes | `1` — Separation with Plinth | Green | 192 |
| Columns | `2` — Adherence | Blue | 72 |
| Core + corridors | `3` — Interlock | Purple | 26 |

### Original Building

![Original Building Ghosted](assets/02.%20Original%20Building_Ghosted.png)

---

## Graph Construction

**Pipeline:** OBJ → `Topology.ByOBJPath` → faces → `SelfMerge` → closed cells → adjacency edges → `Graph.ByVerticesEdges` → CSV export

- Each **closed geometry** (column, office, core volume, ground slab) becomes **one graph node**.
- Two nodes are connected by an edge if their geometries **touch** (boundary distance < 0.01).
- No `SelfMerge` of all cells into a single CellComplex — this avoids face-splitting that would inflate the node count.

### Geometry (colored by type)

| Color | Element |
|-------|---------|
| 🔴 Red | Ground slab / podium |
| 🟢 Green | Office volumes |
| 🔵 Blue | Columns |
| 🟣 Purple | Core + corridors |

![White Geometry](assets/A.%20White.png)

![Coloured Geometry](assets/B.%20Colour.png)

### Adjacency Graph

![Graph](assets/C.%20Graph.png)

**Graph statistics:**
- Nodes: **310**
- Edges: **1590**
- Node features: one-hot encoding of `cell_type` → `[feature_00, feature_01, feature_02, feature_03]`

---

## Graph Classification — Results

The pre-trained **BGR (Building-Ground Relationship)** model classifies the graph into one of five categories:

| Label | Category |
|-------|----------|
| 0 | Separation |
| 1 | Separation with Plinth |
| 2 | Adherence |
| 3 | Adherence with Plinth |
| 4 | Interlock |

### Prediction

| | Value | Label |
|---|---|---|
| **Manual assignment** | `0` | Separation |
| **Model prediction** | `1` | Separation with Plinth |
| **Confidence** | — | **94%** |

The model predicts **Separation with Plinth** with 94% confidence. The manual label assigned was **Separation** (label 0). The difference between the two is subtle — both describe a building that sits above or apart from the ground plane, with the model detecting plinth-like characteristics (the elevated ground slab / podium layer) that justify the one-step shift.

---

## Notebooks

| Notebook | Description |
|----------|-------------|
| `01. Creating BGR Graph.ipynb` | Import OBJ geometry → build graph → export CSV dataset |
| `02. Graph Classification of Unseen Data.ipynb` | Load dataset → load pre-trained model → predict → visualize results |

---

## File Structure

```
Assignment-03_RamonGarcia/
├── assets/                        # Renders and graph visualizations
├── dataset_graph_classification/  # Exported CSV dataset (graphs, nodes, edges)
├── geometries/
│   └── obj_geometry_v2.0/         # OBJ exports from Rhino (ground, columns, offices, core)
├── models/
│   └── pyg_model.pt               # Pre-trained PyG classification model
└── notebooks/
    ├── 01. Creating BGR Graph.ipynb
    └── 02. Graph Classification of Unseen Data.ipynb
```

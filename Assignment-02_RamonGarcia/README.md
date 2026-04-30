# Flow and Accessibility Analysis in a Multi-Family Residential Building through Topological Graphs

**Author:** Ramón García Ayala  
**Course:** MaCAD — Graph Machine Learning & Environment  
**Institution:** IAAC — Institute for Advanced Architecture of Catalonia  
**Assignment:** S02 — Submission 01

---

## Overview

This project applies **topological graph theory** to analyze the flow and accessibility patterns of a multi-family residential building. Using the `topologicpy` library, the building geometry is imported from a 3D model and decomposed into topological cells (rooms), apertures (windows and doors), and connectivity graphs that reveal spatial relationships invisible in conventional architectural representations.

The core question explored is: **how do residents move through and access the different spaces in a multi-family building?** By translating the physical building into primal and dual graphs — and by incorporating apertures as shared boundaries — the analysis produces a quantifiable model of spatial accessibility and flow.

---

## Building Model

The building is a multi-story multi-family residential block containing:

| Element | Count |
|---------|-------|
| Rooms (cells) | 31 |
| Windows | 44 |
| Doors | 33 |
| Total apertures | 77 |

Rooms are classified and color-coded by program:

| Color | Program |
|-------|---------|
| Blue | Living rooms & bedrooms |
| Red | Corridors |
| Green | Stairs |
| Yellow | Service spaces |
| Gray | Other |

---

## Methodology

### 1. Geometry Import
The building walls, windows, and doors are imported as separate `.obj` files using `Topology.ByOBJPath()` and assembled into a topological cell complex via `CellComplex.ByCells()`.

### 2. Aperture Assignment
Windows and doors are registered as apertures on the shared faces between rooms using `Topology.AddApertures()`. This encodes the physical openings as topological connections.

### 3. Graph Derivation
Three graph types are derived from the building topology:

- **Access Graph (via shared apertures):** Nodes represent rooms; edges connect rooms that share a door or window. This models direct physical accessibility between adjacent spaces.
- **Dual Graph:** Each room is a node; edges connect rooms that share any face (wall), regardless of apertures. This models spatial adjacency.
- **Primal Graph:** Nodes represent the geometry's vertices; edges follow the building's structural edges. This is the geometric skeleton of the model.

---

## Results

### Scene 1 — 3D Perspective: Access Graph on Building Volume
Full three-dimensional view of the building with rooms colored by program type and the access graph overlaid, showing node-to-node connectivity across all floors.

![Scene 1 — 3D View](Deliverables/Scene_01.png)

---

### Scene 2 — Elevation: Floor-by-Floor Connectivity
Front elevation view exposing the vertical and horizontal relationships between rooms. The graph makes explicit how corridors (red) act as primary distribution nodes connecting living spaces (blue) to service areas (yellow).

![Scene 2 — Elevation View](Deliverables/Scene_02.png)

---

### Scene 3 — Plan: Spatial Access Map
Top-down plan view of the building with the access graph projected onto the floor plan. This reveals the hierarchical structure of movement — from the stair core outward to individual dwelling units — and highlights which spaces are most and least accessible.

![Scene 3 — Plan View](Deliverables/Scene_03.png)

---

## Tools & Dependencies

| Tool | Purpose |
|------|---------|
| [topologicpy](https://github.com/wassimj/topologicpy) `≥ 0.9.18` | Topological modeling and graph derivation |
| [Plotly](https://plotly.com/python/) | Interactive 3D visualization |
| [Grasshopper / Rhino](https://www.rhino3d.com/) | 3D building model generation |
| Python 3.x / Jupyter Notebook | Analysis environment |

---

## Repository Contents

```
TopologicFlow/
├── S02-Submission 01_Graphs.ipynb   # Main analysis notebook
├── Deliverables/
│   ├── Scene_01.png                 # 3D perspective view
│   ├── Scene_02.png                 # Elevation view
│   └── Scene_03.png                 # Plan view
└── README.md
```

---

## How to Run

1. Install dependencies:
   ```bash
   pip install topologicpy plotly
   ```
2. Update the `.obj` file paths in **Cell 4** of the notebook to point to your local asset folder.
3. Run all cells in order (`Kernel > Restart & Run All`).

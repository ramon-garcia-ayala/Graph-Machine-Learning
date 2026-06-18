# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-17 23:22:31_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:/IAAC Local GIT Repositories/Graph ML - Environment/Final_Project\3D-Models\Marsella_3-Apartments.obj |
| `GRID_SIZE` | 2 |
| `FLOOR_HEIGHT` | 10.0 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 1.0 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 3.0 |
| `n_stair_locations` | 4 |

## Geometry

- **Plan bounding box:** X [106.51, 114.97], Y [333.38, 357.48]  (8.46 × 24.10 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 189 | 50 |
| Floor 2 (Z=4) | 88 | 38 |
| Floor 3 (Z=8) | 191 | 36 |

## Building graph

- Nodes: **124**  |  Edges: **197**  |  Density: **0.02583**  |  Stair edges: **4**

## Minimum Spanning Tree

- Vertices: 124  |  Edges: 123  |  Density: 0.01613

## Cross-floor shortest path

- Length: **40.4**  |  Nodes: 13
  |  Simplified: 37.1 (6 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0081 | 0.0488 | 0.0258 | 0.0066 | [0.026341, 0.026529, 0.02439] |
| Closeness | 0.0697 | 0.1482 | 0.1080 | 0.0220 | [0.101677, 0.126588, 0.097177] |
| Betweenness | 0.0000 | 0.5078 | 0.0710 | 0.0881 | [0.062879, 0.09225, 0.059921] |

**Top 5 degree hubs:**

- Floor 1 (110.51, 341.38) → 0.0488 (6 connections)
- Floor 2 (110.51, 349.38) → 0.0488 (6 connections)
- Floor 1 (110.51, 335.38) → 0.0325 (4 connections)
- Floor 1 (112.51, 335.38) → 0.0325 (4 connections)
- Floor 1 (110.51, 337.38) → 0.0325 (4 connections)

## Community detection

- Communities: **7**  |  Total cells: 124  |  Total area: ~496 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 12 | 48 |
| 1 | 19 | 76 |
| 2 | 21 | 84 |
| 3 | 16 | 64 |
| 4 | 20 | 80 |
| 5 | 22 | 88 |
| 6 | 14 | 56 |

## Visibility Graph Analysis (per floor)

| Floor | Viewpoints | min | max | mean |
|---|---|---|---|---|
| Floor 1 | 190 | 38 | 144 | 94.905 |
| Floor 2 | 151 | 16 | 128 | 82.503 |
| Floor 3 | 147 | 17 | 98 | 57.973 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
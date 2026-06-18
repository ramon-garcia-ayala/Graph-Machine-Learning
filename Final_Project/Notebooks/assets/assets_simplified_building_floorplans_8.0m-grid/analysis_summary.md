# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-18 14:43:59_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:\IAAC Local GIT Repositories\Graph ML - Environment\Final_Project\3D-Models\Marsella_3-Floor-Plans_SIMPLIFIED.obj |
| `GRID_SIZE` | 8 |
| `FLOOR_HEIGHT` | 30 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 5.0 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 5.0 |
| `n_stair_locations` | 58 |

## Geometry

- **Plan bounding box:** X [228.75, 361.25], Y [5.25, 28.75]  (132.50 × 23.50 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 804 | 72 |
| Floor 2 (Z=4) | 696 | 33 |
| Floor 3 (Z=8) | 864 | 72 |

## Building graph

- Nodes: **177**  |  Edges: **325**  |  Density: **0.02087**  |  Stair edges: **61**

## Minimum Spanning Tree

- Vertices: 177  |  Edges: 176  |  Density: 0.01130

## Cross-floor shortest path

- Length: **189.0**  |  Nodes: 19
  |  Simplified: 181.6 (6 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0114 | 0.0284 | 0.0209 | 0.0048 | [0.020833, 0.021866, 0.020438] |
| Closeness | 0.0829 | 0.1687 | 0.1234 | 0.0202 | [0.121713, 0.132521, 0.12102] |
| Betweenness | 0.0003 | 0.2632 | 0.0419 | 0.0385 | [0.037123, 0.058684, 0.038972] |

**Top 5 degree hubs:**

- Floor 1 (236.75, 13.25) → 0.0284 (5 connections)
- Floor 1 (244.75, 13.25) → 0.0284 (5 connections)
- Floor 1 (252.75, 13.25) → 0.0284 (5 connections)
- Floor 1 (260.75, 13.25) → 0.0284 (5 connections)
- Floor 1 (268.75, 13.25) → 0.0284 (5 connections)

## Community detection

- Communities: **9**  |  Total cells: 177  |  Total area: ~11328 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 18 | 1152 |
| 1 | 17 | 1088 |
| 2 | 22 | 1408 |
| 3 | 26 | 1664 |
| 4 | 16 | 1024 |
| 5 | 12 | 768 |
| 6 | 24 | 1536 |
| 7 | 16 | 1024 |
| 8 | 26 | 1664 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-18 14:46:39_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:/IAAC Local GIT Repositories/Graph ML - Environment/Final_Project\3D-Models\Marsella_3-Apartments.obj |
| `GRID_SIZE` | 1 |
| `FLOOR_HEIGHT` | 10.0 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 0.3 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 1 |
| `n_stair_locations` | 4 |

## Geometry

- **Plan bounding box:** X [106.51, 114.97], Y [333.38, 357.48]  (8.46 × 24.10 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 187 | 190 |
| Floor 2 (Z=4) | 88 | 154 |
| Floor 3 (Z=8) | 191 | 144 |

## Building graph

- Nodes: **488**  |  Edges: **848**  |  Density: **0.00714**  |  Stair edges: **4**

## Minimum Spanning Tree

- Vertices: 488  |  Edges: 487  |  Density: 0.00410

## Cross-floor shortest path

- Length: **49.0**  |  Nodes: 32
  |  Simplified: 41.0 (6 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0021 | 0.0103 | 0.0071 | 0.0013 | [0.007176, 0.007334, 0.006873] |
| Closeness | 0.0330 | 0.0689 | 0.0508 | 0.0096 | [0.046858, 0.059505, 0.046795] |
| Betweenness | 0.0000 | 0.4786 | 0.0400 | 0.0658 | [0.031526, 0.057745, 0.032157] |

**Top 5 degree hubs:**

- Floor 1 (110.51, 340.38) → 0.0103 (5 connections)
- Floor 1 (111.51, 340.38) → 0.0103 (5 connections)
- Floor 2 (110.51, 340.38) → 0.0103 (5 connections)
- Floor 2 (110.51, 350.38) → 0.0103 (5 connections)
- Floor 2 (111.51, 350.38) → 0.0103 (5 connections)

## Community detection

- Communities: **12**  |  Total cells: 488  |  Total area: ~488 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 57 | 57 |
| 1 | 51 | 51 |
| 2 | 56 | 56 |
| 3 | 26 | 26 |
| 4 | 17 | 17 |
| 5 | 25 | 25 |
| 6 | 36 | 36 |
| 7 | 28 | 28 |
| 8 | 63 | 63 |
| 9 | 46 | 46 |
| 10 | 45 | 45 |
| 11 | 38 | 38 |

## Visibility Graph Analysis (per floor)

| Floor | Viewpoints | min | max | mean |
|---|---|---|---|---|
| Floor 1 | 1993 | 477 | 1307 | 840.628 |
| Floor 2 | 1581 | 88 | 1363 | 894.645 |
| Floor 3 | 1660 | 54 | 1042 | 596.08 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
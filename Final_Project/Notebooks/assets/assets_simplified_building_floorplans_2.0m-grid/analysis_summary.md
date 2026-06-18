# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-18 15:47:20_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:\IAAC Local GIT Repositories\Graph ML - Environment\Final_Project\3D-Models\Marsella_3-Floor-Plans_SIMPLIFIED.obj |
| `GRID_SIZE` | 2 |
| `FLOOR_HEIGHT` | 30 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 2 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 4.0 |
| `n_stair_locations` | 58 |

## Geometry

- **Plan bounding box:** X [228.75, 361.25], Y [5.25, 28.75]  (132.50 × 23.50 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 804 | 884 |
| Floor 2 (Z=4) | 696 | 656 |
| Floor 3 (Z=8) | 864 | 884 |

## Building graph

- Nodes: **2424**  |  Edges: **4661**  |  Density: **0.00159**  |  Stair edges: **61**

## Minimum Spanning Tree

- Vertices: 2424  |  Edges: 2423  |  Density: 0.00083

## Cross-floor shortest path

- Length: **200.0**  |  Nodes: 73
  |  Simplified: 189.2 (5 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0008 | 0.0025 | 0.0016 | 0.0002 | [0.001591, 0.001581, 0.001588] |
| Closeness | 0.0219 | 0.0467 | 0.0350 | 0.0058 | [0.034639, 0.036474, 0.034351] |
| Betweenness | 0.0000 | 0.1399 | 0.0117 | 0.0100 | [0.010128, 0.014118, 0.011557] |

**Top 5 degree hubs:**

- Floor 2 (246.75, 23.25) → 0.0025 (6 connections)
- Floor 2 (298.75, 23.25) → 0.0025 (6 connections)
- Floor 2 (340.75, 23.25) → 0.0025 (6 connections)
- Floor 1 (354.75, 9.25) → 0.0021 (5 connections)
- Floor 1 (230.75, 11.25) → 0.0021 (5 connections)

## Community detection

- Communities: **19**  |  Total cells: 2424  |  Total area: ~9696 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 207 | 828 |
| 1 | 89 | 356 |
| 2 | 116 | 464 |
| 3 | 109 | 436 |
| 4 | 156 | 624 |
| 5 | 213 | 852 |
| 6 | 156 | 624 |
| 7 | 93 | 372 |
| 8 | 130 | 520 |
| 9 | 93 | 372 |
| 10 | 95 | 380 |
| 11 | 84 | 336 |
| 12 | 94 | 376 |
| 13 | 112 | 448 |
| 14 | 169 | 676 |
| 15 | 163 | 652 |
| 16 | 101 | 404 |
| 17 | 120 | 480 |
| 18 | 124 | 496 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
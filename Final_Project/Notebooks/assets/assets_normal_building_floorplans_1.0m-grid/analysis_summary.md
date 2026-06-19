# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-19 07:09:42_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:\IAAC Local GIT Repositories\Graph ML - Environment\Final_Project\3D-Models\Marsella_3-Floor-Plans.obj |
| `GRID_SIZE` | 1 |
| `FLOOR_HEIGHT` | 30 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 1 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 4.0 |
| `n_stair_locations` | 57 |

## Geometry

- **Plan bounding box:** X [121.67, 260.79], Y [333.37, 357.48]  (139.12 × 24.10 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 2419 | 2999 |
| Floor 2 (Z=4) | 1336 | 2508 |
| Floor 3 (Z=8) | 2290 | 3300 |

## Building graph

- Nodes: **8807**  |  Edges: **16319**  |  Density: **0.00042**  |  Stair edges: **60**

## Minimum Spanning Tree

- Vertices: 8807  |  Edges: 8806  |  Density: 0.00023

## Cross-floor shortest path

- Length: **215.0**  |  Nodes: 158
  |  Simplified: 201.2 (6 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0001 | 0.0006 | 0.0004 | 0.0001 | [0.000418, 0.000422, 0.000422] |
| Closeness | 0.0107 | 0.0226 | 0.0166 | 0.0028 | [0.015745, 0.017564, 0.016656] |
| Betweenness | 0.0000 | 0.1128 | 0.0069 | 0.0114 | [0.002799, 0.010355, 0.008066] |

**Top 5 degree hubs:**

- Floor 1 (125.67, 340.37) → 0.0006 (5 connections)
- Floor 1 (126.67, 340.37) → 0.0006 (5 connections)
- Floor 1 (133.67, 340.37) → 0.0006 (5 connections)
- Floor 1 (134.67, 340.37) → 0.0006 (5 connections)
- Floor 1 (142.67, 340.37) → 0.0006 (5 connections)

## Community detection

- Communities: **40**  |  Total cells: 8807  |  Total area: ~8807 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 172 | 172 |
| 1 | 326 | 326 |
| 2 | 229 | 229 |
| 3 | 258 | 258 |
| 4 | 360 | 360 |
| 5 | 235 | 235 |
| 6 | 275 | 275 |
| 7 | 252 | 252 |
| 8 | 376 | 376 |
| 9 | 336 | 336 |
| 10 | 210 | 210 |
| 11 | 196 | 196 |
| 12 | 181 | 181 |
| 13 | 160 | 160 |
| 14 | 172 | 172 |
| 15 | 86 | 86 |
| 16 | 157 | 157 |
| 17 | 153 | 153 |
| 18 | 303 | 303 |
| 19 | 296 | 296 |
| 20 | 336 | 336 |
| 21 | 318 | 318 |
| 22 | 49 | 49 |
| 23 | 42 | 42 |
| 24 | 33 | 33 |
| 25 | 312 | 312 |
| 26 | 364 | 364 |
| 27 | 323 | 323 |
| 28 | 196 | 196 |
| 29 | 172 | 172 |
| 30 | 268 | 268 |
| 31 | 344 | 344 |
| 32 | 129 | 129 |
| 33 | 188 | 188 |
| 34 | 224 | 224 |
| 35 | 288 | 288 |
| 36 | 136 | 136 |
| 37 | 124 | 124 |
| 38 | 120 | 120 |
| 39 | 108 | 108 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
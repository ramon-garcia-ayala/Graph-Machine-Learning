# Analysis Summary — Marsella 3-Apartment Section

_Generated: 2026-06-18 10:39:13_

Spatial Intelligence analysis of a 3-apartment section of the Unite d'Habitation (Marseille).

## Parameters

| Parameter | Value |
|---|---|
| `OBJ_PATH` | E:/IAAC Local GIT Repositories/Graph ML - Environment/Final_Project\3D-Models\Marsella_3-Apartments.obj |
| `GRID_SIZE` | 0.12 |
| `FLOOR_HEIGHT` | 10.0 |
| `FLOOR_LEVELS` | [0, 4, 8] |
| `VGA_GRID_SIZE` | 0.3 |
| `VIS_SAMPLES` | 12 |
| `ISO_STEP` | 0.12 |
| `n_stair_locations` | 4 |

## Geometry

- **Plan bounding box:** X [106.51, 114.97], Y [333.38, 357.48]  (8.46 × 24.10 units)

| Floor | Faces | Navigable nodes |
|---|---|---|
| Floor 1 (Z=0) | 187 | 13101 |
| Floor 2 (Z=4) | 88 | 10185 |
| Floor 3 (Z=8) | 191 | 10025 |

## Building graph

- Nodes: **33311**  |  Edges: **64135**  |  Density: **0.00012**  |  Stair edges: **4**

## Minimum Spanning Tree

- Vertices: 33311  |  Edges: 33310  |  Density: 0.00006

## Cross-floor shortest path

- Length: **50.3**  |  Nodes: 255
  |  Simplified: 41.1 (6 waypoints)

## Centrality metrics

| Metric | min | max | mean | std | per-floor mean |
|---|---|---|---|---|---|
| Degree | 0.0001 | 0.0001 | 0.0001 | 0.0000 | [0.000116, 0.000116, 0.000115] |
| Closeness | 0.0035 | 0.0087 | 0.0057 | 0.0012 | [0.005219, 0.006901, 0.005008] |
| Betweenness | 0.0000 | 0.3208 | 0.0055 | 0.0216 | [0.003986, 0.008299, 0.004697] |

**Top 5 degree hubs:**

- Floor 1 (110.11, 340.82) → 0.0001 (5 connections)
- Floor 1 (111.31, 340.82) → 0.0001 (5 connections)
- Floor 2 (110.23, 350.06) → 0.0001 (5 connections)
- Floor 2 (111.43, 350.06) → 0.0001 (5 connections)
- Floor 1 (106.75, 333.5) → 0.0001 (4 connections)

## Community detection

- Communities: **60**  |  Total cells: 33311  |  Total area: ~479.678 m²

| Community | Cells | Area m² |
|---|---|---|
| 0 | 993 | 14.299 |
| 1 | 1015 | 14.616 |
| 2 | 431 | 6.206 |
| 3 | 1189 | 17.122 |
| 4 | 718 | 10.339 |
| 5 | 636 | 9.158 |
| 6 | 537 | 7.733 |
| 7 | 433 | 6.235 |
| 8 | 320 | 4.608 |
| 9 | 609 | 8.77 |
| 10 | 581 | 8.366 |
| 11 | 321 | 4.622 |
| 12 | 106 | 1.526 |
| 13 | 501 | 7.214 |
| 14 | 635 | 9.144 |
| 15 | 515 | 7.416 |
| 16 | 801 | 11.534 |
| 17 | 631 | 9.086 |
| 18 | 487 | 7.013 |
| 19 | 376 | 5.414 |
| 20 | 718 | 10.339 |
| 21 | 571 | 8.222 |
| 22 | 636 | 9.158 |
| 23 | 640 | 9.216 |
| 24 | 566 | 8.15 |
| 25 | 510 | 7.344 |
| 26 | 877 | 12.629 |
| 27 | 180 | 2.592 |
| 28 | 424 | 6.106 |
| 29 | 424 | 6.106 |
| 30 | 259 | 3.73 |
| 31 | 268 | 3.859 |
| 32 | 707 | 10.181 |
| 33 | 558 | 8.035 |
| 34 | 449 | 6.466 |
| 35 | 294 | 4.234 |
| 36 | 714 | 10.282 |
| 37 | 700 | 10.08 |
| 38 | 1009 | 14.53 |
| 39 | 971 | 13.982 |
| 40 | 620 | 8.928 |
| 41 | 616 | 8.87 |
| 42 | 629 | 9.058 |
| 43 | 522 | 7.517 |
| 44 | 642 | 9.245 |
| 45 | 574 | 8.266 |
| 46 | 549 | 7.906 |
| 47 | 492 | 7.085 |
| 48 | 228 | 3.283 |
| 49 | 225 | 3.24 |
| 50 | 208 | 2.995 |
| 51 | 225 | 3.24 |
| 52 | 650 | 9.36 |
| 53 | 582 | 8.381 |
| 54 | 484 | 6.97 |
| 55 | 292 | 4.205 |
| 56 | 470 | 6.768 |
| 57 | 277 | 3.989 |
| 58 | 870 | 12.528 |
| 59 | 846 | 12.182 |

## Visibility Graph Analysis (per floor)

| Floor | Viewpoints | min | max | mean |
|---|---|---|---|---|
| Floor 1 | 1993 | 477 | 1307 | 840.628 |
| Floor 2 | 1581 | 88 | 1363 | 894.645 |
| Floor 3 | 1660 | 54 | 1042 | 596.08 |

---
_Generated automatically by section 22 of the notebook. Community colours/partition are stochastic and may differ between runs._
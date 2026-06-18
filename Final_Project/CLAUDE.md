# Final Project — Multi-Floor Spatial Intelligence (Unité d'Habitation, Marseille)

## Project overview

Spatial Intelligence analysis of three stacked floor plans from Le Corbusier's *Unité d'Habitation* (Marseille) using **topologicpy** and the Session-03 / Assignment-02 workflows. The key distinction from Assignment-02 is that all metrics are computed on a **single connected building graph** (all three floors joined through stair nodes), not per floor in isolation.

Two notebooks exist: the **full-building** analysis (`Updated_NB_…`) and a **focused apartment-section** analysis (`NB_Marsella_Apartments_Section`) that runs on a smaller OBJ with a 0.2 m grid.

## Folder structure

```
Final_Project/
├── 3D-Models/
│   ├── Marsella_3-Floor-Plans.obj          ← full building (3 floor plans)
│   ├── Marsella_3-Apartments.obj           ← small section (3 apartments, 3 floors)
│   ├── La Cité Radieuse_CellComplex.3dm    ← Rhino reference model
│   └── La Cité Radieuse_Surface Lower Floor.3dm
├── Notebooks/
│   ├── Spatial Intelligence/
│   │   ├── Updated_NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb  ← full building
│   │   └── NB_Marsella_Apartments_Section.ipynb                       ← apartment section
│   └── assets/
│       └── assets_apartments_section/      ← outputs from the apartment-section notebook
├── Team_Notebooks/                          ← split for parallel team runs (full building)
│   ├── 01_Betweenness_Centrality.ipynb
│   ├── 02_Closeness_Centrality.ipynb
│   ├── 03_MST_Communities_Degree.ipynb
│   ├── 04_Path_Visibility_Isovist.ipynb
│   ├── 3D-Model/
│   │   └── Marsella_3-Floor-Plans.obj      ← model copy (self-contained)
│   ├── example_outputs/                    ← reference PNGs from a verified run
│   ├── outputs/                            ← where fresh runs save their PNGs
│   └── README.md
└── assets_new_notebooks/                   ← outputs from Updated_NB (full building)
```

`*.3dmbak` and `*.rhl` (Rhino backup/lock files) are **not tracked** in git.
`OLD_NB_*` files inside `Notebooks/Spatial Intelligence/` are git-ignored.

## Geometry facts

### Full building (`Marsella_3-Floor-Plans.obj`)
- Three 2D floor plans, flat in XY at **Z = 0, 4, 8**.
- Plan dimensions: roughly **139 × 24 units** (X × Y), `X ≈ [121.7, 260.8]`, `Y ≈ [333.4, 357.5]`.
- 57 stair connection points across two transition levels (Floor 3↔2 and Floor 2↔1).

### Apartment section (`Marsella_3-Apartments.obj`)
- Three stacked floor plans of a **small 3-apartment section** of the same building.
- Same Z-level convention: **Z = 0, 4, 8**.
- Only **4 stair connection points** (2 for Floor 3↔2, 2 for Floor 2↔1).
- Stair XY coordinates:
  - Floor 3↔2 (Z = 8): `(111.41043, 350.049)`, `(110.24082, 350.049)`
  - Floor 2↔1 (Z = 4): `(111.28613, 340.78751)`, `(110.11652, 340.78751)`

**Why not `Shell.ByFaces`:** levels Z = 0 and Z = 8 have dense/overlapping triangulation that causes `Shell.ByFaces` to fail. Only Z = 4 reconstructs cleanly. Both notebooks use **grid sampling + point-in-mesh** instead.

## Method (Therme Vals / instructor's approach)

1. Import OBJ → collect all triangulated faces → bin by Z centroid into three floors.
2. For each floor, lay a regular grid (`GRID_SIZE`) and keep only points inside the mesh (*navigable area*) using a vectorised barycentric point-in-triangle test.
3. Each valid point → a topologic vertex at `Z = floor_index × FLOOR_HEIGHT`.
4. Each valid point → a flat square display cell (`Face.ByWire`) at a stacked offset, used for the S03-style filled heatmaps.
5. Connect 4-neighbours within each floor with horizontal edges.
6. Snap each `STAIR_LOCATIONS` entry to the closest navigable node on each pair of adjacent floors → add vertical stair edges (`find_closest_node`).
7. `Graph.ByVerticesEdges(all_v, all_e)` → **combined building graph**.
8. Run all metrics on this single graph.

## Workflows in both notebooks

| Section | Workflow | Scope |
|---|---|---|
| 12 | Show combined 3D building graph | Visual (interactive 3D) |
| 13 | Minimum Spanning Tree | **Whole building** |
| 14 | Shortest Path (cross-floor + straightened) | **Whole building** |
| 15 | Degree Centrality (hub / dead-end stats) | **Whole building** |
| 16 | Closeness Centrality (Integration) | **Whole building** |
| 17 | Betweenness Centrality (Choice) | **Whole building** |
| 18 | Community Detection (area / count per community) | **Whole building** |
| 19 | Visibility Heatmap / VGA | Per floor |
| 20 | Isovist Analysis (geometric visibility polygons) | Per floor (Z=4 only if Shell succeeds) |
| 21 | Building-wide Summary | **Whole building** |

## Key parameters

### Full-building notebook (`Updated_NB_Marsella_MultiFloor_Spatial_Intelligence`)

| Parameter | Value | Effect |
|---|---|---|
| `OBJ_PATH` | `Marsella_3-Floor-Plans.obj` | Full building geometry |
| `GRID_SIZE` | `0.5` | ~40 000 nodes; walls visible; use Team_Notebooks for this size |
| `STAIR_LOCATIONS` | 57 entries | XY coordinates of all stairs |
| `VGA_GRID_SIZE` | `5.0` | Visibility viewpoint spacing (coarser than analysis grid) |
| `ISO_STEP` | `5.0` | Isovist viewpoint spacing |
| `ASSETS_DIR` | `assets_new_notebooks/` | Output PNGs |

### Apartment-section notebook (`NB_Marsella_Apartments_Section`)

| Parameter | Value | Effect |
|---|---|---|
| `OBJ_PATH` | `Marsella_3-Apartments.obj` | Small 3-apartment section |
| `GRID_SIZE` | `0.2` | Fine 0.2 m grid; manageable node count for small section |
| `STAIR_LOCATIONS` | 4 entries | 2 for Floor 3↔2, 2 for Floor 2↔1 |
| `VGA_GRID_SIZE` | `1.0` | Smaller spacing suited to the reduced area |
| `ISO_STEP` | `1.0` | Smaller spacing suited to the reduced area |
| `ASSETS_DIR` | `Notebooks/assets/assets_apartments_section/` | Output PNGs |

Both notebooks share: `renderer = "png"`, `INTERACTIVE_RENDERER = "browser"`, `FLOOR_HEIGHT = 15.0`.

### Visualization fixes applied to the apartment-section notebook

The apartment section is geometrically much smaller than the full building, so several hardcoded parameters from the original were replaced with data-driven equivalents:

- **Floor plan figures (01, 02):** `width`/`height` are now computed from `UMIN/UMAX/VMIN/VMAX` using `px_pu` (pixels-per-unit) instead of fixed `width=1500`.
- **3D plots (03, 08, 10):** `scene_camera(eye=[2.0, 2.0, 2.0])` added before `save_fig` to ensure all floors fit in the static PNG export.
- **Heatmaps (04-07, 09):** `camera=[0,0,6]` removed from `Topology.Show`; replaced with `scene_camera(eye=[0,0,1.5])` — plotly's standard normalised zoom that scales correctly regardless of model size.

### Stair connectivity format

Each `STAIR_LOCATIONS` entry controls **which floor pairs that stair connects**:

- `(X, Y)` — connects **all** adjacent floors (1↔2 *and* 2↔3).
- `(X, Y, [(floor_a, floor_b), ...])` — connects only the listed pairs. Floor indices: `0 = Floor 1`, `1 = Floor 2`, `2 = Floor 3`.

Every floor must be reached by at least one stair — otherwise it stays disconnected and centrality / shortest-path sections break (`"No path found"`).

## Python environment

The project uses the venv at `../.env/` (one level up from `Final_Project/`). Activate before running:

```powershell
.\.env\Scripts\Activate.ps1
```

**Note:** `nbconvert` is not installed in this venv. Run notebooks directly in **Jupyter / VS Code**, not via `jupyter nbconvert --execute`.

## Git workflow notes

- Always **wait for the notebook kernel to finish** (status bar shows idle) before running `git commit` on assets.
- `*.3dmbak` and `*.rhl` files should not be staged — they are Rhino auto-backups.
- `OLD_NB_*` notebooks are git-ignored; only `Updated_NB_*` and `NB_Marsella_Apartments_Section` are tracked.
- Community detection (`Graph.CommunityPartition`) is stochastic — community colours will vary between runs.

## Typical run time

| Notebook | `GRID_SIZE` | Approx. nodes | Estimated time |
|---|---|---|---|
| Apartment section | `0.2` | ~few thousand | minutes–1 h |
| Full building | `0.5` | ~40 000 | days (use Team_Notebooks) |
| Full building | `1.0` | ~8 800 | 1.5–3 h |
| Full building | `3.0` | ~1 012 | ~2.5 min |

### Team_Notebooks split (for full building at GRID_SIZE = 0.5)

| Notebook | Analysis | Estimated time |
|---|---|---|
| `01_Betweenness_Centrality` | Betweenness (Choice) | hours–day+ |
| `02_Closeness_Centrality` | Closeness (Integration) | ~10–20 h |
| `03_MST_Communities_Degree` | MST + Community + Degree | ~2–4 h |
| `04_Path_Visibility_Isovist` | 3D graph + Shortest Path + VGA + Isovist | ~1–2 h |

All four notebooks were smoke-tested end-to-end at `GRID_SIZE = 8.0` — all passed.

### WebGL note

`renderer = "png"` avoids VS Code's WebGL crash for all heatmap cells. Sections 12, 13, and 14 (3D building graph, MST, shortest-path) use `INTERACTIVE_RENDERER = "browser"`, which opens in the system browser to bypass the VS Code WebGL freeze while still providing a rotatable 3D figure. All three cells also call `save_fig` to write a static PNG.

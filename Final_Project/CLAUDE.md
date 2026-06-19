# Final Project — Multi-Floor Spatial Intelligence (Unité d'Habitation, Marseille)

## Project overview

Spatial Intelligence analysis of three stacked floor plans from Le Corbusier's *Unité d'Habitation* (Marseille) using **topologicpy** and the Session-03 / Assignment-02 workflows. The key distinction from Assignment-02 is that all metrics are computed on a **single connected building graph** (all three floors joined through stair nodes), not per floor in isolation.

Three active notebooks exist: the **full-building simplified** analysis (`Simplified_NB_…`), the **full-building original** analysis (`Updated_NB_…`), and a **focused apartment-section** analysis (`NB_Marsella_Apartments_Section`).

## Folder structure

```
Final_Project/
├── 3D-Models/
│   ├── Marsella_3-Floor-Plans.obj              ← original full building (3 floor plans)
│   ├── Marsella_3-Floor-Plans_SIMPLIFIED.obj   ← simplified full building geometry
│   ├── Marsella_3-Apartments.obj               ← small section (3 apartments, 3 floors)
│   ├── Point_tags.gh                           ← Grasshopper script for picking stair coords
│   ├── La Cité Radieuse_CellComplex.3dm        ← Rhino reference model
│   └── La Cité Radieuse_Surface Lower Floor.3dm
├── Notebooks/
│   ├── Spatial Intelligence/
│   │   ├── Simplified_NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb  ← simplified building
│   │   ├── Updated_NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb     ← original full building
│   │   └── NB_Marsella_Apartments_Section.ipynb                          ← apartment section
│   └── assets/
│       ├── assets_simplified_building_floorplans_8.0m-grid/  ← Simplified outputs (GRID_SIZE=8.0)
│       │   ├── 01_floor_plans.png          (vertical, black bg)
│       │   ├── 02_navigable_grids.png      (vertical, black bg)
│       │   ├── 03_building_graph_3d.png    (orthographic isometric, axes visible)
│       │   ├── 04–07_centrality_*.png      (show_face_heatmap, stacked vertical)
│       │   ├── 08_shortest_path_3d.png     (orthographic isometric)
│       │   ├── 09_visibility_isovist.png   (show_face_heatmap)
│       │   ├── 10_mst_3d.png              (orthographic isometric)
│       │   ├── 11_isovists_Floor_2.png     (isovist via Shell.ByFaces)
│       │   ├── analysis_summary.md
│       │   └── analysis_metadata.json
│       └── assets_apartments_section_0.12m-grid/  ← Apartment outputs (GRID_SIZE=0.12)
│           ├── 01_floor_plans.png          (horizontal, black bg)
│           ├── 02_navigable_grids.png      (horizontal, black bg)
│           ├── 03_building_graph_3d.png    (orthographic isometric)
│           ├── 04–07_centrality_*.png      (show_grid_heatmaps, 3 panels)
│           ├── 08_shortest_path_3d.png     (orthographic isometric)
│           ├── 09_visibility_isovist.png   (show_grid_heatmaps, 3 panels)
│           ├── 10_mst_3d.png              (orthographic isometric)
│           ├── 11_isovists_all_floors.png  (ray-casting, 3 panels)
│           ├── analysis_summary.md
│           └── analysis_metadata.json
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
├── assets_building_floorplans_v1.0/        ← outputs from original NB (first run)
└── assets_building_floorplans_v2.0/        ← outputs from Updated_NB (improved run)
```

Assets folders are named with the grid size used in that run (e.g. `_0.12m-grid`, `_8.0m-grid`). When re-running at a new `GRID_SIZE`, update `ASSETS_DIR` in the config cell to match.

`*.3dmbak` and `*.rhl` (Rhino backup/lock files) are **not tracked** in git.
`OLD_NB_*` files inside `Notebooks/Spatial Intelligence/` are git-ignored.

## Geometry facts

### Original full building (`Marsella_3-Floor-Plans.obj`)
- Three 2D floor plans, flat in XY at **Z = 0, 4, 8**.
- Plan dimensions: roughly **139 × 24 units** (X × Y), `X ≈ [121.7, 260.8]`, `Y ≈ [333.4, 357.5]`.
- Used by `Updated_NB_…` and the Team_Notebooks.

### Simplified full building (`Marsella_3-Floor-Plans_SIMPLIFIED.obj`)
- Three 2D floor plans of the same building, simplified mesh (2 644 verts vs 6 431).
- **Different coordinate system** from the original: `X ≈ [228.8, 361.2]`, `Y ≈ [5.2, 28.8]`.
- Floor levels: Y_obj ≈ **1, 4, 8** (not 0 — but FLOOR_LEVELS=[0,4,8] bins correctly via nearest-Z).
- Used by `Simplified_NB_…`. Stair coordinates must be picked in this coordinate system.
- 58 stair locations: 24 for Floor 3↔2 (y≈22), 31 for Floor 1↔2 (y≈12), 3 connecting all floors (y≈24).
- Stair picking script: `Point_tags.gh` (Grasshopper).

### Apartment section (`Marsella_3-Apartments.obj`)
- Three stacked floor plans of a **small 3-apartment section**.
- Same Z-level convention: **Z = 0, 4, 8**. Plan coords: `X ≈ [106.5, 115.0]`, `Y ≈ [333.4, 357.5]`.
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
| 20 | Isovist Analysis (ray-casting, all three floors) | Per floor |
| 21 | Building-wide Summary | **Whole building** |
| 22 | Export analysis summary (`analysis_summary.md` + `analysis_metadata.json`) | **Whole building** |

## Key parameters

### Simplified-building notebook (`Simplified_NB_Marsella_MultiFloor_Spatial_Intelligence`)

| Parameter | Value | Effect |
|---|---|---|
| `OBJ_PATH` | `Marsella_3-Floor-Plans_SIMPLIFIED.obj` | Simplified full building geometry |
| `GRID_SIZE` | `0.7` | Current value; 8.0 used for smoke tests |
| `STAIR_LOCATIONS` | 58 entries | 24 for 3↔2, 31 for 1↔2, 3 for all floors |
| `VGA_GRID_SIZE` | `5.0` | Coarse spacing (O(n²) cost) |
| `ISO_STEP` | `5.0` | Isovist viewpoint spacing |
| `ASSETS_DIR` | `Notebooks/assets/assets_simplified_building_floorplans_{grid}/` | Output PNGs |
| `INTERACTIVE_RENDERER` | `"png"` | Static PNG only (no browser popup) |

### Original full-building notebook (`Updated_NB_Marsella_MultiFloor_Spatial_Intelligence`)

| Parameter | Value | Effect |
|---|---|---|
| `OBJ_PATH` | `Marsella_3-Floor-Plans.obj` | Original full building geometry |
| `GRID_SIZE` | `0.5` | ~40 000 nodes; use Team_Notebooks for this size |
| `STAIR_LOCATIONS` | 57 entries | Original XY coordinates (Y≈333-357 coordinate system) |
| `VGA_GRID_SIZE` | `5.0` | Visibility viewpoint spacing |
| `ISO_STEP` | `5.0` | Isovist viewpoint spacing |
| `ASSETS_DIR` | `Notebooks/assets/assets_building_floorplans_v2.0/` | Output PNGs |

### Apartment-section notebook (`NB_Marsella_Apartments_Section`)

| Parameter | Value | Effect |
|---|---|---|
| `OBJ_PATH` | `Marsella_3-Apartments.obj` | Small 3-apartment section |
| `GRID_SIZE` | `0.12` | Current value (0.3 is faster for iteration) |
| `STAIR_LOCATIONS` | 4 entries | 2 for Floor 3↔2, 2 for Floor 2↔1 |
| `VGA_GRID_SIZE` | `0.3` | Fine spacing for small section |
| `ISO_STEP` | `3.0` | Isovist viewpoint spacing |
| `ASSETS_DIR` | `Notebooks/assets/assets_apartments_section_{grid}/` | Output PNGs |

All notebooks share: `renderer = "png"`, `FLOOR_HEIGHT = 15.0`, `FLOOR_LEVELS = [0, 4, 8]`.

### Visualization design

**Shared across all notebooks (black background everywhere):**
- All figures use `paper_bgcolor="black"` / `plot_bgcolor="black"` / `backgroundColor="black"`.
- White axis text, titles, and tick labels; faint white grid lines `rgba(255,255,255,0.10-0.15)`.

**3D plots (03 building graph, 08 shortest path, 10 MST) — all notebooks:**
- `projection=dict(type="orthographic")`, `eye=(1.4, 1.4, 1.4)` — isometric view, full building fits in frame.
- `aspectmode="data"` so floor proportions are preserved.
- Axes visible with titles `x`, `y`, `z (floor stack)`.

**Floor plans (01) and navigable grids (02):**
- *Simplified & Updated notebooks:* **vertical stack** (`rows=N, cols=1`) — correct for the long horizontal plans.
- *Apartment-section notebook:* **horizontal panels** (`rows=1, cols=N`) — correct for tall narrow plans.

**Centrality / community heatmaps (04–07):**
- *Apartment-section:* `show_grid_heatmaps` → `go.Heatmap` 2D raster, 3 side-by-side panels, real plan coordinates on axes.
- *Simplified & Updated:* `show_face_heatmap` → `Topology.Show` 3D faces, vertical stack, `scene_camera eye=[0,0,1.5]`.

**VGA heatmap (09):**
- *Apartment-section:* `show_grid_heatmaps` path with `(xs, ys, deg)` per floor.
- *Simplified & Updated:* `show_face_heatmap` path with display cell faces.

**Isovist analysis (11):**
- *Apartment-section:* numeric ray-casting over the navigable cell mask — works on all 3 floors. Output: `11_isovists_all_floors.png`.
- *Simplified & Updated:* `Face.Isovist` via `Shell.ByFaces` — only works on Floor 2 (Z=4); others skipped. Output: `11_isovists_Floor_2.png`.

**Section 22 — analysis summary export (all notebooks):**
- Writes `analysis_summary.md` and `analysis_metadata.json` to `ASSETS_DIR`.
- Collects: parameters, geometry, graph stats, MST, shortest path, centralities + top-5 hubs, communities, VGA.
- Uses `globals()` guards — safe to run after partial execution.

**Section 23 — git commit & push (all notebooks):**
- Stages the notebook + `ASSETS_DIR`, commits with timestamp message, pushes `origin main`.

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
- `OLD_NB_*` notebooks are git-ignored; `Simplified_NB_*`, `Updated_NB_*` and `NB_Marsella_Apartments_Section` are tracked.
- Community detection (`Graph.CommunityPartition`) is stochastic — community colours will vary between runs.

## Typical run time

| Notebook | `GRID_SIZE` | Approx. nodes | Estimated time |
|---|---|---|---|
| Apartment section | `0.12` | ~15 000 | 8–18 h (betweenness dominates) |
| Apartment section | `0.2` | ~4 000 | 1–1.5 h |
| Apartment section | `0.3` | ~1 800 | 10–25 min |
| Simplified building | `0.7` | ~few thousand | 30–90 min |
| Simplified building | `8.0` | ~100–150 | < 1 min (smoke test) |
| Full building (original) | `0.5` | ~40 000 | days (use Team_Notebooks) |
| Full building (original) | `1.0` | ~8 800 | 1.5–3 h |
| Full building (original) | `3.0` | ~1 012 | ~2.5 min |

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

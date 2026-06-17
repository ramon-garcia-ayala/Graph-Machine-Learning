# Final Project — Multi-Floor Spatial Intelligence (Unité d'Habitation, Marseille)

## Project overview

Spatial Intelligence analysis of three stacked floor plans from Le Corbusier's *Unité d'Habitation* (Marseille) using **topologicpy** and the Session-03 / Assignment-02 workflows. The key distinction from Assignment-02 is that all metrics are computed on a **single connected building graph** (all three floors joined through stair nodes), not per floor in isolation.

## Folder structure

```
Final_Project/
├── 3D-Models/
│   ├── Marsella_3-Floor-Plans.obj          ← source geometry (3 floor plans)
│   ├── La Cité Radieuse_CellComplex.3dm    ← Rhino reference model
│   └── La Cité Radieuse_Surface Lower Floor.3dm
├── Notebooks/
│   └── NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb   ← original notebook
├── Spatial Intelligence/
│   └── Updated_NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb  ← extended notebook
├── Team_Notebooks/                          ← split for parallel team runs
│   ├── 01_Betweenness_Centrality.ipynb
│   ├── 02_Closeness_Centrality.ipynb
│   ├── 03_MST_Communities_Degree.ipynb
│   ├── 04_Path_Visibility_Isovist.ipynb
│   ├── 3D-Model/
│   │   └── Marsella_3-Floor-Plans.obj      ← model copy (self-contained)
│   ├── example_outputs/                    ← reference PNGs from a verified run
│   ├── outputs/                            ← where fresh runs save their PNGs
│   └── README.md
└── assets/
    ├── 01_floor_plans.png
    ├── 02_navigable_grids.png
    ├── 03_building_graph_3d.png
    ├── 04_degree_centrality.png
    ├── 05_closeness_centrality.png
    ├── 06_betweenness_centrality.png
    ├── 07_communities.png
    ├── 08_shortest_path_3d.png
    ├── 09_visibility_isovist.png
    ├── 10_mst_3d.png
    └── 11_isovists_Floor_*.png
```

`*.3dmbak` and `*.rhl` (Rhino backup/lock files) are **not tracked** in git.

## Geometry facts

- **Source:** `Marsella_3-Floor-Plans.obj` — a single OBJ with three 2D floor plans.
- **After `Topology.ByOBJPath` (Z-up convention):** the three plans are flat in the XY plane at three discrete Z levels: **Z = 0, Z = 4, Z = 8**.
- **Plan dimensions:** roughly 139 × 24 units (X × Y), with `X ≈ [121.7, 260.8]`, `Y ≈ [333.4, 357.5]`.
- **Why not `Shell.ByFaces`:** levels Z = 0 and Z = 8 have dense/overlapping triangulation that causes `Shell.ByFaces` to fail. Only Z = 4 reconstructs cleanly. This is why the notebook uses **grid sampling + point-in-mesh** instead.

## Method (Therme Vals / instructor's approach)

1. Import OBJ → collect all triangulated faces → bin by Z centroid into three floors.
2. For each floor, lay a regular grid (`GRID_SIZE`) and keep only points inside the mesh (*navigable area*) using a vectorised barycentric point-in-triangle test.
3. Each valid point → a topologic vertex at `Z = floor_index × FLOOR_HEIGHT`.
4. Each valid point → a flat square display cell (`Face.ByWire`) at a stacked offset, used for the S03-style filled heatmaps.
5. Connect 4-neighbours within each floor with horizontal edges.
6. Snap each `STAIR_LOCATIONS` entry to the closest navigable node on each pair of adjacent floors → add vertical stair edges (`find_closest_node`).
7. `Graph.ByVerticesEdges(all_v, all_e)` → **combined building graph**.
8. Run all metrics on this single graph.

## Workflows in the notebook

The table below reflects the **updated notebook** (`Spatial Intelligence/Updated_NB_…`). The original `Notebooks/NB_…` stops at section 19 without MST or Isovists.

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

**Ordering rationale:** MST (13) shows the structural backbone before navigating it; Shortest Path (14) validates stair connectivity interactively; centralities (15–17) run on the full graph; Community (18) groups the result; Visibility (19–20) is independent of the graph metrics.

## Visual export format

Heatmaps (sections 13–18) use a **2D raster renderer** (`go.Heatmap`) instead of `Topology.Show` 3D faces. Each metric value is written into a numpy matrix (one cell per grid node, `NaN` for walls/holes), then rendered with a Plotly Heatmap and exported via kaleido. Three floors are stacked vertically with a small gap between them.

**Why 2D instead of 3D:** `Topology.Show` with 8 000+ faces requires WebGL. VS Code's notebook WebGL context crashes under that load (`"WebGL is not supported"`). The 2D renderer produces identical-looking filled-cell heatmaps without any WebGL dependency.

## Key parameters (Section 3 — Configuration)

| Parameter | Current value | Effect |
|---|---|---|
| `renderer` | `"png"` | Plotly render target for all heatmap cells. `"png"` uses kaleido (no WebGL, works in VS Code). |
| `INTERACTIVE_RENDERER` | `"browser"` | Render target for rotatable 3D-graph cells (sections 12, 13, 14). `"browser"` opens in your default web browser, bypassing VS Code's WebGL crash. Team_Notebooks use `"png"` for unattended runs. |
| `GRID_SIZE` | `0.5` | Analysis grid spacing. **Current value produces ~40 000 nodes and makes walls visible** at the cost of very long run times. See timing table below. |
| `FLOOR_HEIGHT` | `15.0` | Vertical gap between floors in the 3D graph (visual only). |
| `STAIR_LOCATIONS` | 57 entries | XY plan coordinates of the stairs (+ optional floor-pair list). Run section 8 to see the navigable grid and locate them. See *Stair connectivity format* below. |
| `VGA_GRID_SIZE` | `5.0` | Visibility viewpoint spacing (section 19). Coarser than `GRID_SIZE` by design. `compute_visibility` is O(n²) in viewpoints — keep above 4.0 for reasonable run times. |
| `VIS_SAMPLES` | `12` | Samples along each sightline for the occlusion test. |
| `ISO_STEP` | `5.0` | Isovist viewpoint spacing (section 20). `Face.Isovist` is slow; keep sparse. |

### Stair connectivity format

Each `STAIR_LOCATIONS` entry controls **which floor pairs that stair connects**. Two forms are accepted:

- `(X, Y)` — connects **all** adjacent floors (1↔2 *and* 2↔3). Original behaviour.
- `(X, Y, [(floor_a, floor_b), ...])` — connects only the listed pairs. Floor indices are `0 = Floor 1`, `1 = Floor 2`, `2 = Floor 3`.

```python
STAIR_LOCATIONS = [
    (155.0, 345.0, [(0, 1), (1, 2)]),   # full vertical stair: 1↔2 and 2↔3
    (205.0, 345.0, [(0, 1)]),           # only Floor 1 ↔ Floor 2
    (245.0, 345.0, [(1, 2)]),           # only Floor 2 ↔ Floor 3
    (180.0, 345.0, [(0, 2)]),           # Floor 1 ↔ Floor 3 directly (skips Floor 2)
]
```

Each pair becomes one direct vertical edge between the closest navigable node on each floor (it does **not** pass through intermediate floors). **Every floor must be reached by at least one stair**, otherwise it stays disconnected and the centrality / shortest-path sections (15–18) break (`"No path found"`). Section 10 (cell `97ded8bd`) reads these pairs; Section 3 (cell `7e3f6b5b`) defines them.

## Python environment

The project uses the venv at `../env/` (one level up from `Final_Project/`). Activate before running:

```powershell
.\.env\Scripts\Activate.ps1
```

**Note:** `nbconvert` is not installed in this venv. Run the notebook directly in **Jupyter / VS Code**, not via `jupyter nbconvert --execute`.

## Git workflow notes

- Always **wait for the notebook kernel to finish** (status bar shows idle) before running `git commit` on assets. Committing mid-run will record partially generated `assets/` as deletions.
- `*.3dmbak` and `*.rhl` files should not be staged — they are Rhino auto-backups.
- Community detection (`Graph.CommunityPartition`) is stochastic — the community colours will vary between runs; the image in `assets/07_communities.png` reflects one particular run.

## Typical run time

| `GRID_SIZE` | Nodes | Total time (all sections) | Notes |
|---|---|---|---|
| `8.0` | ~158 | <1 min | Smoke-test only |
| `4.0` | ~640 | ~30–60 min | Fast iteration |
| `3.0` | ~1 012 | ~2.5 min | — |
| `2.0` | ~2 300 | ~5–8 min | — |
| `1.0` | ~8 800 | ~1.5–3 hours | — |
| `0.5` | ~40 000 | **days (split across team)** | Walls visible; use Team_Notebooks |

First run is slower because kaleido (image export) starts a Chromium subprocess.

### Team_Notebooks split (for GRID_SIZE = 0.5)

The workflow is split into 4 self-contained notebooks under `Team_Notebooks/` so each team member can run one analysis in parallel on their own machine. Each notebook has its own copy of the OBJ model, writes PNGs to its local `outputs/`, and has `example_outputs/` as reference.

| Notebook | Analysis | Estimated time |
|---|---|---|
| `01_Betweenness_Centrality` | Betweenness (Choice) | hours–day+ |
| `02_Closeness_Centrality` | Closeness (Integration) | ~10–20 h |
| `03_MST_Communities_Degree` | MST + Community + Degree | ~2–4 h |
| `04_Path_Visibility_Isovist` | 3D graph + Shortest Path + VGA + Isovist | ~1–2 h |

All four notebooks were smoke-tested end-to-end at `GRID_SIZE = 8.0` — all passed.

### WebGL note

`renderer = "png"` avoids VS Code's WebGL crash for all heatmap cells. With `GRID_SIZE = 1.0` (~8 800 cells) the old `Topology.Show` 3D path crashed VS Code with *"WebGL is not supported"*. The 2D `go.Heatmap` path (sections 14–18) has no such limit.

Sections 12, 13, and 14 (3D building graph, MST, shortest-path) use `Topology.Show` or `go.Scatter3d` + `INTERACTIVE_RENDERER = "browser"`, which opens in the system browser instead of the VS Code webview. This avoids the VS Code WebGL freeze while still providing a fully rotatable/zoomable 3D figure. All three cells also call `save_fig` to write a static PNG for the report.

**Minimum cells needed to run section 19 (Visibility Heatmap) independently:** steps 1 (imports), 3 (config), 4 (utility functions), 5 (OBJ import). Grid sampling, graph building, and centrality sections (7–18) are not needed.

**Minimum cells needed to run section 20 (Isovist Analysis) independently:** same as section 19 — steps 1, 3, 4, 5. The isovist cell rebuilds its own floor faces from `floor_faces` (populated in step 5).

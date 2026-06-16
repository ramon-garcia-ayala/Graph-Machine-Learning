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
│   └── NB_Marsella_MultiFloor_Spatial_Intelligence.ipynb
└── assets/
    ├── 01_floor_plans.png
    ├── 02_navigable_grids.png
    ├── 03_building_graph_3d.png
    ├── 04_degree_centrality.png
    ├── 05_closeness_centrality.png
    ├── 06_betweenness_centrality.png
    ├── 07_communities.png
    ├── 08_shortest_path_3d.png
    └── 09_visibility_isovist.png
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

| Section | Workflow | Scope |
|---|---|---|
| 13 | Degree Centrality | **Whole building** |
| 14 | Closeness Centrality (Integration) | **Whole building** |
| 15 | Betweenness Centrality (Choice) | **Whole building** |
| 16 | Community Detection | **Whole building** |
| 17 | Shortest Path (cross-floor) | **Whole building** |
| 18 | Visibility / Isovist (VGA) | Per floor (visibility doesn't cross slabs) |

## Visual export format

Heatmaps (sections 13–18) use a **2D raster renderer** (`go.Heatmap`) instead of `Topology.Show` 3D faces. Each metric value is written into a numpy matrix (one cell per grid node, `NaN` for walls/holes), then rendered with a Plotly Heatmap and exported via kaleido. Three floors are stacked vertically with a small gap between them.

**Why 2D instead of 3D:** `Topology.Show` with 8 000+ faces requires WebGL. VS Code's notebook WebGL context crashes under that load (`"WebGL is not supported"`). The 2D renderer produces identical-looking filled-cell heatmaps without any WebGL dependency.

## Key parameters (Section 3 — Configuration)

| Parameter | Default | Effect |
|---|---|---|
| `renderer` | `"png"` | Plotly render target. `"png"` uses kaleido (no WebGL, works in VS Code). Change to `"browser"` for interactive figures. |
| `GRID_SIZE` | `1.0` | Analysis grid spacing. Lower = finer resolution, slower. `2.0` → ~3–4 min total. |
| `FLOOR_HEIGHT` | `15.0` | Vertical gap between floors in the 3D graph (visual only). |
| `STAIR_LOCATIONS` | 3 points at Y≈345 | XY plan coordinates of the stairs (+ optional floor-pair list). **Edit these to match your actual stairs.** Run section 8 first to see the navigable grid and locate them. See *Stair connectivity format* below. |
| `VGA_GRID_SIZE` | `8.0` | Visibility viewpoint spacing (section 18). Coarser than `GRID_SIZE` by design. |
| `VIS_SAMPLES` | `12` | Samples along each sightline for the occlusion test. |

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

Each pair becomes one direct vertical edge between the closest navigable node on each floor (it does **not** pass through intermediate floors). **Every floor must be reached by at least one stair**, otherwise it stays disconnected and the centrality / shortest-path sections (14–17) break (`"No path found"`). Section 10 (cell `97ded8bd`) reads these pairs; Section 3 (cell `7e3f6b5b`) defines them.

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

| `GRID_SIZE` | Nodes | Total time (all sections) |
|---|---|---|
| `3.0` | ~1 012 | ~2.5 min |
| `2.0` | ~2 300 | ~5–8 min |
| `1.0` | ~8 800 | ~1.5–3 hours |

First run is slower because kaleido (image export) starts a Chromium subprocess.

### WebGL note

`renderer = "png"` avoids VS Code's WebGL crash. With `GRID_SIZE = 1.0` (~8 800 cells) the old `Topology.Show` 3D path crashed VS Code with *"WebGL is not supported"*. The 2D `go.Heatmap` path (sections 13–18) has no such limit. Sections 12 and 17 still use `Topology.Show` for the 3D building graph and shortest-path visualisation; these are lighter (graph edges, not filled faces) and have not caused crashes.

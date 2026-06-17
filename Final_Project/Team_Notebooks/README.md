# Team Notebooks — Multi-Floor Spatial Intelligence (Marsella / Unité d'Habitation)

Self-contained split of the Spatial Intelligence workflow into **4 notebooks**, one per team member, so the heavy `GRID_SIZE = 0.5` analyses can run in parallel on different machines and be left running for hours.

Everything needed lives in **this folder** — the 3D model and the output folder included. No external paths.

```
Team_Notebooks/
├── 01_Betweenness_Centrality.ipynb
├── 02_Closeness_Centrality.ipynb
├── 03_MST_Communities_Degree.ipynb
├── 04_Path_Visibility_Isovist.ipynb
├── 3D-Model/
│   └── Marsella_3-Floor-Plans.obj  ← the model (read by every notebook)
├── outputs/                        ← all PNGs are saved here
└── README.md
```

## How it works

Each notebook starts with an **identical SETUP section** (imports → config → utilities → OBJ import → grid sampling → build the building graph). Because the grid sampling is deterministic, all four rebuild **exactly the same connected building graph** at `GRID_SIZE = 0.5`, so the results are consistent across machines. After SETUP, each notebook runs only its own analysis and saves its figures to `outputs/`.

## Assignment & expected runtime (@ `GRID_SIZE = 0.5`, ~40 000 nodes)

| Notebook | Owner | Analysis | Est. runtime | Output(s) |
|---|---|---|---|---|
| `01_Betweenness_Centrality.ipynb` | ______ | Betweenness (Choice) | **hours–day+** (heaviest, O(V²·E)) | `06_betweenness_centrality.png` |
| `02_Closeness_Centrality.ipynb` | ______ | Closeness (Integration) | **~10–20 h** (O(V²)) | `05_closeness_centrality.png` |
| `03_MST_Communities_Degree.ipynb` | ______ | MST + Community + Degree | **~2–4 h** | `10_mst_3d.png`, `07_communities.png`, `04_degree_centrality.png` |
| `04_Path_Visibility_Isovist.ipynb` | ______ | 3D graph + Shortest Path + VGA + Isovist | **~1–2 h** | `03_building_graph_3d.png`, `08_shortest_path_3d.png`, `09_visibility_isovist.png`, `11_isovists_Floor_*.png` |

> The graph build (SETUP section 11) alone takes **~30–60 min** at 0.5 in every notebook — it is unavoidable since every analysis needs the graph.

## How to run

1. Open the folder in VS Code / Jupyter so the notebook's working directory is **this folder** (the notebooks read `3D-Model/Marsella_3-Floor-Plans.obj` relative to `os.getcwd()`).
2. **Smoke-test first (recommended):** in the Configuration cell temporarily set `GRID_SIZE = 8.0`, *Run All* (~5 s end-to-end) to confirm everything works, then set it back to `0.5`.
3. *Run All* and leave it running. PNGs land in `outputs/`.

## If a centrality notebook does not finish / runs out of RAM

Betweenness and Closeness at ~40 000 nodes may exhaust memory or take more than a day. Fallback: raise `GRID_SIZE` (e.g. `1.0` → ~10 000 nodes, much faster, still high-resolution). **The whole team must use the same `GRID_SIZE`** for the final figures to be comparable.

## Notes

- 3D figures render as static PNG (`INTERACTIVE_RENDERER = "png"`) so nothing pops up during unattended runs. Set it to `"browser"` in the Config cell to rotate/zoom them.
- `Graph.CommunityPartition` is stochastic — community colours vary between runs.
- `VGA_GRID_SIZE` (notebook 4, section 19) and `ISO_STEP` (section 20) drive their own cost and are **independent of `GRID_SIZE`**.

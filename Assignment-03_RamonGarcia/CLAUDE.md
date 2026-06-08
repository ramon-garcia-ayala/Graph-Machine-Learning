# Assignment-03 — Building Graph + GML Classification

Pipeline que convierte un edificio modelado en Rhino en un grafo y lo clasifica con un
modelo de PyTorch Geometric, usando **topologicpy**.

## Flujo de trabajo

1. **Rhino** (`geometries/*.3dm`) → se exportan capas a OBJ.
2. **`notebooks/01. Creating BGR Graph.ipynb`** → construye el grafo y exporta el dataset CSV.
3. **`notebooks/S06-13 GML Graph Classification.ipynb`** → entrena el modelo (PyG) y lo guarda en `models/pyg_model.pt`. Phase 2 del mismo notebook predice datasets no vistos.
4. **`notebooks/02. Graph Classification of Unseen Data.ipynb`** → carga `pyg_model.pt` y predice sobre un dataset preparado.

## Estructura

| Ruta | Contenido |
|------|-----------|
| `geometries/obj_geometry_v2.0/` | OBJ **vigentes**: `ground.obj`, `columns.obj`, `offices.obj`, `core.obj` (los que usa el notebook 01) |
| `geometries/obj_geometry/` | OBJ antiguos (v1) — no usados por el pipeline actual |
| `geometries/main-model_v2.0.3dm` | Modelo Rhino fuente vigente |
| `notebooks/` | Los 3 notebooks del flujo |
| `models/pyg_model.pt` | Modelo PyG entrenado |
| `dataset_graph_classification_v1.0/` | Dataset exportado (`graphs.csv`, `nodes.csv`, `edges.csv`, `meta.yaml`) |

## Entorno

- Intérprete: `..\.env\Scripts\python.exe` (venv en la raíz del repo, **un nivel por encima** de esta carpeta).
- Dependencia clave: `topologicpy` (instalado en ese venv).

## Convenciones del grafo (notebook 01)

- **Un node = una geometría cerrada (cell)**, representado por su centro (`Topology.InternalVertex`).
  NO se usan esquinas / mesh vertices.
- **NO** fundir todas las cells con `Topology.SelfMerge` en un único `CellComplex`: eso parte el
  espacio en cada cara compartida y multiplica los nodes (334 geometrías → ~1621 fragmentos). El
  grafo se construye con `Graph.ByVerticesEdges`.
- **Edge = dos cells que se tocan** (`Topology.ShortestDistance < touch_tol`), con prefiltro por
  bounding box para acelerar.
- Mapping de `cell_type`: `ground=0, office=1, column=2, core=3`. Features one-hot `feature_00..03`.

## topologicpy — notas

- `Topology.ByOBJPath(...)` devuelve una **lista** de clusters, no una `Topology`; hay que iterar y
  extraer faces (`Topology.Faces`) por cada elemento.
- **Importar siempre con `transposeAxes=True`** (es el default): el OBJ es **Y-up** y topologicpy/Rhino
  son **Z-up**, así que transpone Y/Z y el edificio queda con la altura en Z. Con `False` la altura
  sale en Y (error clásico).
- `Topology.ShortestDistance(a, b)` es costoso en bucle O(n²); prefiltrar siempre por bounding box.
- Por capa: `Faces → Helper.Flatten → SelfMerge(Cluster.ByTopologies) → Topology.Cells` da una cell
  por geometría cerrada (esto SÍ es correcto; el problema es el SelfMerge global posterior).

## Git

- No añadir trailers `Co-Authored-By` en los commits.

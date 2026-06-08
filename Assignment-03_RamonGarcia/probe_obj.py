import os, glob, time
import pandas as pd
from topologicpy.Topology import Topology
from topologicpy.Cell import Cell
from topologicpy.CellComplex import CellComplex
from topologicpy.Graph import Graph
from topologicpy.Dictionary import Dictionary
from topologicpy.Vertex import Vertex

OBJ_DIR = r"E:\IAAC Local GIT Repositories\Graph ML - Environment\Assignment-03_RamonGarcia\geometries\obj_geometry"

ROOM_TYPE_BY_CATEGORY = {
    "ground": "circulation",
    "core": "circulation",
    "viewpoint": "amenity",
    "columns": "structure",
    "amenities": "amenity",
    "shops": "retail",
    "apartment": "residential",
}
COLOR_BY_TYPE = {
    "circulation": "red", "amenity": "green", "structure": "gray",
    "retail": "orange", "residential": "blue",
}

def category_of(filename):
    stem = os.path.splitext(os.path.basename(filename))[0]
    parts = stem.split("_", 1)
    name = parts[1] if len(parts) > 1 and parts[0].isdigit() else stem
    name = name.lower()
    if name.startswith("apartment"):
        return "apartment", name
    return name, name

t0 = time.time()
rooms = []
entrance_assigned = False
files = sorted(glob.glob(os.path.join(OBJ_DIR, "*.obj")))
for f in files:
    cat_key, label = category_of(f)
    room_type = ROOM_TYPE_BY_CATEGORY.get(cat_key, "other")
    color = COLOR_BY_TYPE.get(room_type, "gray")
    objs = Topology.ByOBJPath(f, selfMerge=True)
    if not isinstance(objs, list):
        objs = [objs]
    idx = 0
    for o in objs:
        faces = Topology.Faces(o)
        if not faces or len(faces) < 2:
            continue
        try:
            cell = Cell.ByFaces(faces, tolerance=0.001)
        except Exception:
            cell = None
        if cell is None or not Topology.IsInstance(cell, "Cell"):
            continue
        idx += 1
        verts = Topology.Vertices(cell)
        xs = [Vertex.X(v) for v in verts]; ys = [Vertex.Y(v) for v in verts]; zs = [Vertex.Z(v) for v in verts]
        x, y, z = min(xs), min(ys), min(zs)
        width = max(xs) - x; length = max(ys) - y; height = max(zs) - z
        if not entrance_assigned and cat_key == "ground":
            name = "entrance"; entrance_assigned = True
        else:
            name = f"{label}_{idx}"
        d = Dictionary.ByKeysValues(
            ["name", "room_type", "x", "y", "width", "length", "height", "color", "size"],
            [name, room_type, x, y, width, length, height, color, 18],
        )
        cell = Topology.SetDictionary(cell, d)
        rooms.append({"name": name, "room_type": room_type, "x": x, "y": y,
                      "width": width, "length": length, "height": height, "cell": cell})

print("rooms built:", len(rooms), "in %.1fs" % (time.time()-t0))
print("entrance present:", any(r["name"] == "entrance" for r in rooms))
print("room_type counts:")
print(pd.Series([r["room_type"] for r in rooms]).value_counts().to_string())

# zero-size check (degenerate bbox would break aspect_ratio)
deg = [r["name"] for r in rooms if r["width"] == 0 or r["length"] == 0]
print("degenerate width/length rooms:", len(deg), deg[:5])

# Downstream: CellComplex + Graph
t1 = time.time()
cells = [r["cell"] for r in rooms]
building = CellComplex.ByCells(cells, transferDictionaries=True, silent=True)
print("CellComplex built in %.1fs ->" % (time.time()-t1), Topology.TypeAsString(building) if building else None)
if building:
    cc_cells = Topology.Cells(building)
    print("CellComplex #cells:", len(cc_cells) if cc_cells else 0)
    t2 = time.time()
    g = Graph.ByTopology(building, storeBREP=True)
    gv = Graph.Vertices(g); ge = Graph.Edges(g)
    print("Graph built in %.1fs -> #verts:" % (time.time()-t2), len(gv), "#edges:", len(ge))
    print("len(rooms) == #graph_verts:", len(rooms) == len(gv))

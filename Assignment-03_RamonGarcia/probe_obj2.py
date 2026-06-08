import os, glob, time
from topologicpy.Topology import Topology
from topologicpy.Cell import Cell
from topologicpy.Cluster import Cluster
from topologicpy.Graph import Graph
from topologicpy.Dictionary import Dictionary
from topologicpy.Vertex import Vertex

OBJ_DIR = r"E:\IAAC Local GIT Repositories\Graph ML - Environment\Assignment-03_RamonGarcia\geometries\obj_geometry"

rooms = []
for f in sorted(glob.glob(os.path.join(OBJ_DIR, "*.obj"))):
    objs = Topology.ByOBJPath(f, selfMerge=True)
    if not isinstance(objs, list):
        objs = [objs]
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
        d = Dictionary.ByKeysValues(["name", "width"], [f"r{len(rooms)}", 1.0])
        cell = Topology.SetDictionary(cell, d)
        rooms.append(cell)

print("cells:", len(rooms))

# Approach A: Cluster + Graph.ByTopology
t = time.time()
clus = Cluster.ByTopologies(rooms)
try:
    gA = Graph.ByTopology(clus, storeBREP=True)
    gvA = Graph.Vertices(gA)
    print("A) Cluster->Graph: %.1fs verts=%d edges=%d" % (time.time()-t, len(gvA), len(Graph.Edges(gA))))
    # check dict survival
    keys0 = Dictionary.Keys(Topology.Dictionary(gvA[0])) if gvA else None
    print("   vertex[0] dict keys:", keys0)
except Exception as e:
    print("A) failed:", repr(e))

# Approach B: Graph.ByTopology on cluster with direct adjacency flag variations
t = time.time()
try:
    gB = Graph.ByTopology(clus, direct=True, viaSharedTopologies=True, storeBREP=False)
    print("B) direct+shared: %.1fs verts=%d edges=%d" % (time.time()-t, len(Graph.Vertices(gB)), len(Graph.Edges(gB))))
except Exception as e:
    print("B) failed:", repr(e))

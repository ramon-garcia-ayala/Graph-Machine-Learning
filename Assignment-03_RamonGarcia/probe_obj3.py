import os, glob, time
import numpy as np, pandas as pd
from topologicpy.Topology import Topology
from topologicpy.Cell import Cell
from topologicpy.Cluster import Cluster
from topologicpy.Vertex import Vertex
from topologicpy.Edge import Edge
from topologicpy.Graph import Graph
from topologicpy.Dictionary import Dictionary

OBJ_DIR = r"E:\IAAC Local GIT Repositories\Graph ML - Environment\Assignment-03_RamonGarcia\geometries\obj_geometry"
ADJ_TOL = 0.05

ROOM_TYPE_BY_CATEGORY = {"ground":"circulation","core":"circulation","viewpoint":"amenity",
    "columns":"structure","amenities":"amenity","shops":"retail","apartment":"residential"}
COLOR_BY_TYPE = {"circulation":"red","amenity":"green","structure":"gray","retail":"orange","residential":"blue"}

def category_of(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = stem.split("_",1)
    label = (parts[1] if len(parts)>1 and parts[0].isdigit() else stem).lower()
    key = "apartment" if label.startswith("apartment") else label
    return key, label

# ---------------- CELL 10 replacement ----------------
t0=time.time()
rooms=[]; entrance_assigned=False
for f in sorted(glob.glob(os.path.join(OBJ_DIR,"*.obj"))):
    key,label = category_of(f)
    room_type = ROOM_TYPE_BY_CATEGORY.get(key,"other")
    color = COLOR_BY_TYPE.get(room_type,"gray")
    objs = Topology.ByOBJPath(f, selfMerge=True)
    if not isinstance(objs,list): objs=[objs]
    idx=0
    for o in objs:
        faces = Topology.Faces(o)
        if not faces or len(faces)<2: continue
        try: cell = Cell.ByFaces(faces, tolerance=0.001)
        except Exception: cell=None
        if cell is None or not Topology.IsInstance(cell,"Cell"): continue
        idx+=1
        vs=Topology.Vertices(cell)
        xs=[Vertex.X(v) for v in vs]; ys=[Vertex.Y(v) for v in vs]; zs=[Vertex.Z(v) for v in vs]
        x,y,z=min(xs),min(ys),min(zs); width=max(xs)-x; length=max(ys)-y; height=max(zs)-z
        if not entrance_assigned and key=="ground":
            name="entrance"; entrance_assigned=True
        else: name=f"{label}_{idx}"
        d=Dictionary.ByKeysValues(
            ["name","room_type","x","y","width","length","height","color","size"],
            [name,room_type,x,y,width,length,height,color,18])
        cell=Topology.SetDictionary(cell,d)
        rooms.append({"name":name,"room_type":room_type,"x":x,"y":y,
                      "width":width,"length":length,"height":height,"cell":cell})
print("CELL10: rooms=%d (%.1fs) entrance=%s"%(len(rooms),time.time()-t0,
      any(r["name"]=="entrance" for r in rooms)))

# ---------------- CELL 12 replacement: building (Cluster) ----------------
cells=[r["cell"] for r in rooms]
building=Cluster.ByTopologies(cells)
print("CELL12: building=",Topology.TypeAsString(building),"#cells=",len(Topology.Cells(building)))

# ---------------- CELL 18 replacement: custom bbox adjacency graph ----------------
t=time.time()
def bbox(cell):
    vs=Topology.Vertices(cell)
    xs=[Vertex.X(v) for v in vs]; ys=[Vertex.Y(v) for v in vs]; zs=[Vertex.Z(v) for v in vs]
    return (min(xs),min(ys),min(zs),max(xs),max(ys),max(zs))
def touch(a,b,tol=ADJ_TOL):
    return (a[0]<=b[3]+tol and b[0]<=a[3]+tol and
            a[1]<=b[4]+tol and b[1]<=a[4]+tol and
            a[2]<=b[5]+tol and b[2]<=a[5]+tol)
boxes=[bbox(c) for c in cells]
gverts=[]
for c in cells:
    cen=Topology.InternalVertex(c)
    cen=Topology.SetDictionary(cen, Topology.Dictionary(c))
    gverts.append(cen)
gedges=[]; deg=[0]*len(cells)
for i in range(len(cells)):
    for j in range(i+1,len(cells)):
        if touch(boxes[i],boxes[j]):
            gedges.append(Edge.ByVertices([gverts[i],gverts[j]]))
            deg[i]+=1; deg[j]+=1
g=Graph.ByVerticesEdges(gverts,gedges)
gv=Graph.Vertices(g); ge=Graph.Edges(g)
print("CELL18: graph verts=%d edges=%d (%.1fs) deg[min/mean/max]=%d/%.1f/%d isolated=%d"%(
      len(gv),len(ge),time.time()-t,min(deg),sum(deg)/len(deg),max(deg),deg.count(0)))

# ---------------- downstream checks (cells 24/26/28) ----------------
# alignment
print("len(rooms)==#gverts:",len(rooms)==len(gv))
# target
def get_target(d): return 1 if Dictionary.ValueAtKey(d,"room_type")=="circulation" else 0
y=np.array([get_target(Topology.Dictionary(v)) for v in gv])
print("labels: circulation=%d other=%d"%(int(y.sum()),int((y==0).sum())))
# geometric_features KeyError check
def geom(d):
    p=Dictionary.PythonDictionary(d)
    return p["width"]*p["length"], max(p["width"],p["length"])/min(p["width"],p["length"])
bad=0
for v in gv:
    try: geom(Topology.Dictionary(v))
    except Exception as e: bad+=1
print("geometric_features failures:",bad)
# entrance findable + shortest path works
entrance=None
for v in gv:
    if Dictionary.ValueAtKey(Topology.Dictionary(v),"name")=="entrance": entrance=v
print("entrance found:",entrance is not None,"deg(entrance)=",Graph.VertexDegree(g,entrance) if entrance else None)
sp=Graph.ShortestPath(g,gv[200],entrance)
print("sample shortestpath type:",Topology.TypeAsString(sp) if sp else None)

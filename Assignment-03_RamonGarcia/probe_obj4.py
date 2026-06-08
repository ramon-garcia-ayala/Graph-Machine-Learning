import os, glob, tempfile
import numpy as np, pandas as pd
from topologicpy.Topology import Topology
from topologicpy.Cell import Cell
from topologicpy.Cluster import Cluster
from topologicpy.Vertex import Vertex
from topologicpy.Edge import Edge
from topologicpy.Graph import Graph
from topologicpy.Dictionary import Dictionary

OBJ_DIR = r"E:\IAAC Local GIT Repositories\Graph ML - Environment\Assignment-03_RamonGarcia\geometries\obj_geometry"
ROOM_TYPE_BY_CATEGORY = {"ground":"circulation","core":"circulation","viewpoint":"amenity",
    "columns":"structure","amenities":"amenity","shops":"retail","apartment":"residential"}
COLOR_BY_TYPE = {"circulation":"red","amenity":"green","structure":"gray","retail":"orange","residential":"blue"}
def category_of(path):
    stem=os.path.splitext(os.path.basename(path))[0]; parts=stem.split("_",1)
    label=(parts[1] if len(parts)>1 and parts[0].isdigit() else stem).lower()
    return ("apartment" if label.startswith("apartment") else label), label

# CELL 10
rooms=[]; entrance_assigned=False
for path in sorted(glob.glob(os.path.join(OBJ_DIR,"*.obj"))):
    key,label=category_of(path); room_type=ROOM_TYPE_BY_CATEGORY.get(key,"other"); color=COLOR_BY_TYPE.get(room_type,"gray")
    objects=Topology.ByOBJPath(path,selfMerge=True)
    if not isinstance(objects,list): objects=[objects]
    idx=0
    for obj in objects:
        faces=Topology.Faces(obj)
        if not faces or len(faces)<2: continue
        try: cell=Cell.ByFaces(faces,tolerance=0.001)
        except Exception: cell=None
        if cell is None or not Topology.IsInstance(cell,"Cell"): continue
        idx+=1
        vs=Topology.Vertices(cell); xs=[Vertex.X(v) for v in vs]; ys=[Vertex.Y(v) for v in vs]; zs=[Vertex.Z(v) for v in vs]
        x,y=min(xs),min(ys); width,length,height=max(xs)-x,max(ys)-y,max(zs)-min(zs)
        if not entrance_assigned and key=="ground": name="entrance"; entrance_assigned=True
        else: name=f"{label}_{idx}"
        d=Dictionary.ByKeysValues(["name","room_type","x","y","width","length","height","color","size"],
            [name,room_type,x,y,width,length,height,color,18])
        cell=Topology.SetDictionary(cell,d)
        rooms.append({"name":name,"room_type":room_type,"x":x,"y":y,"width":width,"length":length,"height":height,"cell":cell})

# CELL 12
cells=[d['cell'] for d in rooms]; building=Cluster.ByTopologies(cells)

# CELL 18
def _bbox(c):
    vs=Topology.Vertices(c); xs=[Vertex.X(v) for v in vs]; ys=[Vertex.Y(v) for v in vs]; zs=[Vertex.Z(v) for v in vs]
    return (min(xs),min(ys),min(zs),max(xs),max(ys),max(zs))
def _touch(a,b,tol=0.05):
    return (a[0]<=b[3]+tol and b[0]<=a[3]+tol and a[1]<=b[4]+tol and b[1]<=a[4]+tol and a[2]<=b[5]+tol and b[2]<=a[5]+tol)
_boxes=[_bbox(c) for c in cells]
node_verts=[Topology.SetDictionary(Topology.InternalVertex(c),Topology.Dictionary(c)) for c in cells]
adj_edges=[]
for i in range(len(cells)):
    for j in range(i+1,len(cells)):
        if _touch(_boxes[i],_boxes[j]): adj_edges.append(Edge.ByVertices([node_verts[i],node_verts[j]]))
g=Graph.ByVerticesEdges(node_verts,adj_edges); g_verts=Graph.Vertices(g); g_edges=Graph.Edges(g)

# CELL 20
for v in g_verts:
    d=Dictionary.SetValuesAtKeys(Topology.Dictionary(v),["size","color"],[18,"red"]); Topology.SetDictionary(v,d)
for e in g_edges:
    Topology.SetDictionary(e,Dictionary.ByKeysValues(["width","color"],[4,"black"]))

# CELL 24 target
def get_target(d): return 1 if Dictionary.ValueAtKey(d,"room_type")=="circulation" else 0
targets=[]
for v in g_verts:
    d=Dictionary.SetValueAtKey(Topology.Dictionary(v),"label",get_target(Topology.Dictionary(v))); Topology.SetDictionary(v,d); targets.append(get_target(d))
y=np.array(targets,dtype=int)

# CELL 26 geometric
def geometric_features(d):
    p=Dictionary.PythonDictionary(d); area=p["width"]*p["length"]; per=2*(p["width"]+p["length"])
    ar=max(p["width"],p["length"])/min(p["width"],p["length"]); comp=area/(per**2) if per>0 else 0.0
    return {"area":area,"perimeter":per,"aspect_ratio":ar,"compactness":comp}
gf=[]
for v in g_verts:
    d=Topology.Dictionary(v); feat=geometric_features(d)
    for k in feat: d=Dictionary.SetValueAtKey(d,k,feat[k])
    Topology.SetDictionary(v,d); gf.append(feat)
geom_df=pd.DataFrame(gf); geom_df.index=[r["name"] for r in rooms]

# CELL 28 topological
entrance=None
for v in g_verts:
    d=Topology.Dictionary(v)
    if Dictionary.ValueAtKey(d,"name")=="entrance": entrance=v
    d=Dictionary.SetValuesAtKeys(d,["degree","is_connected_to_entrance"],[Graph.VertexDegree(g,v),0]); Topology.SetDictionary(v,d)
for v in g_verts:
    d=Topology.Dictionary(v); path=Graph.ShortestPath(g,v,entrance)
    dist=len(Topology.Edges(path)) if Topology.IsInstance(path,"wire") else (1 if Topology.IsInstance(path,"edge") else 0)
    d=Dictionary.SetValueAtKey(d,"distance_to_entrance",dist); Topology.SetDictionary(v,d)
for av in Graph.AdjacentVertices(g,entrance):
    d=Dictionary.SetValueAtKey(Topology.Dictionary(av),"is_connected_to_entrance",1); Topology.SetDictionary(av,d)
def topo(d): return {"degree":Dictionary.ValueAtKey(d,"degree"),"distance_to_entrance":Dictionary.ValueAtKey(d,"distance_to_entrance"),"is_connected_to_entrance":Dictionary.ValueAtKey(d,"is_connected_to_entrance")}
topo_df=pd.DataFrame([topo(Topology.Dictionary(v)) for v in g_verts]); topo_df.index=[Dictionary.ValueAtKey(Topology.Dictionary(v),"name") for v in g_verts]

# CELL 30/31 semantic
room_types=sorted({r["room_type"] for r in rooms}); keys=["room_type_"+s for s in room_types]
def oh(val,cats): return [1 if val==c else 0 for c in cats]
for v in g_verts:
    d=Topology.Dictionary(v); d=Dictionary.SetValuesAtKeys(d,keys,oh(Dictionary.ValueAtKey(d,"room_type"),room_types)); Topology.SetDictionary(v,d)
def sem(d):
    r={"room_type":Dictionary.ValueAtKey(d,"room_type")}
    for k in keys: r[k]=Dictionary.ValueAtKey(d,k)
    return r
semantic_df=pd.DataFrame([sem(Topology.Dictionary(v)) for v in g_verts]); semantic_df.index=[Dictionary.ValueAtKey(Topology.Dictionary(v),"name") for v in g_verts]

# CELL 33/35 feature matrix
feature_df=pd.concat([geom_df.reset_index(drop=True),topo_df.reset_index(drop=True),semantic_df.drop(columns=["room_type"]).reset_index(drop=True)],axis=1)
feature_df.index=[Dictionary.ValueAtKey(Topology.Dictionary(v),"name") for v in g_verts]
node_features=[c for c in feature_df.columns.tolist() if "room_type_" not in c]

# CELL 37/38 export + reimport to TEMP dir
tmp=tempfile.mkdtemp(prefix="ds_")
status=Graph.ExportGraphsToCSV([g],path=tmp,nodeLabelKey="label",nodeFeaturesKeys=node_features,overwrite=True)
graphs=Graph.ByCSVPath(path=tmp); new_g=graphs[0]

print("OK end-to-end")
print(" rooms/nodes:",len(rooms),"/",len(g_verts),"edges:",len(g_edges))
print(" labels circ/other:",int(y.sum()),"/",int((y==0).sum()))
print(" room_types:",room_types)
print(" node_features:",node_features)
print(" feature_df shape:",feature_df.shape)
print(" export status:",status," reimport nodes:",len(Graph.Vertices(new_g)))
print(" exported files:",os.listdir(tmp))

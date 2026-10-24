import sys, json, time
sys.path.insert(0, sys.argv[3])
from common import *
from OCP.XCAFPrs import XCAFPrs_DocumentExplorer, XCAFPrs_DocumentExplorerFlags_None
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.RWGltf import RWGltf_CafWriter
from OCP.TColStd import TColStd_IndexedDataMapOfStringString, TColStd_MapOfAsciiString
from OCP.TCollection import TCollection_AsciiString
from OCP.Message import Message_ProgressRange
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.BRep import BRep_Tool
from OCP.TopoDS import TopoDS

xbf, outdir = sys.argv[1], sys.argv[2]
UF = "Upper Frame Model AL Extursion 4040 v22:1"
targets = {
  "seat": [[UF, "SPARCO Seat v2:2"]],
  "seat-brackets": [[UF, "Laser Cut Model Of Seat Adj Plates v3:1"], [UF, "Laser Cut Model Of Seat Adj Plates v3(Mirror):1"]],
  "wheel": [[UF, "MOZA  F1 Wheel v2:1"]],
  "wheelbase": [[UF, "Moza R9 Base Mount Plate v17:1"]],
  "pedals": [[UF, "Pedal Set 2 v2:1"]],
  "shifter": [[UF, "MOZA-SHIFT-STP v1:1"]],
  "handbrake": [[UF, "Rally Handbrake v2:1"]],
  "monitor": [[UF, "Model Monitor v5:1"]],
}
lin, ang = float(sys.argv[4]), float(sys.argv[5])
a, doc, st = load_xbf(xbf)
rootseq = TDF_LabelSequence()
for r in roots(doc): rootseq.Append(r)

# walk every node once, remembering its instance-name path
nodes = []  # (path tuple, id string, depth)
exp = XCAFPrs_DocumentExplorer(doc, rootseq, XCAFPrs_DocumentExplorerFlags_None)
stack = []
while exp.More():
    n = exp.Current(); d = exp.CurrentDepth()
    stack = stack[:d] + [name(n.Label)]
    nodes.append((tuple(stack[1:]), n.Id.ToCString(), d))
    exp.Next()
print("nodes", len(nodes), flush=True)

def tri_count(shape):
    e = TopExp_Explorer(shape, TopAbs_FACE); t = 0
    while e.More():
        loc = TopLoc_Location()
        tr = BRep_Tool.Triangulation_s(TopoDS.Face_s(e.Current()), loc)
        if tr is not None: t += tr.NbTriangles()
        e.Next()
    return t

report = {}
for key, paths in targets.items():
    t0 = time.time()
    flt = TColStd_MapOfAsciiString()
    bb = Bnd_Box(); tris = 0
    for path in paths:
        comp, lab, loc = find_path(doc, path)
        shp = XCAFDoc_ShapeTool.GetShape_s(lab).Moved(loc)
        BRepMesh_IncrementalMesh(shp, lin, False, ang, True)
        BRepBndLib.Add_s(shp, bb, True)
        tris += tri_count(shp)
        p = tuple(path)
        for npath, nid, d in nodes:
            # keep the node itself, everything under it, and the assemblies above it
            if npath[:len(p)] == p or p[:len(npath)] == npath:
                flt.Add(TCollection_AsciiString(nid))
    w = RWGltf_CafWriter(TCollection_AsciiString(f"{outdir}/{key}.glb"), True)
    w.SetMergeFaces(True)
    ok = w.Perform(doc, rootseq, flt, TColStd_IndexedDataMapOfStringString(), Message_ProgressRange())
    x0,y0,z0,x1,y1,z1 = bb.Get()
    report[key] = {"ok": ok, "triangles": tris, "bbox_mm": [round(v,1) for v in (x0,y0,z0,x1,y1,z1)],
                   "size_mm": [round(x1-x0,1), round(y1-y0,1), round(z1-z0,1)]}
    print(key, report[key], round(time.time()-t0,1), "s", flush=True)
json.dump(report, open(f"{outdir}/report.json", "w"), indent=1)

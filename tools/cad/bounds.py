import sys, json, numpy as np, trimesh
d = sys.argv[1]
out = {}
def verts(name):
    s = trimesh.load(f"{d}/{name}.glb", force='scene')
    V = []
    for n in s.graph.nodes_geometry:
        T, g = s.graph[n]; m = s.geometry[g]
        V.append((np.c_[m.vertices, np.ones(len(m.vertices))] @ T.T)[:, :3])
    return np.vstack(V) * 1000.0
for name in ["seat", "seat-brackets", "wheel", "wheelbase", "pedals", "shifter", "handbrake", "monitor"]:
    V = verts(name)
    out[name] = {"min": V.min(0).round(1).tolist(), "max": V.max(0).round(1).tolist(), "verts": int(len(V))}
    print(name, out[name])
json.dump(out, open(f"{d}/bounds.json", "w"), indent=1)
# seat silhouettes in HexRig coordinates (mm)
V = verts("seat")
def env(a, b, step):
    lo, hi = a.min(), a.max(); n = int(np.ceil((hi - lo) / step)); res = []
    for i in range(n):
        e0, e1 = lo + i * step, lo + (i + 1) * step
        sel = (a >= e0) & (a <= e1)
        if sel.any(): res.append([round(float(min(max((e0 + e1) / 2, lo), hi)), 1), round(float(b[sel].min()), 1), round(float(b[sel].max()), 1)])
    res[0][0] = round(float(lo), 1); res[-1][0] = round(float(hi), 1)
    return res
json.dump({"side": env(V[:, 0], V[:, 1], 35), "top": env(V[:, 0], V[:, 2], 35)}, open(f"{d}/seat-silhouette.json", "w"))
print(json.load(open(f"{d}/seat-silhouette.json"))["side"])

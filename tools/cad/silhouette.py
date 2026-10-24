import sys, json, numpy as np, trimesh
glb, off = sys.argv[1], json.loads(sys.argv[2])
scene = trimesh.load(glb, force='scene')
V = []
for name, g in scene.graph.nodes_geometry and [(n, scene.graph[n]) for n in scene.graph.nodes_geometry]:
    T, geom = g
    m = scene.geometry[geom]
    v = np.c_[m.vertices, np.ones(len(m.vertices))] @ T.T
    V.append(v[:, :3])
V = np.vstack(V) + np.array(off)
print("bbox", V.min(0).round(1), V.max(0).round(1), len(V))
def env(a, b, step):
    lo, hi = a.min(), a.max(); edges = np.arange(lo, hi + step, step); out = []
    for i in range(len(edges) - 1):
        sel = (a >= edges[i]) & (a < edges[i + 1] + (1 if i == len(edges) - 2 else 0))
        if sel.sum(): out.append({"x": round(float((edges[i] + edges[i + 1]) / 2)), "lo": round(float(b[sel].min())), "hi": round(float(b[sel].max()))})
    return out
side = env(V[:, 0], V[:, 1], 40)
top = env(V[:, 0], V[:, 2], 40)
print(json.dumps(side).replace('"', "'"))
print(json.dumps(top).replace('"', "'"))

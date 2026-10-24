import sys, time
sys.path.insert(0, sys.argv[3])
from common import load_step
from OCP.TCollection import TCollection_ExtendedString
t = time.time()
a, doc = load_step(sys.argv[1])
print("loaded", time.time()-t, flush=True)
st = a.SaveAs(doc, TCollection_ExtendedString(sys.argv[2]))
print("saved", st, time.time()-t, flush=True)

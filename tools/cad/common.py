import time
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ShapeTool
from OCP.TDF import TDF_LabelSequence, TDF_Label
from OCP.TDataStd import TDataStd_Name
from OCP.TopLoc import TopLoc_Location
from OCP.XCAFApp import XCAFApp_Application
from OCP.BinXCAFDrivers import BinXCAFDrivers
from OCP.PCDM import PCDM_ReaderStatus

def app():
    a = XCAFApp_Application.GetApplication_s()
    BinXCAFDrivers.DefineFormat_s(a)
    return a

def load_step(path):
    a = app()
    doc = TDocStd_Document(TCollection_ExtendedString("BinXCAF"))
    a.InitDocument(doc)
    r = STEPCAFControl_Reader()
    r.SetNameMode(True); r.SetColorMode(True); r.SetLayerMode(True)
    r.ReadFile(path); r.Transfer(doc)
    return a, doc

def load_xbf(path):
    # TDocStd_Application.Open can't hand the new document back through the Python binding,
    # so read straight into a document we own.
    from OCP.BinXCAFDrivers import BinXCAFDrivers_DocumentRetrievalDriver
    from OCP.PCDM import PCDM_ReaderFilter
    from OCP.Message import Message_ProgressRange
    a = app()
    doc = TDocStd_Document(TCollection_ExtendedString("BinXCAF"))
    drv = BinXCAFDrivers_DocumentRetrievalDriver()
    drv.Read(TCollection_ExtendedString(path), doc, a, PCDM_ReaderFilter(), Message_ProgressRange())
    return a, doc, drv.GetStatus()

def name(label):
    attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
        return attr.Get().ToExtString()
    return "?"

def components(label):
    comps = TDF_LabelSequence()
    XCAFDoc_ShapeTool.GetComponents_s(label, comps, False)
    out = []
    for i in range(1, comps.Length()+1):
        c = comps.Value(i)
        ref = TDF_Label()
        XCAFDoc_ShapeTool.GetReferredShape_s(c, ref)
        out.append((c, ref, XCAFDoc_ShapeTool.GetLocation_s(c)))
    return out

def roots(doc):
    st = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    seq = TDF_LabelSequence(); st.GetFreeShapes(seq)
    return [seq.Value(i) for i in range(1, seq.Length()+1)]

def find_path(doc, names):
    """Follow instance names from the root; returns (component label, referred label, accumulated location)."""
    lab = roots(doc)[0]; loc = TopLoc_Location(); comp = None
    for n in names:
        for c, ref, l in components(lab):
            if name(c) == n:
                comp, lab, loc = c, ref, loc.Multiplied(l); break
        else:
            raise KeyError(n)
    return comp, lab, loc

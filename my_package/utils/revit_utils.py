
import Grasshopper
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
from RhinoInside.Revit import Revit, Convert

def get_active_doc():
    return Revit.ActiveDBDocument

def get_active_ui_doc():
    return Revit.ActiveUIDocument
def get_revit_version():
    return Revit.ActiveUIApplication.Application.VersionNumber

def show_warning(msg):
    ghenv.Component.AddRuntimeMessage(RML.Warning, msg)

def show_error(msg):
    ghenv.Component.AddRuntimeMessage(RML.Error, msg)

def show_remark(msg):
    ghenv.Component.AddRuntimeMessage(RML.Remark, msg)
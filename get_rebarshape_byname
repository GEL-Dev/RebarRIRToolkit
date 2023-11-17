__author__ = "ykish"
__version__ = "2023.05.08"

import rhinoscriptsyntax as rs

import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
import math
import Rhino
import RhinoInside
import Grasshopper
import ghpythonlib.treehelpers as th
import Grasshopper.Kernel.Data.GH_Path as GH_Path
import Grasshopper.DataTree as DataTree
import scriptcontext
from RhinoInside.Revit import Revit, Convert
from Autodesk.Revit import DB
from Autodesk.Revit.DB.Structure import *
from System.Collections.Generic import List, IList
from System import Enum, Action

doc = Revit.ActiveDBDocument
if shape is not None:

    allRebarShape  = DB.FilteredElementCollector(doc).OfClass(DB.Structure.RebarShape).WhereElementIsElementType().ToElements()
    rebarShape = [rebarShape for rebarShape in allRebarShape if rebarShape.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == shape]
'''
for res in allRebarShape:
    print res.Id
    print doc.GetElement(res.Id).get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString()
    
'''
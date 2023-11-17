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

def getRebarDiameter(rebar):
	bartypeId = rebar.GetTypeId()
	type = doc.GetElement(bartypeId)
	diameter = type.BarModelDiameter
	diameter = Convert.Geometry.GeometryDecoder.ToModelLength(diameter)
	return diameter, type
	
def getCenterLineCurves(rebar):
    revit_Curves = element.GetCenterlineCurves(0,0,0,MultiplanarOption.IncludeAllMultiplanarCurves,0)
    curves = []
    for rc in revit_Curves:
        if rc.GetType() == DB.Line:
            c = Convert.Geometry.GeometryDecoder.ToCurve(rc)
            curves.append(c)
        if rc.GetType() == DB.Arc:
            c = Convert.Geometry.GeometryDecoder.ToCurve(rc)
            curves.append(c)
    return curves

    
def getSpacing(rebar):

    layoutRule = rebar.LayoutRule
    
    if layoutRule == "Single":
        return 0  # or whatever default value you want to return for single bars
    
    try:
        s = rebar.MaxSpacing
        return Convert.Geometry.GeometryDecoder.ToModelLength(s)
    except Exception as e:
        
        return None
    
    
centerLine = getCenterLineCurves(element)
diameter = getRebarDiameter(element)[0]

quantity = element.NumberOfBarPositions 
spacing = getSpacing(element)


rebartype = getRebarDiameter(element)[1]
paraIndex = DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS;
comment = element.get_Parameter(paraIndex).AsString()
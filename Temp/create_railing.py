__author__ = "ykish"
__version__ = "2023.10.29"

import clr
clr.AddReference('System.Core')
clr.AddReference('RhinoInside.Revit')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from RhinoInside.Revit import Revit, Convert
from Autodesk.Revit.DB import CurveLoop, ElementType, Level, Transaction, Architecture

def create_railing(curve, type_element, level):
    result = None
    doc = Revit.ActiveDBDocument
    with Transaction(doc, "Create Railing") as transaction:
        transaction.Start()
        rv_curve= Convert.Geometry.GeometryEncoder.ToCurve(curve)
        curve_loop = CurveLoop.Create([rv_curve])
        result = Architecture.Railing.Create(doc, curve_loop, type_element.Id, level.Id)
        
        transaction.Commit()
    
    return result

railing = create_railing(curve, type, level)
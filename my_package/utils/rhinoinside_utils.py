# -*- coding: utf-8 -*-
import clr
clr.AddReference('RhinoInside.Revit')
clr.AddReference('System.Core')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
from RhinoInside.Revit import Revit, Convert
from Autodesk.Revit import DB
from System.Collections.Generic import List, IList
from System import Enum, Action, Func, Uri, Guid, DateTime
from Autodesk.Revit.DB import XYZ, Line as RevitLine, CurveArray, CurveArrArray,NurbSpline,BoundingBoxXYZ, Arc as RevitArc,Curve as RevitCurve,CurveLoop,CylindricalHelix, Ellipse as RevitEllipse,HermiteSpline 
from Rhino.Geometry import Arc, Circle,Point3d,Point3f, Vector3d,Vector3f,Line ,Polyline, PolyCurve, Curve, PolylineCurve, NurbsCurve,LineCurve,Ellipse,Arc,Circle,ArcCurve
import RhinoInside.Revit.Convert.Geometry
clr.ImportExtensions(RhinoInside.Revit.Convert.Geometry)



def get_active_doc():
    return Revit.ActiveDBDocument

def get_active_ui_doc():
    return Revit.ActiveUIDocument

def convert_rhino_to_revit_geometry(rhino_geometry):
    geometry_type = type(rhino_geometry)
    print(geometry_type)
    if geometry_type is Point3d or \
        geometry_type is Point3f or \
        geometry_type is Vector3d or \
        geometry_type is Vector3f:
            return rhino_geometry.ToXYZ()
    elif geometry_type is Ellipse or \
        geometry_type is LineCurve or \
        geometry_type is NurbsCurve or \
        geometry_type is PolyCurve or \
        geometry_type is PolylineCurve or \
        geometry_type is Curve or \
        geometry_type is ArcCurve:
            return rhino_geometry.ToCurve()
    elif geometry_type is Polyline:
        return rhino_geometry.ToPolyLine()
    elif geometry_type is Line:
        return rhino_geometry.ToLine()
    elif geometry_type is Arc or\
        geometry_type is Circle:
            return rhino_geometry.ToArc()
    else:
        raise ValueError("Unsupported geometry type: {0}".format(geometry_type))
def convert_revit_to_rhino_geometry(revit_geometry):
    geometry_type = type(revit_geometry)
    print(geometry_type)
    if geometry_type is BoundingBoxXYZ:
            return revit_geometry.ToBox()
    elif geometry_type is RevitArc or \
        geometry_type is RevitCurve or \
        geometry_type is CurveLoop or \
        geometry_type is RevitLine or \
        geometry_type is CylindricalHelix or \
        geometry_type is NurbSpline or \
        geometry_type is HermiteSpline:
            return revit_geometry.ToCurve()
    elif geometry_type is CurveArray or \
        geometry_type is CurveArrArray:
            return revit_geometry.ToCurveMany()
    elif geometry_type is XYZ:
            return revit_geometry.ToPoint3d()
    else:
        raise ValueError("Unsupported geometry type: {0}".format(geometry_type))
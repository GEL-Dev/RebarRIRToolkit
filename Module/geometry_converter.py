import clr

clr.AddReference("RevitAPI")
clr.AddReference("RhinoCommon")

from Autodesk.Revit.DB import Line as RevitLine
from Rhino.Geometry import Line as RhinoLine

def convert_line(revit_line):
    """Converts a Rhino line to a Revit line"""
    start = convert_point(revit_line.From)
    end = convert_point(revit_line.To)
    return RevitLine.CreateBound(start, end)

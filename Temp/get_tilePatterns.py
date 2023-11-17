import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import TilePatternsBuiltIn
from System import Enum
from RhinoInside.Revit import Revit

doc = Revit.ActiveDBDocument
tilepatterns = doc.Settings.TilePatterns

tilePatternsName = [x.ToString() for x in Enum.GetValues(TilePatternsBuiltIn)]

titlePatterns = tilePatternsName
a = Enum.GetValues(TilePatternsBuiltIn)
b = tilepatterns
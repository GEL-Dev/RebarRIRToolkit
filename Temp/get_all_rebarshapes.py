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
import System
from System.Collections.Generic import List, IList
from System import Enum, Action

# Get the Revit document
doc = Revit.ActiveDBDocument

allRebarShape  = DB.FilteredElementCollector(doc).OfClass(DB.Structure.RebarShape).WhereElementIsElementType().ToElements()
allRebarShapeNames = []

# Get all the rebar shape names
for shape in allRebarShape:
    allRebarShapeNames.append(shape.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString())

# Get all curves for the browser
output_tree = DataTree[System.Object]()

for i, shape in enumerate(allRebarShape):
    curves = shape.GetCurvesForBrowser()
    for j,curve in enumerate(curves):
        rhino_curve = Convert.Geometry.GeometryDecoder.ToCurve(curve)
        output_tree.Add(rhino_curve, GH_Path(i))

allRebarCurves = output_tree

# Get all the rebar hook angles
output_tree = DataTree[System.Object]()
allRebarShapeHookAngle = []

for i, shape in enumerate(allRebarShape):
        output_tree.Add(shape.GetDefaultHookAngle(0), GH_Path(i))
        output_tree.Add(shape.GetDefaultHookAngle(1), GH_Path(i))
allRebarShapeHookAngle = output_tree
    
# Get all the rebar hook angles
output_tree = DataTree[System.Object]()
allRebarShapeHookOrientation = []

for i, shape in enumerate(allRebarShape):
        output_tree.Add(shape.GetDefaultHookOrientation(0), GH_Path(i))
        output_tree.Add(shape.GetDefaultHookOrientation(1), GH_Path(i))
allRebarShapeHookOrientation = output_tree

# Get all the rebar parameters
output_tree = DataTree[System.Object]()
output_curve = DataTree[System.Object]()
allRebarSegmentLabel = []
for i, shape in enumerate(allRebarShape):
    familyId = shape.ShapeFamilyId
    family = doc.GetElement(familyId)
    family_doc = doc.EditFamily(family);
    #family_doc = family.Document
    
    collector = DB.FilteredElementCollector(family_doc);
    familyDimensions = collector.OfClass(DB.Dimension).ToElements();
    labelParamIdToDimId ={}
    for dim in familyDimensions:
        try:
            famParam = dim.FamilyLabel 
            print(famParam)
            if famParam is not None:
                print(famParam.Id)
                labelParamIdToDimId[famParam.Id] = dim.Id
                print("Print not None")
                print(dim.Id)
            
            
            #if famParam is not None:
                
                #print(dim.Id)
        except :
            continue
    
    def_by_seg = shape.GetRebarShapeDefinition()
    if not isinstance(def_by_seg, RebarShapeDefinitionBySegments):
        raise TypeError("Expected RebarShapeDefinitionBySegments type")
    segment_pos_to_label = {}
    curves_for_browser = shape.GetCurvesForBrowser()
    for ii in range(def_by_seg.NumberOfSegments):
        seg = def_by_seg.GetSegment(ii)
        constraints = seg.GetConstraints()
        for constraint in constraints:
            param_id = constraint.GetParamId()
            if param_id is not DB.ElementId.InvalidElementId and param_id in labelParamIdToDimId :
                label_name = ""
                for param in shape.Parameters:
                    if param.Id == param_id:
                        label_name = param.Definition.Name
                        rhino_curve = Convert.Geometry.GeometryDecoder.ToCurve(curves_for_browser[ii])
                        segment_pos_to_label[label_name] = rhino_curve
                        output_tree.Add(label_name, GH_Path(i))
                        output_curve.Add(rhino_curve, GH_Path(i))
                        
        
allRebarSegmentLabel = output_tree
allRebarCurves = output_curve
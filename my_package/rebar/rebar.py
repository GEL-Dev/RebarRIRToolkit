# -*- coding: utf-8 -*-

import clr
from rebarShape import RebarShapeCurve
from data_processor import find_row_by_name
from utils.utils import update_params_from_dict_list, dictionary_from_csv
from utils.rhinoinside_utils import convert_rhino_to_revit_geometry, get_active_doc, get_active_ui_doc, convert_rhino_to_revit_length, convert_revit_to_rhino_length
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction, BuiltInParameter, IFailuresPreprocessor, FailureProcessingResult, BuiltInFailures, ElementId
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarShape, RebarHookType,RebarReinforcementData, RebarCoupler,RebarCouplerError,RebarHookOrientation

import math

class MyPreProcessor(IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):
        transactionName = failuresAccessor.GetTransactionName()
        failMessages = failuresAccessor.GetFailureMessages()
        
        if failMessages.Count == 0:
            return FailureProcessingResult.Continue

        for currentMessage in failMessages:
            failID = currentMessage.GetFailureDefinitionId()
            if failID == BuiltInFailures.OverlapFailures.DuplicateRebar:
                failuresAccessor.DeleteWarning(currentMessage)
        
        return FailureProcessingResult.Continue

def get_hook_orientation(hook_orientation):
    if hook_orientation == 'left' or hook_orientation == 'Left':
        return RebarHookOrientation.Left
    elif hook_orientation == 'right' or hook_orientation == 'Right':
        return RebarHookOrientation.Right
    else:
        return None
    
def get_hook_orientation_from_shapename(shapename):
    data = find_row_by_name(shapename)
    start_hook_orientation =get_hook_orientation(data[0]['HookOrientation0']) 
    end_hook_orientation =  get_hook_orientation(data[0]['HookOrientation1']) 

    return [start_hook_orientation, end_hook_orientation]
    
def get_rebar_type_by_diameter(rh_diameter):
    doc = get_active_doc()
    rebar_types = FilteredElementCollector(doc).OfClass(RebarBarType).ToElements()
    for rebar_type in rebar_types:
        print(rebar_type)
        print(rebar_type.BarModelDiameter)
        rv_diameter = convert_rhino_to_revit_length(rh_diameter)
        if abs(rebar_type.BarModelDiameter - rv_diameter) < 0.00001:
            return rebar_type
    return None

def get_rebar_shape_by_name(name):
    doc = get_active_doc()
    rebar_shapes = [rebarShape for rebarShape in FilteredElementCollector(doc).OfClass(RebarShape).ToElements() if rebarShape.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == name]
    if len(rebar_shapes) > 0:
        return rebar_shapes[0]
    return None

def get_hook_type_by_angle(angle):
    doc = get_active_doc()
    rebar_hook_type = [rebarHook for rebarHook in FilteredElementCollector(doc).OfClass(RebarHookType).ToElements() if abs(rebarHook.HookAngle -angle) < 0.001 ]
    if len(rebar_hook_type) > 0:
        return rebar_hook_type[0]
    return None

def get_hook_type_from_shapename(shapename):
    data = find_row_by_name(shapename)
    start_hook_type =get_hook_type_by_angle(float(data[0]['Hook At Start'] )* math.pi/180) 
    end_hook_type =  get_hook_type_by_angle(float(data[0]['Hook At End']) * math.pi/180) 

    return [start_hook_type, end_hook_type]

def create_rebar_from_cureves_and_shape(host,curves, norm, diameter, shape,startHookAngle,endHookAngle, startHookOrientation,endHookOrientation):
    doc = get_active_doc()
    rv_shape = get_rebar_shape_by_name(shape)
    rv_curves = [convert_rhino_to_revit_geometry(curve) for curve in curves]
    rv_norm = convert_rhino_to_revit_geometry(norm)
    rv_type = get_rebar_type_by_diameter(diameter)
    rv_startHookType = get_hook_type_by_angle(startHookAngle)
    rv_endHookType = get_hook_type_by_angle(endHookAngle)
    rv_startHookOrientation = get_hook_orientation(startHookOrientation)
    rv_endHookOrientation = get_hook_orientation(endHookOrientation)

    rebar = Rebar.CreateFromCurvesAndShape(doc, rv_shape, rv_type, rv_startHookType, rv_endHookType, host, rv_norm, rv_curves, rv_startHookOrientation, rv_endHookOrientation)
    return rebar

def create_rebar_from_shape(host, diameter, shape,origin, xVec, yVec):
    doc = get_active_doc()
    rv_shape = get_rebar_shape_by_name(shape)
    rv_origin = convert_rhino_to_revit_geometry(origin)
    rv_xVec = convert_rhino_to_revit_geometry(xVec)
    rv_yVec = convert_rhino_to_revit_geometry(yVec)
    rv_type = get_rebar_type_by_diameter(diameter)

    rebar = Rebar.CreateFromRebarShape(doc, rv_shape, rv_type, host, rv_origin, rv_xVec, rv_yVec)
    return rebar

def scaleToBox_rebar(rebar, origin, xVec, yVec):
    doc = get_active_doc()
    rv_origin = convert_rhino_to_revit_geometry(origin)
    rv_xVec = convert_rhino_to_revit_geometry(xVec)
    rv_yVec = convert_rhino_to_revit_geometry(yVec)
    rebar_diameter = rebar.get_Parameter(BuiltInParameter.REBAR_BAR_DIAMETER).AsDouble()
    accessor = rebar.GetShapeDrivenAccessor()
    if rebar.GetHookRotationAngle(1)>0:
        accessor.ScaleToBox(rv_origin - rebar_diameter*rv_xVec.Normalize()*0.5, rv_xVec +  rebar_diameter*rv_xVec.Normalize(), rv_yVec)
    else:
        accessor.ScaleToBox(rv_origin - rebar_diameter*rv_xVec.Normalize()*0.5, rv_xVec +  rebar_diameter*rv_xVec.Normalize()*0.5, rv_yVec)
    return rebar

def set_layoutAsNumberWithSpacing(rebar, number, spacing):
    doc = get_active_doc()
    rv_spacing = convert_rhino_to_revit_length(spacing)
    accessor = rebar.GetShapeDrivenAccessor()
    accessor.SetLayoutAsNumberWithSpacing(number, rv_spacing)
    return rebar

def create_rebar_coupler_at_Start(rebar):
    doc = get_active_doc()
    rebar_diameter = rebar.get_Parameter(BuiltInParameter.REBAR_BAR_DIAMETER).AsString()
    cuplerTypes = [couplerType for couplerType in FilteredElementCollector(doc).OfClass(RebarCoupler).ToElements() if  rebar_diameter in couplerType.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() ]
    if len(cuplerTypes) > 0:
        defaulttypeId = cuplerTypes[0].Id
        if defaulttypeId != ElementId.InvalidElementId:
            rebarData1 = RebarReinforcementData.Create(rebar.Id, 0)
            error = clr.Reference[RebarCouplerError]()
            return RebarCoupler.Create(doc, defaulttypeId, rebarData1, None, error)
    return None

def create_rebars_from_curves_and_shape(host, curves_list, norms, shapes, startHookAngles, endHookAngles, startHookOrientations, endHookOrientations, spacings, diameters, comments, bar_counts):
    doc = get_active_doc()
    rebars = []
    with Transaction(doc, 'create_bars') as t:
        t.Start()
        failureOptions = t.GetFailureHandlingOptions()
        handler = MyPreProcessor()
        t.SetFailureHandlingOptions(failureOptions)
        
        for i, curve in enumerate(curves_list):
            rebar = create_rebar_from_cureves_and_shape(host,curves_list[i], norms[i], diameters[i], shapes[i],startHookAngles[i],endHookAngles[i], startHookOrientations[i],endHookOrientations[i])
            if(spacings[i] == None and spacings[i] >0):
                rebar = set_layoutAsNumberWithSpacing(rebar, bar_counts[i], spacings[i])
            rebars.append(rebar)


        t.Commit()
    return rebars


def create_rebars_from_curves(curves, norms, types, shapes, pitches, a, b, c, d, e, f, g, comments, bar_numbers):
    rebars = []
    with Transaction('create_bars') as t:
        doc = get_active_doc()
        t.Start()
        failureOptions = t.GetFailureHandlingOptions()
        handler = MyPreProcessor()
        t.SetFailureHandlingOptions(failureOptions)

        for i, curve in enumerate(curves):
            rebar = Rebar.CreateFromCurvesAndShape(doc, shapes[i], types[i], None, None, None, norms[i], curve, RebarHookOrientation.Right, RebarHookOrientation.Right)
            # その他のRebar設定...
            rebars.append(rebar.Id)

        t.Commit()
    return rebars


def get_rebars_in_doc(doc):
    return FilteredElementCollector(doc).OfClass(Rebar).ToElements()

def get_rebar_in_host(doc,host):
    return FilteredElementCollector(doc,host.Id).OfClass(Rebar).ToElements()

def get_rebar_by_mark(doc,mark):
    return FilteredElementCollector(doc).OfClass(Rebar).WhereElementIsNotElementType().Where(lambda r:r.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString() == mark).ToElements()

def get_rebar_in_host_by_mark(doc,host,mark):
    return FilteredElementCollector(doc,host.Id).OfClass(Rebar).WhereElementIsNotElementType().Where(lambda r:r.get_Parameter(BuiltInParameter.ALL_MODEL_MARK).AsString() == mark).ToElements()


def create_rebarShapeParams_from_csv(csv_path):
    dict_list = dictionary_from_csv(csv_path)
    params_template = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'x': None, 'y': None, 'j': None}
    updated_params_list = update_params_from_dict_list(dict_list, params_template)
    return updated_params_list

def create_rebarShapePrarams_from_dict(dict):
    params_template = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'x': None, 'y': None, 'j': None}
    updated_params = params_template.copy()
    for key in updated_params:
        if key in dict:
            updated_params[key] = None if dict[key] == "" else float(dict[key])
    return updated_params

def create_rebarShapeCurve_from_csv(csv_path, planes=None):
    params_list = create_rebarShapeParams_from_csv(csv_path)
    dict_list = dictionary_from_csv(csv_path)
    if planes == None:
        planes = [None for i in range(len(dict_list))]
    rebarShape_list = []
    for i, dict in enumerate(dict_list):
        name = dict['shape']
        data= find_row_by_name(name)
        rgName = data[0]['RhinoBaseLineType']
        rebarShape_list.append(RebarShapeCurve(rgName,name, planes[i],**params_list[i]).curve)
    return rebarShape_list

def create_rebarShapeCurve_from_params(name,params, plane=None):
    return RebarShapeCurve(name, plane,**params)

def create_rebars_from_csv(csv_path, planes,host, startHookOrientations, endHookOrientations,  comments):
    curves_list = create_rebarShapeCurve_from_csv(csv_path, planes )
    norms = [plane.Normal for plane in planes]
    dict_list = dictionary_from_csv(csv_path)
    shapes = [dict['shape'] for dict in dict_list]
    spacings = [dict['spacing'] for dict in dict_list]
    diameters = [dict['diameter'] for dict in dict_list]
    bar_counts = [dict['number'] for dict in dict_list]
    startHookAngles = [find_row_by_name(dict['shape'])['Hook At Start'] * math.pi/180 for dict in dict_list]
    endHookAngles = [find_row_by_name(dict['shape'])['Hook At End'] * math.pi/180 for dict in dict_list]
    startHookOrientations = [find_row_by_name(dict['shape'])['HookOrientation0']  for dict in dict_list]
    endHookOrientations = [find_row_by_name(dict['shape'])['HookOrientation1'] * math.pi/180 for dict in dict_list]
    
    return create_rebars_from_curves_and_shape(host, curves_list, norms, shapes, startHookAngles, endHookAngles, startHookOrientations, endHookOrientations, spacings, diameters, comments, bar_counts)

def create_rebarShape_rhinoCurve_from_dict(dict, plane=None):
    shapeName = dict['shape']
    if shapeName == '0':
        shapeName = "00"
    data= find_row_by_name(shapeName)
    rgName = data[0]['RhinoBaseLineType']
    params = create_rebarShapePrarams_from_dict(dict)
    return RebarShapeCurve(rgName,shapeName, plane,**params)

def create_rebar_from_dict_CAS(dict,  plane, host):
    doc = get_active_doc()

    shape = create_rebarShape_rhinoCurve_from_dict(dict, plane)
    curves = shape.curve
    norm = shape.plane.Normal
    rv_norm = convert_rhino_to_revit_geometry(norm)
    rv_curves = [convert_rhino_to_revit_geometry(curve) for curve in curves]
    rv_shape = get_rebar_shape_by_name(shape.rv_name)
    rv_type = get_rebar_type_by_diameter(float(dict['diameter']))
    rv_startHookOrientation = get_hook_orientation_from_shapename(shape.rv_name)[0]
    rv_endHookOrientation = get_hook_orientation_from_shapename(shape.rv_name)[1]
    rv_startHookType = get_hook_type_from_shapename(shape.rv_name)[0]
    rv_endHookType = get_hook_type_from_shapename(shape.rv_name)[1]
    rebar = Rebar.CreateFromCurvesAndShape(doc, rv_shape, rv_type, rv_startHookType, rv_endHookType, host, rv_norm, rv_curves, rv_startHookOrientation, rv_endHookOrientation)
    return rebar


def create_rebar_from_dict_RS(dict,  plane, host):
    doc = get_active_doc()
    shape = create_rebarShape_rhinoCurve_from_dict(dict, plane)
    rv_shape = get_rebar_shape_by_name(shape.rv_name)
    rv_type = get_rebar_type_by_diameter(dict['diameter'])
    rv_origin = convert_rhino_to_revit_geometry(shape.plane.Origin)
    rv_xVec = convert_rhino_to_revit_geometry(shape.plane.XAxis)
    rv_yVec = convert_rhino_to_revit_geometry(shape.plane.YAxis)
    rebar = Rebar.CreateFromRebarShape(doc, rv_shape, rv_type, host, rv_origin, rv_xVec, rv_yVec)
    return rebar

def create_rebar_from_C(curves, plane, host):
    doc = get_active_doc()
    rv_curves = [convert_rhino_to_revit_geometry(curve) for curve in curves]
    rv_norm = convert_rhino_to_revit_geometry(plane.Normal)
    rv_rebarStyle = None
    rv_rebarBarStyle = None
    rv_startHookType = None
    rv_endHookType =None
    rv_starthookOrientation =None
    rv_endhookOrientation =None
    useExistingShapeIfPossible = True
    createNewShape = True
    
    rebar = Rebar.CreateFromCurves(doc, rv_rebarStyle, rv_rebarBarStyle, rv_startHookType, rv_endHookType, host, rv_norm, rv_curves,rv_starthookOrientation,rv_endhookOrientation,useExistingShapeIfPossible,createNewShape)
    return rebar

def set_rebar_spacing_from_dict(rebar, dict):
    doc = get_active_doc()
    spacing = dict['spacing']
    bar_counts = dict['number']
    rv_spacing = convert_rhino_to_revit_length(spacing)
    accessor = rebar.GetShapeDrivenAccessor()
    accessor.SetLayoutAsNumberWithSpacing(bar_counts, rv_spacing)
    return rebar

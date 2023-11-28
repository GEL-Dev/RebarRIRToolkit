from utils.utils import update_params_from_dict_list, dictionary_from_csv
from rebar.rebarShape import RebarShapeCurve
from rebar.data_processor import find_row_by_name
from utils.rhinoinside_utils import convert_rhino_to_revit_geometry, get_active_doc, get_active_ui_doc, convert_rhino_to_revit_length, convert_revit_to_rhino_length
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction, Rebar, BuiltInParameter, IFailuresPreprocessor, FailureProcessingResult, BuiltInFailures, Structure, RebarCoupler, ElementId
import clr
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
        return Structure.RebarHookOrientation.Left
    elif hook_orientation == 'right' or hook_orientation == 'Right':
        return Structure.RebarHookOrientation.Right
    else:
        return None
def get_rebar_type_by_diameter(rh_diameter):
    doc = get_active_doc()
    rebar_types = FilteredElementCollector(doc).OfClass(Structure.RebarBarType).ToElements()
    for rebar_type in rebar_types:
        print(rebar_type)
        print(rebar_type.BarModelDiameter)
        rv_diameter = convert_rhino_to_revit_length(rh_diameter)
        if rebar_type.BarModelDiameter == rv_diameter:
            return rebar_type
    return None

def get_rebar_shape_by_name(name):
    doc = get_active_doc()
    rebar_shapes = [rebarShape for rebarShape in FilteredElementCollector(doc).OfClass(Structure.RebarShape).ToElements() if rebarShape.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() == name]
    if len(rebar_shapes) > 0:
        return rebar_shapes[0]
    return None

def get_hook_type_by_angle(angle):
    doc = get_active_doc()
    rebar_hook_type = [rebarHook for rebarHook in FilteredElementCollector(doc).OfClass(Structure.RebarHookType).ToElements() if abs(rebarHook.HookAngle -angle) < 0.001 ]
    if len(rebar_hook_type) > 0:
        return rebar_hook_type[0]
    return None

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

    rebar = Structure.Rebar.CreateFromCurvesAndShape(doc, rv_shape, rv_type, rv_startHookType, rv_endHookType, host, rv_norm, rv_curves, rv_startHookOrientation, rv_endHookOrientation)
    return rebar

def create_rebar_from_shape(host, diameter, shape,origin, xVec, yVec):
    doc = get_active_doc()
    rv_shape = get_rebar_shape_by_name(shape)
    rv_origin = convert_rhino_to_revit_geometry(origin)
    rv_xVec = convert_rhino_to_revit_geometry(xVec)
    rv_yVec = convert_rhino_to_revit_geometry(yVec)
    rv_type = get_rebar_type_by_diameter(diameter)

    rebar = Structure.Rebar.CreateFromRebarShape(doc, rv_shape, rv_type, host, rv_origin, rv_xVec, rv_yVec)
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
    cuplerTypes = [couplerType for couplerType in FilteredElementCollector(doc).OfClass(Structure.RebarCouplerType).ToElements() if  rebar_diameter in couplerType.get_Parameter(BuiltInParameter.ALL_MODEL_TYPE_NAME).AsString() ]
    if len(cuplerTypes) > 0:
        defaulttypeId = cuplerTypes[0].Id
        if defaulttypeId != ElementId.InvalidElementId:
            rebarData1 = Structure.RebarReinforcementData.Create(rebar.Id, 0)
            error = clr.Reference[Structure.RebarCouplerError]()
            return Structure.RebarCoupler.Create(doc, defaulttypeId, rebarData1, None, error)
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
            rebar = Structure.Rebar.CreateFromCurvesAndShape(doc, shapes[i], types[i], None, None, None, norms[i], curve, Structure.RebarHookOrientation.Right, Structure.RebarHookOrientation.Right)
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

def create_rebar_in_host(doc, host, rebar_shape, rebar_type, start_hook_type, end_hook_type, start_hook_orientation, end_hook_orientation, start_hook_extension, end_hook_extension, start_hook_angle, end_hook_angle, start_hook_radius, end_hook_radius, start_hook_length, end_hook_length, start_hook_free_length, end_hook_free_length, start_hook_bend_length, end_hook_bend_length, start_hook_extension_direction, end_hook_extension_direction, start_hook_orientation_angle, end_hook_orientation_angle, start_hook_orientation_length, end_hook_orientation_length, start_hook_orientation_direction, end_hook_orientation_direction, start_hook_orientation_bend_length, end_hook_orientation_bend_length, start_hook_orientation_bend_length_direction, end_hook_orientation_bend_length_direction, rebar_location_curve, rebar_location_curve_type, rebar_location_curve_array, rebar_location_curve_array_type, rebar_location_curve_array_normal, rebar_location_curve_array_normal_type, rebar_location_curve_array_normal_flip):
    # トランザクション開始
    t = Transaction(doc, "Create Rebar")
    t.Start()

def create_rebarShapeParams_from_csv(csv_path):
    dict_list = dictionary_from_csv(csv_path)
    params_template = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'x': None, 'y': None, 'j': None}
    updated_params_list = update_params_from_dict_list(dict_list, params_template)
    return updated_params_list

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
    endHookOrientations = [find_row_by_name(dict['shape'])['HookOrientation1'] for dict in dict_list]
    
    return create_rebars_from_curves_and_shape(host, curves_list, norms, shapes, startHookAngles, endHookAngles, startHookOrientations, endHookOrientations, spacings, diameters, comments, bar_counts)
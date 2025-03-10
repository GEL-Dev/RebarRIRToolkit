# -*- coding: utf-8 -*-
import clr
clr.AddReference("RhinoInside.Revit")
clr.AddReference('System.Core')
clr.AddReference('RevitAPI') 
clr.AddReference('RevitAPIUI')
import System
import ghpythonlib.treehelpers as th
import Autodesk
from System.Collections.Generic import List, IList
from .rebarShape import RebarShapeCurve
from .data_processor import find_row_by_name
from utils.utils import update_params_from_dict_list, dictionary_from_csv
from utils.revit_utils import get_active_doc, get_active_ui_doc
from utils.rhinoinside_utils import convert_rhino_to_revit_geometry, convert_rhino_to_revit_length, convert_revit_to_rhino_length
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory,Transaction, TransactionGroup,BuiltInParameter, IFailuresPreprocessor, FailureProcessingResult, BuiltInFailures, ElementId,Element,ElementType,Curve
from Autodesk.Revit.DB.Structure import RebarStyle, RebarFreeFormValidationResult,Rebar, RebarBarType, RebarShape, RebarHookType,RebarReinforcementData, RebarCoupler,RebarCouplerError,RebarHookOrientation,RebarConstraintsManager

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

def get_rebar_style_by_name(name):
    rebar_shape = get_rebar_shape_by_name(name)
    if rebar_shape != None:
        print(rebar_shape.RebarStyle)
        return rebar_shape.RebarStyle

def get_hook_type_by_angle(angle, style):
    doc = get_active_doc()
    rebar_hook_type = [rebarHook for rebarHook in FilteredElementCollector(doc).OfClass(RebarHookType).ToElements() if abs(rebarHook.HookAngle -angle) < 0.01 ]
    if len(rebar_hook_type) > 0:
        for hook in rebar_hook_type:
            if hook.Style == style:
                return hook
    return None

def get_hook_type_from_shapename(shapename):
    data = find_row_by_name(shapename)
    style = get_rebar_style_by_name(shapename)
    start_hook_type =get_hook_type_by_angle(float(data[0]['Hook At Start'] )* math.pi/180, style) 
    end_hook_type =  get_hook_type_by_angle(float(data[0]['Hook At End']) * math.pi/180, style) 

    return [start_hook_type, end_hook_type,style]

def get_default_coupler_type(doc, rebar, coupler_family_name):
    
    rebar_diameter = Element.Name.GetValue(doc.GetElement(rebar.GetTypeId())).replace('D',"")
    coupler_types = [coupler_type for coupler_type in FilteredElementCollector(doc).OfClass(ElementType).OfCategory(BuiltInCategory.OST_Coupler).ToElements() if (coupler_family_name + rebar_diameter) in Element.Name.GetValue(coupler_type) ] 
    if len(coupler_types) > 0:
        return coupler_types[0]
        
    return None

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

def create_rebarShape_rhinoCurve_from_dict(dict, plane=None):
    shapeName = dict['shape']
    if len(shapeName) == 1:
        shapeName = "0" + shapeName

    data= find_row_by_name(shapeName)
    rgName = data[0]['RhinoBaseLineType']
    params = create_rebarShapePrarams_from_dict(dict)
    return RebarShapeCurve(rgName,shapeName, plane,**params)

def create_rebarShape_rhinoCurves_from_dict_list(dict_list, plane_list=None):
    curves_list = []
    for i, dict in enumerate(dict_list):
        curves_list.append(create_rebarShape_rhinoCurve_from_dict(dict, plane_list[i]).curve)
    return th.list_to_tree(curves_list)

def create_rebar_coupler_data(doc, rebar, start, end, coupler_family_name):
    coupler_type = get_default_coupler_type(doc, rebar,coupler_family_name)
    if coupler_type != None:
        defaulttypeId = coupler_type.Id
        #print(defaulttypeId)
        if defaulttypeId != ElementId.InvalidElementId:
            rebarData_start =None
            rebarData_end =None
            if start:
                rebarData_start = RebarReinforcementData.Create(rebar.Id, 0)
                #print(rebarData_start)
            if end:
                rebarData_end = RebarReinforcementData.Create(rebar.Id, 1)
                #print(rebarData_end)
            error = clr.Reference[RebarCouplerError]()

            return defaulttypeId, rebarData_start, rebarData_end, error
    return None


def create_rebar_coupler_at_index(doc,rebar, start, end,coupler_family_name):
    doc = get_active_doc()
    t = Transaction(doc, 'create coupler')
    t.Start()
    data = create_rebar_coupler_data(doc,rebar, start, end, coupler_family_name)
    if data == None:
        return rebar
    type_Id, rebarData_start, rebarData_end, error = data
    #print("type_Id" , type_Id)
    #print("rebarData_start" , rebarData_start)
    #print("rebarData_end" , rebarData_end)
    if type_Id == None:
        return rebar
    if rebarData_start == None and rebarData_end == None:
        return rebar
    if rebarData_start != None:
        RebarCoupler.Create(doc, type_Id, rebarData_start, None, error)
    if rebarData_end != None:
        RebarCoupler.Create(doc, type_Id, rebarData_end, None, error)
    t.Commit()
    return rebar

def create_rebar_coupler_from_dict(doc, rebar, dict,coupler_family_name):
    start = False
    end = False
    if 'coupler_start' in dict:
        if dict['coupler_start'] == 1 or dict['coupler_start'] == "1":
            start = True
            
            
    if 'coupler_end' in dict:
        if dict['coupler_end'] == 1 or dict['coupler_end'] == "1":
            end = True
    if end is False and start is False:
        return rebar
    return create_rebar_coupler_at_index(doc,rebar, start, end,coupler_family_name)
    
def create_rebars_from_curves(curves, norms, types, shapes, pitches, a, b, c, d, e, f, g, comments, bar_numbers):
    rebars = []
    doc = get_active_doc()
    with Transaction(doc,'create_bars') as t:
        
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

def create_rebar_from_dict_CAS(doc,dict,  plane, host):
    doc = get_active_doc()
    t = Transaction(doc, 'create_bars')
    t.Start()
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
    t.Commit()
    return rebar

def create_rebar_from_curve_CAS(curves, plane, host, diameter, shapeName):
    doc = get_active_doc()
    rv_curves = [convert_rhino_to_revit_geometry(curve) for curve in curves]
    rv_norm = convert_rhino_to_revit_geometry(plane.Normal)
    rv_shape = get_rebar_shape_by_name(shapeName)
    rv_type = get_rebar_type_by_diameter(diameter)
    rebar = Rebar.CreateFromCurvesAndShape(doc, rv_shape, rv_type, None, None, host, rv_norm, rv_curves, RebarHookOrientation.Right, RebarHookOrientation.Right)
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

def set_layoutAsNumberWithSpacing(rebar, number, spacing):
    rv_spacing = convert_rhino_to_revit_length(spacing)
    if rebar == None:
        return rebar
    accessor = rebar.GetShapeDrivenAccessor()
    accessor.SetLayoutAsNumberWithSpacing(number, rv_spacing, True, True, True)
    return rebar

def set_rebar_spacing_from_dict(rebar, dict):
    doc = get_active_doc()
    t = Transaction(doc, 'edit constraints')
    t.Start()
    if rebar == None:
        return rebar
    number = 1
    spacing = 0
    if 'spacing' not in dict or 'number' not in dict:
        return rebar
    else:
        if dict['spacing'] == None or dict['spacing'] == "" or dict['spacing'] == 0:
            return rebar
        else:
            spacing = float(dict['spacing'])
        if dict['number'] == None or dict['number'] == "" or dict['number'] == 0 or dict['number'] == 1:
            return rebar
        else:
            number = int(dict['number'])
    bar_counts = int(dict['number']) 
    if bar_counts > 1 and spacing > 0:
        rebar = set_layoutAsNumberWithSpacing(rebar, bar_counts, float(dict['spacing']))
    t.Commit()
    return rebar

def set_comment(rebar, comment):
    doc = get_active_doc()
    t = Transaction(doc, 'set comment')
    t.Start()
    if rebar == None:
        return rebar
    comment_param = rebar.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
    comment_param.Set(comment)
    t.Commit()
    return rebar

def set_comment_from_dict(rebar, dict):
    if rebar == None:
        return rebar
    if 'name' not in dict or dict['name'] == None:
        return rebar
    rebar = set_comment(rebar, dict['name'])
    return rebar




def create_rebars_from_dict_CAS(dict_list, plane_list, host,coupler_family_name="CPLD"):
    doc = get_active_doc()
    rebars = []

    transaction_group = TransactionGroup(doc, "Grouped Transactions")
    transaction_group.Start()
    try:
        for i, dict in enumerate(dict_list):
            rebar = create_rebar_from_dict_CAS(doc, dict,  plane_list[i], host)
            rebar = set_rebar_spacing_from_dict(rebar, dict)
            rebar = create_rebar_coupler_from_dict(doc, rebar, dict,coupler_family_name)
            rebar = set_comment_from_dict(rebar, dict)
            if rebar != None:
                rebars.append(rebar)
        transaction_group.Assimilate()

    except Exception as e:
        # エラーが発生した場合、TransactionGroup全体をロールバック
        print("Error:", e)
        transaction_group.RollBack()
    

    return rebars

def create_rebar_from_dict_FreeForm(doc,dict,  plane, host):
    t = Transaction(doc, 'create_bars')
    t.Start()
    shape = create_rebarShape_rhinoCurve_from_dict(dict, plane)
    curves = shape.curve
    norm = shape.plane.Normal
    rv_curves_list = List[IList[Curve]]()
    space = float(dict['spacing'])
    number = int(dict['number'])
    if number <= 1:
        curve_group = List[Curve]([convert_rhino_to_revit_geometry(curve) for curve in curves])
        rv_curves_list.Add(curve_group)
    else:
        for i in range(number):
            offset_curves = []
            for curve in curves:
                distance = space * i
                offset_vector = norm * distance
                nurbs_curve = curve.ToNurbsCurve()
                transformed_nurbs_curve = nurbs_curve.Duplicate()
                transformed_nurbs_curve.Translate(offset_vector)
                offset_curves.append(transformed_nurbs_curve)
            rv_curves = List[Curve]([convert_rhino_to_revit_geometry(curve) for curve in offset_curves])
            rv_curves_list.Add(rv_curves)
    
  
    rv_type = get_rebar_type_by_diameter(float(dict['diameter']))
    rv_startHookOrientation = get_hook_orientation_from_shapename(shape.rv_name)[0]
    rv_endHookOrientation = get_hook_orientation_from_shapename(shape.rv_name)[1]
    rv_startHookType = get_hook_type_from_shapename(shape.rv_name)[0]
    rv_endHookType = get_hook_type_from_shapename(shape.rv_name)[1]
    style = get_hook_type_from_shapename(shape.rv_name)[2]
    error = clr.Reference[RebarFreeFormValidationResult]()
    rebar = Rebar.CreateFreeForm(doc, rv_type,host,rv_curves_list, error)
    if error.Value == RebarFreeFormValidationResult.Success:
        '''
        
        workshop_instuctions_param =rebar.get_Parameter(BuiltInParameter.REBAR_WORKSHOP_INSTRUCTIONS)
        if partition_param and partition is not None:
            # Number Suffixを設定
            partition_param.Set(partition)
            print(f"Updated Rebar Number Suffix for Rebar ID: {rebar.Id}")
        if workshop_instuctions_param :
            workshop_instuctions_param.Set(0)
        #rebar.set_hook_orientation(0, rv_startHookOrientation)
        #rebar.set_hook_orientation(1, rv_endHookOrientation)
        #rebar.set_hook_type(0, rv_startHookType)
        #rebar.set_hook_type(1, rv_endHookType)
        '''
        workshop_instuctions_param =rebar.get_Parameter(BuiltInParameter.REBAR_WORKSHOP_INSTRUCTIONS)
        if workshop_instuctions_param :
            workshop_instuctions_param.Set(0)
        
        if rebar != None:
            
            #rebar.get_Parameter(BuiltInParameter.REBAR_ELEM_HOOK_STYLE).Set(int(RebarStyle.StirrupTie))
            rebar.get_Parameter(BuiltInParameter.REBAR_ELEM_HOOK_STYLE).Set(int(style))

  
            try:
                rebar.SetHookOrientation(0, rv_startHookOrientation)
                rebar.SetHookOrientation(1, rv_endHookOrientation)
                
                if(rebar.CanUseHookType(rv_startHookType.Id)):
                    rebar.SetHookTypeId(0, rv_startHookType.Id)
                    print("Set Hook Type" , rv_startHookType.Id)
                if(rebar.CanUseHookType(rv_endHookType.Id)):
                    rebar.SetHookTypeId(1, rv_endHookType.Id)
                

                t.Commit()
                return rebar
            except Exception as e:
                print("Error:", e)
                t.RollBack()
                return None
    else:
        print("Failed to create rebar:", error.Value)
        t.RollBack()
        return None
    return None

    


def create_rebars_from_dict_FreeForm(dict_list, plane_list, host,coupler_family_name="CPLD"):
    doc = get_active_doc()
    transaction_group = TransactionGroup(doc, "Grouped Transactions")
    transaction_group.Start()
    rebars = []
    try:
        for i, dict in enumerate(dict_list):
            rebar = create_rebar_from_dict_FreeForm(doc, dict,  plane_list[i], host)
            rebar = create_rebar_coupler_from_dict(doc, rebar, dict,coupler_family_name)
            rebar = set_comment_from_dict(rebar, dict)
            if rebar != None:
                rebars.append(rebar)
        transaction_group.Assimilate()
        print("Success")

    except Exception as e:
        # エラーが発生した場合、TransactionGroup全体をロールバック
        print("Error:", e)
        transaction_group.RollBack()
   
    pass


    

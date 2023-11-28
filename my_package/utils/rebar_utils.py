# -*- coding: utf-8 -*-
from Autodesk.Revit.DB.Structure import Rebar, RebarBarType, RebarShape, RebarHookType
from Autodesk.Revit.DB import XYZ, ElementId,FilteredElementCollector, BuiltInCategory,BuiltInParameter

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
    # ホストの座標系を取得
    host_coordinate_system = host.GetCoordinateSystem()
    # ホストの座標系のX軸を取得
    host_coordinate_system_x = host_coordinate_system.BasisX
    # ホストの座標系のY軸を取得
    host_coordinate_system_y = host_coordinate_system.BasisY
    # ホストの座標系のZ軸を取得
    host_coordinate_system_z = host_coordinate_system.BasisZ
    # ホストの座標系の原点を取得
    host_coordinate_system_origin = host_coordinate_system.Origin
    # ホストの座標系の原点のX座標を取得
    host_coordinate_system_origin_x = host_coordinate_system_origin.X
    # ホストの座標系の原点のY座標を取得
    host_coordinate_system_origin_y = host_coordinate_system_origin.Y
    # ホストの座標系の原点のZ座標を取得
    host_coordinate_system_origin_z = host_coordinate_system_origin.Z   
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
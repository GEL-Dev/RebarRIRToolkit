# -*- coding: utf-8 -*-
from my_package.utils.rhinoinside_utils import get_active_doc, get_active_ui_doc, convert_rhino_to_revit_geometry

doc = get_active_doc()
uidoc = get_active_ui_doc()


a = convert_rhino_to_revit_geometry(x)


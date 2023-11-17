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

def load_rhinoinside():
    # RhinoInsideに関連する機能
    pass
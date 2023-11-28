"""Provides a scripting component.
    Inputs:
        _uninstall: bool:
    Output:
        message: string:  The a output variable"""

__author__ = "ykish"
__version__ = "2023.11.28"

ghenv.Component.Name = 'RebarToolkit Installer'
ghenv.Component.NickName = 'RTUninstall'

ghenv.Component.Category = 'RebarToolkit'

import clr
import os
import shutil
clr.AddReference("System")
from System import Array
import Rhino

def remove_directory(path):
    """ Remove a directory and all its contents """
    if os.path.exists(path):
        shutil.rmtree(path)
        message = "Removed directory: {}".format(path)
    else:
        message = "Directory not found: {}".format(path)
    return message

def remove_from_python_search_paths(path):
    """ Remove a path from Rhino's Python script search paths """
    current_paths = list(Rhino.Runtime.PythonScript.SearchPaths)
    if path in current_paths:
        current_paths.remove(path)
        Rhino.Runtime.PythonScript.SearchPaths = Array[str](current_paths)
        message = "Removed from Python search paths: {}".format(path)
    else:
        message = "Path not found in Python search paths: {}".format(path)
    return message


if _uninstall:
    message =[]
    print("start uninstall")
    save_dir = os.path.join(os.environ["LOCALAPPDATA"], "GEL", "RebarToolkit")
    message.append(remove_directory(save_dir))
    package_dir= os.path.join(save_dir,'my_package')
    message.append(remove_from_python_search_paths(package_dir))
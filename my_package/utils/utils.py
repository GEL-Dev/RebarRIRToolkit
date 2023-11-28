# -*- coding: utf-8 -*-
import sys
import clr
import os
import shutil
import csv
clr.AddReference("System")
from System import Array

def path_from_string(path_string):
    return os.path.abspath(path_string)

def add_path(folder_path):
    """Add a given folder path to Python's sys.path if it's not already included."""
    if folder_path not in sys.path:
        sys.path.append(folder_path)
        return "Added '{}' to sys.path".format(folder_path)
    else:
        return "'{}' already in sys.path".format(folder_path)
    
def remove_directory(path):
    """ Remove a directory and all its contents """
    if os.path.exists(path):
        shutil.rmtree(path)
        return "Removed directory: {}".format(path)
    else:
        return "Directory not found: {}".format(path)
    
def dictionary_from_csv(csv_path):
    """Read a CSV file and return a list of dictionaries of its contents."""
    with open(csv_path, 'r') as csv_file:
        # csv.DictReaderを使用してCSVファイルを読み込む
        dict_list = [row for row in csv.DictReader(csv_file)]
    return dict_list

def update_params_from_dict_list(dict_list, params_template):

    updated_params_list = []
    for d in dict_list:
        updated_params = params_template.copy()
        for key in updated_params:
            if key in d:
                updated_params[key] = None if d[key] == "" else d[key]
        updated_params_list.append(updated_params)
    
    return updated_params_list
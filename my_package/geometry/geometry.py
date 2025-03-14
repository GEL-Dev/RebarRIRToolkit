# -*- coding: utf-8 -*-
import Rhino.Geometry as rg
import System
import ghpythonlib.treehelpers as th
import math


def create_plane_from_dict(d, plane, normal):
    """Create a Rhino.Geometry.Plane object from a dictionary."""
    x = float(d["x_offset"])
    y= float(d["y_offset"])
    z = float(d["z_offset"])
    origin = plane.Origin
    xaxis = plane.XAxis
    yaxis = plane.YAxis
    zaxis = plane.ZAxis
    place_origin =origin + xaxis * x + yaxis * y + zaxis * z

    new_plane = rg.Plane(place_origin, normal)
    return new_plane

def create_plane_list_from_dict_list(dict_list, plane_list, normal_list):
    """Create a list of Rhino.Geometry.Plane objects from a list of dictionaries."""
    result_planes  = []
    len_planes = len(plane_list)
    len_normals = len(normal_list)
    print(len_planes,len_normals)
    for i, d in enumerate(dict_list):
        plane = plane_list[min(i, len_planes - 1)]
        normal = normal_list[min(i, len_normals - 1)]
        new_plane = create_plane_from_dict(d, plane, normal)
        result_planes .append(new_plane)
    return result_planes 

def create_plane_list_from_dict_list(rebar_dict_list, face_dict_list):
    """Create a list of Rhino.Geometry.Plane objects from a list of dictionaries."""
    result_planes  = []
    for rebar_dict in rebar_dict_list:

        face = int(rebar_dict["face"])
        main_axis = rebar_dict["main_axis"]
        sub_axis = rebar_dict["sub_axis"]
        x_offset = float(rebar_dict["x_offset"])
        y_offset= float(rebar_dict["y_offset"])
        z_offset = float(rebar_dict["z_offset"])

        angle_in_radians = 0
        if("angle_plane" in rebar_dict and rebar_dict["angle_plane"] is not None and rebar_dict["angle_plane"].strip() != ''):
            angle_in_radians = math.radians(float(rebar_dict["angle_plane"]))
      


        for d in face_dict_list:

            if face == int(d["i"]):

                origin = d["Pt"]
                x_axis = d["x"]
                y_axis = d["y"]
                z_axis = d["z"]

                place_origin =origin + x_axis * x_offset + y_axis * y_offset + z_axis * z_offset
                
                
                if main_axis =='x':
                    main_axis_rs = x_axis
                elif main_axis =='y':
                    main_axis_rs = y_axis
                elif main_axis =='z':
                    main_axis_rs = z_axis
                elif main_axis =='x_n':
                    main_axis_rs =  x_axis*-1
                elif main_axis =='y_n':
                    main_axis_rs =  y_axis*-1
                elif main_axis =='z_n':
                    main_axis_rs =  z_axis*-1
                else:
                    main_axis_rs = x_axis
                if sub_axis =='x':
                    sub_axis_rs = x_axis
                elif sub_axis =='y':
                    sub_axis_rs = y_axis
                elif sub_axis =='z':    
                    sub_axis_rs = z_axis 
                elif sub_axis =='x_n':
                    sub_axis_rs =  x_axis*-1
                elif sub_axis =='y_n':
                    sub_axis_rs =  y_axis*-1
                elif sub_axis =='z_n':
                    sub_axis_rs =  z_axis*-1        
                else:
                    sub_axis_rs = y_axis
            
                new_plane = rg.Plane(place_origin, main_axis_rs, sub_axis_rs)
                new_plane.Rotate(angle_in_radians, main_axis_rs)
                result_planes .append(new_plane)
    return result_planes

def offset_planes_from_dict(plane_list, rebar_dict_list, face_dict_list):
    """Offset a list of Rhino.Geometry.Plane objects."""
    offset_planes = []
    for i, plane in enumerate(plane_list):
        rebar_dict = rebar_dict_list[i]
        number =0
        spacing =0.0

         # 必須キーが存在するかの確認
        if 'number' not in rebar_dict or 'spacing' not in rebar_dict:
            print("number or spacing is not in rebar dict")
            offset_planes.append(plane)
            continue 
        
        # 数値変換可能かの確認
        try:
            number = int(rebar_dict['number'])
            spacing = float(rebar_dict['spacing'])
        except ValueError:
            print("number or spacing is not a valid integer or float")
            offset_planes.append(plane)
            continue

        if  rebar_dict['spacing'].strip() == '' or rebar_dict['number'].strip() == '':
            print("number or spacing is not an integer")
            offset_planes.append(plane)
            continue

        # 数値の範囲チェック
        if number <= 1:
            print("number value is invalid:", number)
            offset_planes.append(plane)
            continue 
        if spacing <= 0:
            print("spacing value is invalid:", spacing)
            offset_planes.append(plane)
            continue 

        
        if  rebar_dict["face"] is None or 'face' not in rebar_dict:
            print("face value is not valid or no face key")
            offset_planes.append(plane)
            continue 
        face = int(rebar_dict["face"])
        
        face_dict = next((face_dict for face_dict in face_dict_list if face_dict["i"] == face), None)
        
        if face_dict is None:
            offset_planes.append(plane)
            continue 
        z_axis_key = ["x","y","z"]
        main_axis = str(rebar_dict["main_axis"].replace("_n",""))
        sub_axis = str(rebar_dict["sub_axis"].replace("_n",""))
        z_axis_key.remove(main_axis)
        z_axis_key.remove(sub_axis)
        face_z_axis = face_dict[z_axis_key[0]]
        if face_z_axis == plane.Normal:
            offset_planes.append(plane)
            #print(face_z_axis)
            continue
           

        number = int(rebar_dict['number'])-1
        spacing = float(rebar_dict['spacing'])
        offset_vector = face_z_axis * spacing*number
        #print(offset_vector)
        new_plane = rg.Plane(plane.Origin + offset_vector, plane.XAxis, plane.YAxis)
        offset_planes.append(new_plane)
        #print(plane)
        #print(new_plane)

    return offset_planes

def offset_curve(curve, plane, number, spacing, branch_path):
    offset_curves = th.Tree[object]()
    for i in range(number):
        distance = i * spacing
        offset_vector = plane.Normal * distance
        nurbs_curve = curve.ToNurbsCurve()
        transformed_nurbs_curve = nurbs_curve.Duplicate()
        transformed_nurbs_curve.Translate(offset_vector)
        new_branch_path = branch_path.AppendElement(i)
        offset_curves.Add(transformed_nurbs_curve, new_branch_path)

    return offset_curves

def create_offset_curves_tree_from_dict_list(plane_list, curves, rebar_dict_list):
    offset_curve_tree = th.Tree[object]()
    #print(curves.BranchCount)
    for i in range(curves.BranchCount):
        _dict = rebar_dict_list[i]
        branch_path = curves.Path(i)
        number = 1
        spacing = 0
        if 'number' in _dict:
            if _dict['number'] is not None and _dict['number'].strip() != '':
                number = int(_dict['number'])
        if 'spacing' in _dict:
            if _dict['spacing'] is not None and _dict['spacing'].strip() != '':
                spacing = float(_dict['spacing'])
     
        if number < 2 or spacing is 0:
            new_branch_path = branch_path.AppendElement(0)
            for curve in curves.Branch(branch_path):
                offset_curve_tree.Add(curve, new_branch_path)
            continue
        else:
            number = int(_dict['number'])
            spacing = float(_dict['spacing'])
            plane = plane_list[i]
            for curve in curves.Branch(branch_path):
                offset_curves  = offset_curve(curve, plane, number, spacing,branch_path)
                offset_curve_tree.MergeTree(offset_curves)
    return offset_curve_tree

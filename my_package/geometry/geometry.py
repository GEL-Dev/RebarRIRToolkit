import Rhino.Geometry as rg
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
        x = rebar_dict["x_axis"]
        y = rebar_dict["y_axis"]
        x_offset = float(rebar_dict["x_offset"])
        y_offset= float(rebar_dict["y_offset"])
        z_offset = float(rebar_dict["z_offset"])

        for d in face_dict_list:

            if face == int(d["i"]):

                origin = d["Pt"]
                x_axis = d["x"]
                y_axis = d["y"]
                z_axis = d["z"]

                place_origin =origin + x_axis * x_offset + y_axis * y_offset + z_axis * z_offset
                
                
                if x =='x':
                    x_axis_rs = x_axis
                elif x =='y':
                    x_axis_rs = y_axis
                elif x =='z':
                    x_axis_rs = z_axis
                elif x =='x_n':
                    x_axis_rs =  x_axis*-1
                elif x =='y_n':
                    x_axis_rs =  y_axis*-1
                elif x =='z_n':
                    x_axis_rs =  z_axis*-1
                else:
                    x_axis_rs = x_axis
                if y =='x':
                    y_axis_rs = x_axis
                elif y =='y':
                    y_axis_rs = y_axis
                elif y =='z':    
                    y_axis_rs = z_axis 
                elif y =='x_n':
                    y_axis_rs =  x_axis*-1
                elif y =='y_n':
                    y_axis_rs =  y_axis*-1
                elif y =='z_n':
                    y_axis_rs =  z_axis*-1        
                else:
                    y_axis_rs = y_axis
            
                new_plane = rg.Plane(place_origin, x_axis_rs, y_axis_rs)
                result_planes .append(new_plane)
    return result_planes
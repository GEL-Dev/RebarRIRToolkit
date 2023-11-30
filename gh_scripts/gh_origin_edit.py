face = _rebar_dict["face"]
x = _rebar_dict["x_axis"]
y = _rebar_dict["y_axis"]

for d in _face_dict:
    if face == int(d["i"]):
        print(d)
        origin = d["Pt"]
        x_axis = d["x"]
        y_axis = d["y"]
        z_axis = d["z"]
        
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
        


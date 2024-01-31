face = _rebar_dict["face"]
main_axis = _rebar_dict["main_axis"]
sub_axis = _rebar_dict["sub_axis"]

for d in _face_dict:
    if face == int(d["i"]):
        print(d)
        origin = d["Pt"]
        main_axis = d["x"]
        y_axis = d["y"]
        z_axis = d["z"]
        
        if main_axis =='x':
            main_axis_rs = main_axis
        elif main_axis =='y':
            main_axis_rs = y_axis
        elif main_axis =='z':
            main_axis_rs = z_axis
        elif main_axis =='x_n':
            main_axis_rs =  main_axis*-1
        elif main_axis =='y_n':
            main_axis_rs =  y_axis*-1
        elif main_axis =='z_n':
            main_axis_rs =  z_axis*-1
        else:
            main_axis_rs = main_axis
        if sub_axis =='x':
            sub_axis_rs = main_axis
        elif sub_axis =='y':
            sub_axis_rs = y_axis
        elif sub_axis =='z':    
            sub_axis_rs = z_axis 
        elif sub_axis =='x_n':
            sub_axis_rs =  main_axis*-1
        elif sub_axis =='y_n':
            sub_axis_rs =  y_axis*-1
        elif sub_axis =='z_n':
            sub_axis_rs =  z_axis*-1        
        else:
            sub_axis_rs = y_axis
        


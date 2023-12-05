__author__ = "ykish"
__version__ = "2023.12.04"

import scriptcontext as sc
RebarShapeCurve = sc.sticky["RebarShapeCurve"]

length_parameters =_length_parameters.split(',')

params = {'a': None, 'b': None, 'c': None, 'd': None, 'e': None, 'f': None, 'g': None, 'h': None, 'x': None, 'y': None, 'j': None}

for param in length_parameters:
    params[param] = locals()[param]
    print(params[param])
    
curve = RebarShapeCurve(_rgLineType, p, **params).curve


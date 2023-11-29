from rebar.data_processor import find_row_by_name
from rebar.rebarShape  import RebarShapeCurve

print(name)
data= find_row_by_name(name)
print(data[0])
print(data[0]['RhinoBaseLineType'])
print(data[0]['LengthParameter'])
print(data[0]['Name'])

rgLineType = data[0]['RhinoBaseLineType']
length_parameters = data[0]['LengthParameter']
length_parameters = length_parameters.split(',')
# すべての可能なパラメータをNoneで初期化


for param in length_parameters:
    params[param] = locals()[param]
    print(params[param])
    
curve = RebarShapeCurve(rgLineType, p, **params).curve
hookAtStart =data[0]['Hook At Start'] 
hookAtEnd =data[0]['Hook At End'] 
hookOrientationStart =data[0]['HookOrientatiotion0'] 
hookOrientationEnd =data[0]['HookOrientation1'] 
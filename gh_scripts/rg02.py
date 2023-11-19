
"""Provides a scripting component.
    Inputs:
        a: length of line
        b: length of line
        plane: The base plane
    Output:
        line: The line"""

import Rhino.Geometry as rg


if a is None:
    a = 1000
    
if b is None:
    b = 1000

if plane is None:
    plane = rg.Plane.WorldXY

fromPt = rg.Point3d(0,0,0);
toPt = rg.Point3d(b,0,0);
base_line = rg.Line(fromPt,toPt)

toPt2 = rg.Point3d(b,a,0);
base_line2 = rg.Line(toPt,toPt2)



# Move the line to the plane
orient = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,plane)
base_line.Transform(orient)
base_line2.Transform(orient)
line = [base_line,base_line2]
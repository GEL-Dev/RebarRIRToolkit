import Rhino.Geometry as rg
#import scriptcontext as sc
import math
class RebarShapeCurve:
    def __init__(self,rh_name, rv_name,plane=None,a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0,x=0,y=0,j=0, radius=0, arc_angle=0):
        self.rh_name = rh_name
        self.rv_name = rv_name
        self.plane = plane
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        self.x = x
        self.y = y
        self.j = j
        self.radius = radius
        self.arc_angle = arc_angle
        self.curve =  self._create_rebarShapeCurve_in_rhino()

    def _generate_i_line(self,a):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)    
        return [base_line]
    
    def _generate_l_line(self,a,b):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a,b,0)
        base_line2 = rg.Line(toPt,toPt2)
        return [base_line,base_line2]
    def _generate_u_line(self,a,b,c):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a,b,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(a-c,b,0)
        base_line3 = rg.Line(toPt2,toPt3)
        return [base_line,base_line2,base_line3]
    
    def _generate_circle_line(self,radius,anele):
        circle = arc = rg.Arc(rg.Point3d(0,0,0),radius,math.radians(anele))
        return [circle]
    
    def _generate_rect_line(self,a,b,c,d):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a,b,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(a-c,b,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(a-c,b-d,0)
        base_line4 = rg.Line(toPt3,toPt4)
        return [base_line,base_line2,base_line3,base_line4]
    
    def _generate_wrapped_rect_line(self,a,b,c,d,e,f):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(-f,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(-f,e,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(-f+d,e,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(-f+d,e-c,0)
        base_line4 = rg.Line(toPt3,toPt4)
        toPt5 = rg.Point3d(-f+d+b,e-c,0)
        base_line5 = rg.Line(toPt4,toPt5)
        toPt6 = rg.Point3d(-f+d-b,a,0)
        base_line6 = rg.Line(toPt5,toPt6)
        return [base_line,base_line2,base_line3,base_line4,base_line5,base_line6]

    
    def _generate_c_line(self,a,b,c,d,e):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a,b,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(a-c,b,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(a-c,b-d,0)
        base_line4 = rg.Line(toPt3,toPt4)
        toPt5 = rg.Point3d(a-c+e,b-d,0)
        base_line5 = rg.Line(toPt4,toPt5)
        return [base_line,base_line2,base_line3,base_line4,base_line5]
    
    def _generate_s_line(self,a,b,c,d):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a+b,d,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(a+b+c,d,0)
        base_line3 = rg.Line(toPt2,toPt3)
        return [base_line,base_line2,base_line3]
    def _generate_s_plus_line(self,a,b,c,d,e,x):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(d,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(d+e,x,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(d+e+b,x,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(d+e+b,x-a,0)
        base_line4 = rg.Line(toPt3,toPt4)
        return [base_line,base_line2,base_line3,base_line4]
    
    def _generate_u_plus_line(self,a,b,c,d,e,f,g):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(a+b,f,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(a+b+c,f,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(a+b+c+d,f-g,0)
        base_line4 = rg.Line(toPt3,toPt4)
        toPt5 = rg.Point3d(a+b+c+d+e,f-g,0)
        base_line5 = rg.Line(toPt4,toPt5)
        return [base_line,base_line2,base_line3,base_line4,base_line5]
    
    def _generate_c_plus_line(self,a,b,c,x):
        agnle = math.asin(x/c)
        dist = math.cos(agnle)*c
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(dist,x,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(dist+b,x,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(dist+b,x-a,0)
        base_line3 = rg.Line(toPt2,toPt3)
        return [base_line,base_line2,base_line3]
    
    def _generate_c_30_angle_line(self,a,b,c,d ):
        fromPt = fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(a,0,0)
        base_line = rg.Line(fromPt,toPt)
        nextPt_x = math.cos(math.radians(30))*b
        nextPt_y = math.sin(math.radians(30))*b
        toPt2 = rg.Point3d(nextPt_x,nextPt_y,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(nextPt_x,nextPt_y+c,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(nextPt_x+d,nextPt_y+c,0)
        base_line4 = rg.Line(toPt3,toPt4)
        return [base_line,base_line2,base_line3,base_line4]
    
    def _generate_c_extended_line(self,a,b,c,d,e,x,y):
        angle = math.asin(y/e)
        dist = math.cos(angle)*e
        fromPt = fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(dist,y,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(dist,y+d,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(dist-c,y+d,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(dist-c,y+d-b,0)
        base_line4 = rg.Line(toPt3,toPt4)
        angle2 = math.asin(x/a)
        dist2 = math.cos(angle2)*a
        toPt5 = rg.Point3d(dist-c+dist2,y+d-b-x,0)
        base_line5 = rg.Line(toPt4,toPt5)
        return [base_line,base_line2,base_line3,base_line4,base_line5]
    
    def _generate_arc_curve(self,rad,angle):
        arc = rg.Arc(rg.Point3d(0,0,0),rad,math.radians(angle))
        return [arc]
        
    def _generate_l_angled_line(self,a,b,x):
        angle = math.asin(x/b)
        dist = math.cos(angle)*b
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(dist,x,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(dist+a,x,0)
        base_line2 = rg.Line(toPt,toPt2)
        return [base_line,base_line2]
    
    def _generate_triangle_line(self,b,c,d,e,g,h,x,y):
        fromPt = rg.Point3d(0,0,0)
        toPt = rg.Point3d(g,-y,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(g+e,-y,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(g+e,-y+d,0)
        base_line3 = rg.Line(toPt2,toPt3)
        toPt4 = rg.Point3d(g+e-c,-y+d,0)
        base_line4 = rg.Line(toPt3,toPt4)
        toPt5 = rg.Point3d(g+e-c,-y+d-b,0)
        base_line5 = rg.Line(toPt4,toPt5)
        toPt6 = rg.Point3d(g+e-c+x,-y+d-h,0)
        base_line6 = rg.Line(toPt5,toPt6)
        return [base_line,base_line2,base_line3,base_line4,base_line5,base_line6]
    
    def _generate_u_angled_line(self,a,b,c):
        fromPt = rg.Point3d(a,b,0)
        toPt = rg.Point3d(0,0,0)
        base_line = rg.Line(fromPt,toPt)
        toPt2 = rg.Point3d(c,0,0)
        base_line2 = rg.Line(toPt,toPt2)
        toPt3 = rg.Point3d(c-a,b,0)
        base_line3 = rg.Line(toPt2,toPt3)
        return [base_line,base_line2,base_line3]

        


    def _create_rebarShapeCurve_in_rhino(self):

        if self.rh_name=="rg01":
            base_line = self._generate_i_line(self.a)   
        elif self.rh_name=="rg02":
            base_line = self._generate_l_line(self.b,self.a)
        elif self.rh_name=="rg03":
            base_line = self._generate_u_line(self.a,self.b,self.a)
        elif self.rh_name=="rg04":
            base_line = self._generate_l_line(self.a,self.b)
        elif self.rh_name=="rg05":
            base_line = self._generate_u_line(self.b,self.a,self.c)
        elif self.rh_name=="rg06":
            base_line = self._generate_u_line(self.a,self.b,self.c)
        elif self.rh_name=="rg07":
            base_line = self._generate_circle_line(self.radius,self.arc_angle)
        elif self.rh_name=="rg08":
            base_line = self._generate_rect_line(self.a,self.b,self.c,self.d)
        elif self.rh_name=="rg09":
            base_line = self._generate_c_line(self.d,self.c,self.a,self.b,self.d)
        elif self.rh_name=="rg10":
            base_line = self._generate_c_30_angle_line(self.a,self.b,self.c,self.d)
        elif self.rh_name=="rg11":
            base_line = self._generate_s_line(self.a,self.b,self.c,self.d)
        elif self.rh_name=="rg12":
            base_line = self._generate_arc_curve(self.radius,self.arc_angle)
        elif self.rh_name=="rg13":
            base_line = self._generate_u_plus_line(self.a,self.b,self.c,self.d,self.e,self.f,self.g)
        elif self.rh_name=="rg14":
            base_line = self._generate_triangle_line(self.b,self.c,self.d,self.e,self.g,self.h,self.x,self.y)
        elif self.rh_name=="rg15":
            base_line = self._generate_c_extended_line(self.a,self.b,self.c,self.d,self.e,self.x,self.y)
        elif self.rh_name=="rg16":
            base_line = self._generate_s_plus_line(self.a,self.b,self.c,self.d,self.e,self.x)
        elif self.rh_name=="rg17":
            base_line = self._generate_wrapped_rect_line(self.a,self.b,self.c,self.d,self.e,self.f)
        elif self.rh_name=="rg18":
            base_line = self._generate_c_plus_line(self.a,self.b,self.c,self.x)
        elif self.rh_name=="rg19":
            base_line = self._generate_l_angled_line(self.a,self.b,self.x)
        elif self.rh_name=="rg20":
            base_line = self._generate_s_line(self.c,self.e,self.a,self.x)
        elif self.rh_name=="rg21":
            base_line = self._generate_u_angled_line(self.a,self.b,self.c)
       
        lines = []

        if self.plane is None:
            self.plane = rg.Plane.WorldXY
        if base_line is None:
            base_line = rg.Line(rg.Point3d(0,0,0),rg.Point3d(1000,0,0))
            

        for line in base_line:
            orient = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,self.plane)
            line.Transform(orient)
            lines.append(line)
        
        return lines
    

    #sc.sticky["RebarShapeCurve"] = RebarShapeCurve
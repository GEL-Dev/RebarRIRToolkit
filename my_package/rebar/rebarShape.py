import Rhino.Geometry as rg

class RebarShapeCurve:
    def __init__(self,name,plane=None,a=0,b=0,c=0,d=0,e=0,f=0,g=0,h=0,x=0,y=0,j=0):
        self.name = name
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
    
    def _generate_circle_line(self,a):
        circle = rg.Circle(rg.Point3d(0,0,0),a)
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

    
    def _create_rebarShapeCurve_in_rhino(self):

        if self.name=="rg01":
            base_line = self._generate_i_line(self.a)   
        elif self.name=="rg02":
            base_line = self._generate_l_line(self.b,self.a)
        elif self.name=="rg03":
            base_line = self._generate_u_line(self.a,self.b,self.a)
        elif self.name=="rg04":
            base_line = self._generate_l_line(self.a,self.b)
        elif self.name=="rg05":
            base_line = self._generate_u_line(self.b,self.a,self.c)
        elif self.name=="rg06":
            base_line = self._generate_u_line(self.a,self.b,self.c)
        elif self.name=="rg07":
            base_line = self._generate_circle_line(self.a)
        elif self.name=="rg08":
            base_line = self._generate_rect_line(self.d,self.a,self.b,self.c)
        elif self.name=="rg09":
            base_line = self._generate_c_line(self.d,self.c,self.a,self.b,self.d)
        elif self.name=="rg10":
            pass
        elif self.name=="rg11":
            pass
        elif self.name=="rg12":
            pass
        elif self.name=="rg13":
            pass
        elif self.name=="rg14":
            pass
        elif self.name=="rg15":
            pass
        elif self.name=="rg16":
            pass
        elif self.name=="rg17":
            pass
        elif self.name=="rg18":
            pass
        elif self.name=="rg19":
            pass
        
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
    
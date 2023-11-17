import rhinoscriptsyntax as rs

class SphereGenerator:
    def create_sphere(self, center, radius):
        return rs.AddSphere(center, radius)
import numpy as np


class SphereIntersections:

    def __init__(self):
        pass


    def get_intersections(self, sphere_1:tuple, sphere_2:tuple, sphere_3:tuple, sphere_4:tuple):
        #  each sphere_n tuple should define a circle: (radius, center_x, center_y)

        r1, x1, y1, z1 = sphere_1
        r2, x2, y2, z2 = sphere_2
        r3, x3, y3, z3 = sphere_3
        r4, x4, y4, z4 = sphere_4

        A = 2*(x2-x1)
        B = 2*(y2-y1)
        C = 2*(z2-z1)
        D = r1**2-r2**2-x1**2+x2**2-y1**2+y2**2-z1**2+z2**2

        E = 2*(x3-x2)
        F = 2*(y3-y2)
        G = 2*(z3-z2)
        H = r2**2-r3**2-x2**2+x3**2-y2**2+y3**2-z2**2+z3**2

        J = 2*(x4-x3)
        K = 2*(y4-y3)
        L = 2*(z4-z3)
        M = r3**2-r4**2-x3**2+x4**2-y3**2+y4**2-z3**2+z4**2

        return np.linalg.inv([[A, B, C], [E, F, G], [J, K, L]])@[[D], [H], [M]]
    
    
    
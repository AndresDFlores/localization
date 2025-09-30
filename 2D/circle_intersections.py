import numpy as np


class CircleIntersections:

    def __init__(self):
        pass


    def get_intersections(self, circ_1:tuple, circ_2:tuple, circ_3:tuple):
        #  each circ_n tuple should define a circle: (radius, center_x, center_y)

        r1, x1, y1 = circ_1
        r2, x2, y2 = circ_2
        r3, x3, y3 = circ_3

        A = 2*(x2-x1)
        B = 2*(y2-y1)
        C = r1**2-r2**2-x1**2+x2**2-y1**2+y2**2

        D = 2*(x3-x2)
        E = 2*(y3-y2)
        F = r2**2-r3**2-x2**2+x3**2-y2**2+y3**2

        return np.linalg.inv([[A, B], [D, E]])@[[C], [F]]


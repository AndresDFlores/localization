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



if __name__=="__main__":

    import matplotlib.pyplot as plt


    #  circle definitions
    r1, a1, b1 = (3.16, 7, 1)
    r2, a2, b2 = (9.43, 13, 12)
    r3, a3, b3 = (10.63, 1, 12)


    #  define domain in degrees
    theta = np.arange(0,360,.01)


    #  circle 1 points
    circ1_x = r1*np.cos(theta)+a1
    circ1_y = r1*np.sin(theta)+b1


    #  circle 2 points
    circ2_x = r2*np.cos(theta)+a2
    circ2_y = r2*np.sin(theta)+b2


    #  circle 3 points
    circ3_x = r3*np.cos(theta)+a3
    circ3_y = r3*np.sin(theta)+b3


    circ_ints_class = CircleIntersections()


    #  three-circle intersection linear algebra
    intersection = circ_ints_class.get_intersections_linalg(
        circ_1=(r1,a1,b1), 
        circ_2=(r2,a2,b2),
        circ_3=(r3,a3,b3),
    )

    print(intersection[0], intersection[-1])

    fig, ax = plt.subplots()
    ax.plot(circ1_x, circ1_y, '.', 'b', ms=1)
    ax.plot(circ2_x, circ2_y, '.', 'g', ms=1)
    ax.plot(circ3_x, circ3_y, '.', 'o', ms=1)
    ax.plot(intersection[0], intersection[-1], marker='.', fillstyle='none', linestyle='none', ms=25, color='r')
    ax.set_aspect('equal', adjustable='box')
    plt.show()

    
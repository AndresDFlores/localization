import numpy as np
import matplotlib.pyplot as plt

from circle_intersections import *
from plotter import *


class TrilaterationLocalization:


    @classmethod
    def set_circle_count(cls, circle_count):
        cls.circle_count=circle_count


    def __init__(self, iter:int):

        self.iter=iter

        #  initialize vars
        self.set_circle_count(circle_count=2)
        self.circle_intersections_class = CircleIntersections()

        #  initalize plots
        self.plot_spheres_class = PlotSpheres()


    def localize(self, circles:list):
        #  'circles' input should be a list of tuples
        #  each tuple should define a circle: (radius, center_x, center_y, center_z)

        self.plot_spheres_class.plot_spheres(spheres=circles)

        self.intersection = self.circle_intersections_class.get_intersections(
            circ_1=circles[0],
            circ_2=circles[1],
            circ_3=circles[2],
            circ_4=circles[3]
        )


    def main(self, circles, title):

        #  indicate how many circles have been defined by input
        self.set_circle_count(circle_count=len(circles))
        self.localize(circles)


        #  plot spheres and intersection
        self.plot_spheres_class.format_plots()
        self.plot_spheres_class.plot_intersection(self.intersection)
        self.plot_spheres_class.save_plots(iter=self.iter)
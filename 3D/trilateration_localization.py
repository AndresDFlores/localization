import numpy as np
import matplotlib.pyplot as plt

from sphere_intersections import *
from plotter import *


class TrilaterationLocalization:

    sphere_colors = ['dodgerblue', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']


    @classmethod
    def set_circle_count(cls, circle_count):
        cls.circle_count=circle_count


    def __init__(self, iter:int):

        self.iter=iter

        #  initialize vars
        self.set_circle_count(circle_count=2)
        self.circle_intersections_class = SphereIntersections()

        #  initalize plots
        self.plot_spheres_class = PlotSpheres()


    def localize(self, spheres:list):
        #  'spheres' input should be a list of tuples
        #  each tuple should define a circle: (radius, center_x, center_y, center_z)


        for idx, sphere in enumerate(spheres):
            sphere_color=self.sphere_colors[idx]
            self.plot_spheres_class.set_color(color=sphere_color)
            self.plot_spheres_class.plot_spheres(sphere)


        self.intersection = self.circle_intersections_class.get_intersections(
            sphere_1=spheres[0],
            sphere_2=spheres[1],
            sphere_3=spheres[2],
            sphere_4=spheres[3]
        )


    def main(self, spheres, title):

        #  indicate how many spheres have been defined by input
        self.set_circle_count(circle_count=len(spheres))
        self.localize(spheres)


        #  plot spheres and intersection
        self.plot_spheres_class.format_plots()
        self.plot_spheres_class.plot_intersection(self.intersection)
        self.plot_spheres_class.save_plots(iter=self.iter)
import numpy as np
import matplotlib.pyplot as plt

from circle_intersections import *
from plotter import *


class TrilaterationLocalization:

    circle_colors=['dodgerblue', 'green', 'orange', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']


    def __init__(self, iter:int):

        self.iter=iter

        #  initialize vars
        self.circle_intersections_class = CircleIntersections()

        #  initialize plots
        self.plot_circles_class = PlotCircles()


    def localize(self, circles:list):
        #  'circles' input should be a list of tuples
        #  each tuple should define a circle: (radius, center_x, center_y)


        for idx, circle in enumerate(circles):
            circle_color = self.circle_colors[idx]
            self.plot_circles_class.set_color(color=circle_color)
            self.plot_circles_class.plot_circles(circle=circle)


        self.intersection = self.circle_intersections_class.get_intersections(
            circ_1=circles[0],
            circ_2=circles[1],
            circ_3=circles[2]
        )      


    def main(self, circles, title):

        #  localize tag from circle intersections
        self.localize(circles)


        #  plot circles and intersection
        self.plot_circles_class.plot_intersection(self.intersection)
        self.plot_circles_class.format_plots()
        self.plot_circles_class.save_plots(iter=self.iter)
        
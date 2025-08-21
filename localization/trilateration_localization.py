import numpy as np
import matplotlib.pyplot as plt

from circle_intersections import *


class TrilaterationLocalization:


    @classmethod
    def set_circle_count(cls, circle_count):
        cls.circle_count=circle_count


    def __init__(self):

        #  initialize vars
        self.set_circle_count(circle_count=2)
        self.circle_intersections_class = CircleIntersections()


        #  initialize plots
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='box')

        # Draw the major grid (optional, for comparison)
        self.ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')

        # Draw the minor grid
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')



    def plot_circles(self, circles:list):

        for circle in circles:

            radius = circle[0]
            center_x = circle[1]
            center_y = circle[2]

            #  define domain in degrees
            theta = np.arange(0,360,.01)

            #  circle points
            circ_x = radius*np.cos(theta)+center_x
            circ_y = radius*np.sin(theta)+center_y

            self.ax.plot(center_x, center_y, marker='+', color='green')
            self.ax.scatter(circ_x, circ_y, color='green', s=0.1)

            self.ax.text(center_x, center_y, f'({center_x}, {center_y})', ha='left', va='bottom', size=8, weight='bold')



    def localize(self, circles:list):
        #  'circles' input should be a list of tuples
        #  each tuple should define a circle: (radius, center_x, center_y)

        intersection = self.circle_intersections_class.get_intersections(
            circ_1=circles[0],
            circ_2=circles[1],
            circ_3=circles[2]
        )

        self.ax.scatter(intersection[0], intersection[-1], color='red')
        self.ax.plot(intersection[0], intersection[-1], marker='o', markerfacecolor='none', markeredgecolor='red', markersize=20)
        self.ax.text(
            intersection[0], intersection[-1]+1, 
            f'({round(*intersection[0], 2)}, {round(*intersection[-1], 2)})', 
            ha='left', va='bottom', size=8, weight='bold', color='red')       


    def main(self, circles, title):

        #  indicate how many circles have been defined by input
        self.set_circle_count(circle_count=len(circles))
        self.plot_circles(circles)
        self.localize(circles)

        plt.savefig(f'localization_figs/test_{title}.png', dpi=500)

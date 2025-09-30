import os
import matplotlib.pyplot as plt
import numpy as np


class PlotCircles():

    @classmethod
    def set_color(cls, color):
        cls.color=color


    def __init__(self):

        #  initialize plots
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='box')


    def plot_circles(self, circle:tuple):

        #  Define the circle
        (r, x0, y0) = circle

        #  define domain in degrees
        theta = np.arange(0,360,.01)

        #  circle points
        circ_x = r*np.cos(theta)+x0
        circ_y = r*np.sin(theta)+y0

        self.ax.plot(x0, y0, marker='+', color=self.color)
        self.ax.scatter(circ_x, circ_y, color=self.color, s=0.1)
        self.ax.text(x0, y0+1, f'({x0}, {y0})', ha='left', va='bottom', size=8, weight='bold')


    def plot_intersection(self, intersection:tuple):

        #  plot the intersection point relative to the intersecting circles
        self.ax.scatter(intersection[0], intersection[-1], color='red')
        self.ax.plot(intersection[0], intersection[-1], marker='o', markerfacecolor='none', markeredgecolor='red', markersize=20)

        #  label intersection point
        self.ax.text(
            *intersection[0], *intersection[-1]+1, 
            f'({round(*intersection[0], 2)}, {round(*intersection[-1], 2)})', 
            ha='left', va='bottom', size=8, weight='bold', color='red')
        
        #  generate a title that indicates the intersection point of the circles
        plot_title = f'Tag Location: ({intersection[0][0]:.2f}, {intersection[1][0]:.2f})'
        self.ax.set_title(plot_title)


    def format_plots(self):# Set labels for the axes

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')

        # Draw the major grid (optional, for comparison)
        self.ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')

        # Draw the minor grid
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')


    def save_plots(self, iter):

        title=os.path.join('localization_figs', f'test_{iter}')
        plt.savefig(f'{title}.png', dpi=500)


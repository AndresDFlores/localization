import os
import matplotlib.pyplot as plt
import numpy as np


class PlotSpheres():

    @classmethod
    def set_color(cls, color):
        cls.color=color


    def __init__(self):

        #  initialize figure and add 3D subplot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')
        self.set_color(color='blue')


    def plot_spheres(self, sphere:tuple):

        #  Define the sphere
        (r, x0, y0, z0) = sphere


        # Generate spherical coordinates: u for azimuth, v for elevation
        u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]  # creates a 2D meshgrid


        # Convert spherical coordinates to Cartesian coordinates
        x = r * np.cos(u) * np.sin(v) + x0
        y = r * np.sin(u) * np.sin(v) + y0
        z = r * np.cos(v) + z0


        # Plot the surface of the sphere
        self.ax.plot_surface(x, y, z, alpha=0.2, color=self.color)


    def plot_intersection(self, intersection:tuple):

        #  plot the intersection point relative to the intersecting spheres
        self.ax.scatter(*intersection, color='red')
        self.ax.plot(intersection[0], intersection[1], intersection[2], marker='o', markerfacecolor='none', markeredgecolor='red', markersize=20)

        #  label intersection point
        self.ax.text(
            *intersection[0], *intersection[1]+1, *intersection[2], 
            f'({round(*intersection[0], 2)}, {round(*intersection[1], 2)}, {round(*intersection[2], 2)})', 
            ha='left', va='bottom', size=8, weight='bold', color='red')

        #  generate a title that indicates the intersection point of the spheres
        plot_title = f'Tag Location: ({intersection[0][0]:.2f}, {intersection[1][0]:.2f}, {intersection[2][0]:.2f})'
        self.ax.set_title(plot_title)


    def format_plots(self):# Set labels for the axes

        axis_lims = [0, 10]

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.ax.set_xlim(axis_lims)
        self.ax.set_ylim(axis_lims)
        self.ax.set_zlim(axis_lims)

        # Draw the major grid (optional, for comparison)
        self.ax.grid(which='major', linestyle='-', linewidth='0.5', color='black')

        # Draw the minor grid
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        # # Ensure equal aspect ratio for a true spherical appearance
        self.ax.set_box_aspect([np.ptp(np.arange(*axis_lims)), np.ptp(np.arange(*axis_lims)), np.ptp(np.arange(*axis_lims))])


    def save_plots(self, iter):

        title=os.path.join('localization_figs', f'test_{iter}')
        plt.savefig(f'{title}.png', dpi=500)


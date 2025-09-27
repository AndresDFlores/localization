import os
import matplotlib.pyplot as plt
import numpy as np


class PlotSpheres():

    def __init__(self):

        # Initialize figure and add 3D subplot
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')


    def plot_spheres(self, spheres:list):

        for sphere in spheres:

            #  Define the sphere
            (r, x0, y0, z0) = sphere


            # Generate spherical coordinates: u for azimuth, v for elevation
            u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]  # creates a 2D meshgrid


            # Convert spherical coordinates to Cartesian coordinates
            x = r * np.cos(u) * np.sin(v) + x0
            y = r * np.sin(u) * np.sin(v) + y0
            z = r * np.cos(v) + z0


            # Plot the surface of the sphere
            self.ax.plot_surface(x, y, z, alpha=0.2)


    def plot_intersection(self, intersection:tuple):
        self.ax.scatter(*intersection)


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
        plt.savefig(f'{title}.png', dpi=300)



if __name__=="__main__":

    #  sample data
    spheres = [
        (4, 2, 3, 5),
        (4, 6, 7, 8),
        (4, 6, 5, 2),
        (4, 8, 8, 6)
    ]

    plot_spheres_class = PlotSpheres()
    plot_spheres_class.plot_spheres(spheres)
    plot_spheres_class.format_plots()


    # Display the plot
    plt.show()
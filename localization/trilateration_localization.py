from operator import itemgetter

import numpy as np
from sklearn.cluster import DBSCAN
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


            #  circle 1 points
            circ1_x = radius*np.cos(theta)+center_x
            circ1_y = radius*np.sin(theta)+center_y

            self.ax.plot(center_x, center_y, marker='+', color='green')
            self.ax.scatter(circ1_x, circ1_y, color='green', s=0.1)

            self.ax.text(center_x, center_y, f'({center_x}, {center_y})', ha='left', va='bottom', size=8, weight='bold')



    def get_anchor_intersections(self, circles:list):

        #  get intersection of all defined circles
        all_intersections = []
        for focus_idx, focus_anchor in enumerate(circles):
            for neighbor_idx, neighbor_anchor in enumerate(circles):

                if focus_idx!=neighbor_idx:
                    intersection_points = self.circle_intersections_class.get_intersections(focus_anchor, neighbor_anchor)
                    all_intersections.extend(intersection_points)

        return all_intersections



    def localize(self, circles:list):
        #  'circles' input should be a list of tuples
        #  each tuple should define a circle: (radius, center_x, center_y)

        self.intersections = self.get_anchor_intersections(circles)

        x = list(map(itemgetter(0),self.intersections))
        y = list(map(itemgetter(1),self.intersections))

        self.ax.scatter(x, y, color='orange')



    def cluster(self, X):

        X = [[*x] for x in X]
        cluster_min = 2*self.circle_count  # confirm that this calculation properly defines/constrains the cluster
        dbscan = DBSCAN(eps=1, min_samples=cluster_min)

        clusters = dbscan.fit(X)
        labels = clusters.labels_

        clusters_by_label=[]
        for idx, label in enumerate(labels):
            if label != -1:
                clusters_by_label.append(X[idx])


        cluster_x = list(map(itemgetter(0), clusters_by_label))
        cluster_y = list(map(itemgetter(-1), clusters_by_label))

        mean_cluster_x = np.average(cluster_x)
        mean_cluster_y = np.average(cluster_y)

        self.ax.plot(mean_cluster_x, mean_cluster_y, marker='+', markeredgecolor='red')
        self.ax.plot(mean_cluster_x, mean_cluster_y, marker='o', markerfacecolor='none', markeredgecolor='red', markersize=20)

        self.ax.text(
            mean_cluster_x, mean_cluster_y+1, 
            f'({round(mean_cluster_x, 2)}, {round(mean_cluster_y, 2)})', 
            ha='left', va='bottom', size=8, weight='bold', color='red')
        


    def main(self, circles, title):

        #  indicate how many circles have been defined by input
        self.set_circle_count(circle_count=len(circles))

        self.plot_circles(circles)
        self.localize(circles)
        self.cluster(self.intersections)

        plt.savefig(f'localization_figs/test_{title}.png', dpi=500)

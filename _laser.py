"""
Opis modula: klasa za stvaranje laserske ravnine i potrebne funckije

"""

import _matrices
import _homogeneus
import matplotlib.pyplot as plt
import numpy as np


# Laser plane class
class LaserPlane:

    def __init__(
            self,
            origin,
            dy,
            fi,
            length
    ):
        self.origin = origin  # origin of the laser
        self.dy = dy  # y-axis of the laser
        self.fi = fi  # the angle of propagation of the laser beam of light
        self.length = length  # laser length (the distance from the laser beam and a straight object
        self.dy1 = _matrices.get_rotation_matrix(
            theta_z=self.fi / 2) @ self.dy  # dy1, dy2 - vectors between y-xis determined by the angle of propagation
        self.dy2 = _matrices.get_rotation_matrix(theta_z=-self.fi / 2) @ self.dy

    def draw3D_plane(self):
        ax = plt.gca()
        laser_plane = np.c_[
            self.origin,
            self.origin + (self.length/np.cos(self.fi/2)) * self.dy1,
            self.origin + (self.length/np.cos(-self.fi/2)) * self.dy2,
            self.origin
        ]
        ax.plot(*laser_plane, color="red")
        return ax

    # Function to get the laser points at the end of the laser plane
    def get_points(self, n):
        list_points = []
        T1 = self.origin + (self.length/np.cos(self.fi/2)) * self.dy1
        T2 = self.origin + (self.length/np.cos(-self.fi/2)) * self.dy2
        list_points.append(T1)
        s = T2 - T1  # T1T2
        r1 = T1  # OT1
        ds = 1 / (n - 1)

        for i in range(0, n - 1):
            r = r1 + ds * s
            list_points.append(r)
            ds = ds + 1 / (n - 1)

        points = np.asarray(list_points)

        return points

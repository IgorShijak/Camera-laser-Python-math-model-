# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:34:17 2022

@author: igors

Opis modula: služi za crtanje ravnine slike u 3D prostoru i 2D-u
"""

import matplotlib.pyplot as plt
import numpy as np
from _matrices import get_plane_from_three_points
from _matrices import get_plucker_matrix
from _homogeneus import to_inhomogeneus


class Image:
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def draw(self, color="tab:gray", ax=None):
        if ax is None:
            ax = plt.gca()

        ax.grid(color=color)
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        return ax


class ImagePlane:
    def __init__(
            self,
            origin,
            dx,
            dy,
            dz,
            width,
            height,
            C,
            camera_fov_length
    ):
        self.origin = origin
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.width = width
        self.height = height
        self.C = C
        self.camera_fov_length = camera_fov_length
        self.pi = get_plane_from_three_points(origin, origin + dx, origin + dy)

    def draw3D(self, color="tab:gray", alpha=0.5, ax=None):
        if ax is None:
            ax = plt.gca()

        xticks = np.linspace(0, self.width, num=round(self.width + 1)).reshape(-1, 1) * self.dx
        yticks = np.linspace(0, self.height, num=round(self.height + 1)).reshape(-1, 1) * self.dy
        pts = (self.origin + xticks).reshape(-1, 1, 3) + yticks
        pts = pts.reshape(-1, 3)
        shape = len(xticks), len(yticks)
        X = pts[:, 0].reshape(shape)
        Y = pts[:, 1].reshape(shape)
        Z = pts[:, 2].reshape(shape)
        frame = np.c_[
            self.origin,
            self.origin + self.dx * self.width,
            self.origin
            + self.dx * self.width
            + self.dy * self.height,
            self.origin + self.dy * self.height,
            self.origin,
        ]

        camera_reach = self.C + self.camera_fov_length * self.dz  # center point of the camera reach
        pi_camera_fov = get_plane_from_three_points(camera_reach,
                                                    camera_reach + self.dx,
                                                    camera_reach + self.dy)  # the camera reach plane

        camera_fov = []

        for i in range(np.shape(frame)[1]):
            L = get_plucker_matrix(self.C.T, frame[:, i])
            camera_fov_point = to_inhomogeneus(L @ pi_camera_fov)
            line = np.c_[self.C.T, camera_fov_point]
            ax.plot(*line, color="blue")
            camera_fov.append(camera_fov_point)

        camera_fov = np.asarray(camera_fov).reshape(-1, 3).T

        frame_midpoint1 = (self.origin + self.origin + self.dx * self.width)/2
        frame_midpoint2 = (self.origin + self.origin + self.dy * self.height)/2
        L1 = get_plucker_matrix(self.C.T, frame_midpoint1)
        L2 = get_plucker_matrix(self.C.T, frame_midpoint2)
        fov_midpoint1 = to_inhomogeneus(L1 @ pi_camera_fov)
        fov_midpoint2 = to_inhomogeneus(L2 @ pi_camera_fov)
        l1 = int(np.round(np.linalg.norm(camera_fov[:, 1] - camera_fov[:, 0])))
        l2 = int(np.round(np.linalg.norm(camera_fov[:, 3] - camera_fov[:, 0])))

        ax.plot(*camera_fov, color="blue")
        ax.plot(*frame, color="black")
        ax.plot_wireframe(X, Y, Z, color=color, alpha=alpha)
        ax.text(*fov_midpoint1, str(l1) + ' mm')
        ax.text(*fov_midpoint2, str(l2) + ' mm')
        return ax

    def draw3D_without_fov(self, color="tab:gray", alpha=0.5, ax=None):
        if ax is None:
            ax = plt.gca()

        xticks = np.linspace(0, self.width, num=round(self.width + 1)).reshape(-1, 1) * self.dx
        yticks = np.linspace(0, self.height, num=round(self.height + 1)).reshape(-1, 1) * self.dy
        pts = (self.origin + xticks).reshape(-1, 1, 3) + yticks
        pts = pts.reshape(-1, 3)
        shape = len(xticks), len(yticks)
        X = pts[:, 0].reshape(shape)
        Y = pts[:, 1].reshape(shape)
        Z = pts[:, 2].reshape(shape)
        frame = np.c_[
            self.origin,
            self.origin + self.dx * self.width,
            self.origin
            + self.dx * self.width
            + self.dy * self.height,
            self.origin + self.dy * self.height,
            self.origin,
        ]

        ax.plot(*frame, color="black")
        ax.plot_wireframe(X, Y, Z, color=color, alpha=alpha)
        return ax

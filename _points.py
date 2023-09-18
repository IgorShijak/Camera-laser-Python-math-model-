# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 02:46:54 2022

@author: igors

Opis modula: klasa koja sadrži funkcije za crtanje točaka u 3D prostoru i projiciranje tih točaka na sliku kamere
"""

import matplotlib.pyplot as plt
import numpy as np

from _homogeneus import to_homogeneus, to_inhomogeneus
from _matrices import get_plucker_matrix, get_projection_matrix, get_projection_matrix_2


# Calculate 2D laser points in pixels from 3D points in mm
def calculate_2D(
        point,
        f,
        px=0.0,
        py=0.0,
        pw=1.0,
        ph=1.0,
        C=(0.0, 0.0, 0.0),
        theta_x=0.0,
        theta_y=0.0,
        theta_z=0.0
):
    P = get_projection_matrix(
        f,
        px=px,
        py=py,
        pw=pw,
        ph=ph,
        theta_x=theta_x,
        theta_y=theta_y,
        theta_z=theta_z,
        C=C,
    )

    x = to_inhomogeneus(P @ to_homogeneus(point))

    return x


# Calculate 2D laser points in pixels from 3D points in mm with camera lens distortion
def calculate_2D_with_distortion(
        point,
        k1,
        k2,
        k3,
        p1,
        p2,
        px,
        py,
        f,
        pw,
        ph
):

    x_n = (point[0] - px)/(f/pw)
    y_n = (point[1] - py)/(f/ph)
    r2 = x_n**2 + y_n**2

    x_dist = x_n*(1 + k1*r2 + k2*(r2**2) + k3*(r2**3)) + (2*p1*x_n*y_n + p2*(r2 + 2*(x_n**2)))
    y_dist = y_n*(1 + k1*r2 + k2*(r2**2) + k3*(r2**3)) + (p1*(r2 + 2*(y_n**2)) + 2*p2*x_n*y_n)

    x_d = (x_dist * (f/pw)) + px
    y_d = (y_dist * (f/ph)) + py

    point_dist = np.array([x_d, y_d])

    return point_dist


# Calculate 2D laser points in pixels from 3D points in mm with a camera matrix loaded from a txt file
def calculate_2D_w_camera_matrix(
        point,
        K,
        C=(0.0, 0.0, 0.0),
        theta_x=0.0,
        theta_y=0.0,
        theta_z=0.0,
):
    P = get_projection_matrix_2(
        K,
        theta_x=theta_x,
        theta_y=theta_y,
        theta_z=theta_z,
        C=C,
    )

    x = to_inhomogeneus(P @ to_homogeneus(point))

    return x


# Functions used to plot the points
def draw3D(
        point,
        pi,
        C=(0.0, 0.0, 0.0),
        s=20.0,
        color="tab:green",
        ax=None
):
    if ax is None:
        ax = plt.gca()

    L = get_plucker_matrix(np.asarray(C), point)
    x = to_inhomogeneus(L @ pi)
    ax.scatter3D(*point, s=s, color=color)
    # ax.scatter3D(*x, s=s, color=color)
    # ax.plot(*np.c_[C, self.values], color="tab:gray", alpha=0.5, ls="--")

    return ax


def draw3D_projected(
        point,
        pi,
        C=(0.0, 0.0, 0.0),
        s=20.0,
        color="tab:green",
        ax=None,
):
    if ax is None:
        ax = plt.gca()

    L = get_plucker_matrix(np.asarray(C), point)
    x = to_inhomogeneus(L @ pi)
    ax.scatter3D(*x, s=s, color=color)

    return ax


def draw(x, ax=None, s=20.0, color="tab:green"):
    if ax is None:
        ax = plt.gca()

    ax.scatter(*x, s=s, color=color)

    return ax


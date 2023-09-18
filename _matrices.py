# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 18:26:36 2022

@author: igors

Opis modula: matrice rotacija, kalibracije, projekcije i ostale potrebne matrice
"""

import numpy as np
from _homogeneus import to_homogeneus


# Plucker matrix
def get_plucker_matrix(A, B):
    A = to_homogeneus(A)
    B = to_homogeneus(B)
    L = A.reshape(-1, 1) * B.reshape(1, -1) - B.reshape(-1, 1) * A.reshape(1, -1)
    return L


# Roll matrix Rx
def _get_roll_matrix(theta_x):
    Rx = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, np.cos(theta_x), -np.sin(theta_x)],
            [0.0, np.sin(theta_x), np.cos(theta_x)]
        ]
    )
    return Rx


# Pitch matrix Ry
def _get_pitch_matrix(theta_y):
    Ry = np.array(
        [
            [np.cos(theta_y), 0.0, np.sin(theta_y)],
            [0.0, 1.0, 0.0],
            [-np.sin(theta_y), 0.0, np.cos(theta_y)]
        ]
    )
    return Ry


# Yaw matrix Rz
def _get_yaw_matrix(theta_z):
    Rz = np.array(
        [
            [np.cos(theta_z), -np.sin(theta_z), 0.0],
            [np.sin(theta_z), np.cos(theta_z), 0.0],
            [0.0, 0.0, 1.0]
        ]
    )
    return Rz


# Rotation matrix
def get_rotation_matrix(theta_x=0.0, theta_y=0.0, theta_z=0.0):
    # Roll matrix
    Rx = _get_roll_matrix(theta_x)
    # Pitch matrix
    Ry = _get_pitch_matrix(theta_y)
    # Yaw matrix
    Rz = _get_yaw_matrix(theta_z)
    return Rz @ Ry @ Rx


# Calibration matrix
def get_calibration_matrix(
        f,
        px=0.0,
        py=0.0,
        pw=1.0,
        ph=1.0
):
    K = np.array([[f/pw, 0.0, px/pw], [0.0, f/ph, py/ph], [0.0, 0.0, 1.0]])
    return K


# Projection matrix - ideal
def get_projection_matrix(
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
    K = get_calibration_matrix(f=f, px=px, py=py, pw=pw, ph=ph)
    R = get_rotation_matrix(theta_x=theta_x, theta_y=theta_y, theta_z=theta_z).T
    P = K @ R @ np.c_[np.eye(3), -np.asarray(C)]
    return P


# Projection matrix with real calibration matrix
def get_projection_matrix_2(
        K,
        C=(0.0, 0.0, 0.0),
        theta_x=0.0,
        theta_y=0.0,
        theta_z=0.0,
):
    R = get_rotation_matrix(theta_x=theta_x, theta_y=theta_y, theta_z=theta_z).T
    P = K @ R @ np.c_[np.eye(3), -np.asarray(C)]
    return P


# Calculate the plane equation from three points
def get_plane_from_three_points(X1, X2, X3):
    pi = np.hstack([np.cross(X1 - X3, X2 - X3), -X3 @ np.cross(X1, X2)])
    return pi
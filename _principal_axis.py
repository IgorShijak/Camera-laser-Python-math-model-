# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 01:10:29 2022

@author: igors

Opis modula: klasa i funkcija za crtanje glavne osi kamere
"""

import matplotlib.pyplot as plt
import numpy as np
from _utils import draw3D_arrow


# Principal axis class
class PrincipalAxis:
    def __init__(self, camera_center, camera_dz, f):
        self.camera_center = camera_center  # origin of the camera
        self.camera_dz = camera_dz  # direction of the z axis of the camera
        self.f = f  # focal length
        self.p = camera_center + f * camera_dz  # principal point

    def draw3D(
            self,
            head_length=0.3,
            color="tab:red",
            s=20.0,
            ax=None,
            scale_factor=1.0,
            show_principal_point=True
    ):
        if ax is None:
            ax = plt.gca()

        draw3D_arrow(
            self.camera_center,
            2 * self.f * self.camera_dz,
            head_length=scale_factor*head_length,
            color=color,
            name="Z",
            ax=ax
        )

        if show_principal_point:
            ax.scatter(*self.p, color=color, s=s)
            ax.text(*self.p, 'p')

        return ax

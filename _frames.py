# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 02:08:13 2022

@author: igors

Opis modula: klasa za stvaranje pojedinih koordinatnih sustava
"""

import numpy as np
import matplotlib.pyplot as plt
from _utils import draw3D_arrow


class ReferenceFrame:
    def __init__(self, origin, dx, dy, dz, name):
        self.origin = origin
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.name = name

    def draw3D(self, scale_factor=1.0, show_name=True):
        ax = plt.gca()
        if show_name:
            ax.text(*self.origin + scale_factor * 0.5, self.name)
        ax = draw3D_arrow(self.origin, scale_factor*self.dx, scale_factor*0.3, ax, name='x')
        ax = draw3D_arrow(self.origin, scale_factor*self.dy, scale_factor*0.3, ax, name='y')
        ax = draw3D_arrow(self.origin, scale_factor*self.dz, scale_factor*0.3, ax, name='z')
        return ax

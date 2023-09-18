# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 02:32:24 2022

@author: igors

Opis modula: funkcija za crtanje vektora i funkcija za dobivanje jednadžbe ravnine iz tri točke
"""

import numpy as np
import matplotlib.pyplot as plt


# Function used to plot a vector
def draw3D_arrow(
        arrow_location,
        arrow_vector,
        head_length,
        ax=None,
        color=None,
        name=None,
):
    if ax is None:
        ax = plt.gca()

    ax.quiver(*arrow_location,
              *arrow_vector,
              color=color,
              arrow_length_ratio=head_length / np.linalg.norm(arrow_vector))

    if name is not None:
        ax.text(*(arrow_location + arrow_vector), name)

    return ax



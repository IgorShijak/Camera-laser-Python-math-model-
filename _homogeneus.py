# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 01:39:14 2022

@author: igors

Opis modula: pretvorba normalnih koordinata u homogene koordinate i iz homogenih koordinata u normalne
"""

import numpy as np


def to_homogeneus(X):
    if X.ndim > 1:
        raise ValueError("x has to be a vector.")
    return np.hstack([X, 1])


def to_inhomogeneus(X):
    if X.ndim > 1:
        raise ValueError("x has to be a vector.")
    return (X / X[-1])[:-1]

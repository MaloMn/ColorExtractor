# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 19:04:49 2019

@author: malom
"""

import numpy as np

def unique_pairs(step, m):
    """Produce pairs of indexes in range(n)"""
    for i in np.linspace(step, m, m//step):
        for j in np.linspace(step, m, m//step):
            yield i, j



for i, j in unique_pairs(2, 6):
    print(i, j)
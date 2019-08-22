# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 19:09:05 2019

@author: malom
"""

# Import datas
from PIL import Image
import numpy as np
from time import time

def RGBtoHEXA(l):
    
    x = l[0]
    y = l[1]
    z = l[2]
    
    # Color as hexadecimal
    r = hex(int(x)).split('x')[-1]
    g = hex(int(y)).split('x')[-1]
    b = hex(int(z)).split('x')[-1]
    
    if len(r) < 2:
        r = '0' + r
    if len(g) < 2:
        g = '0' + g
    if len(b) < 2:
        b = '0' + b
    
    return '#' + r + g + b

def show(array, labels):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    from numpy import amax
    
    colors = [(0.0,0.0,0.0,1.0)]
    colors.extend([plt.cm.Spectral(each) for each in np.linspace(0, 1, amax(labels)+1)])

    
    fig = plt.figure()
    fig.set_size_inches(10,7)
    
    for i in range(len(array)):
        plt.plot(array[i][0],array[i][1], c=colors[labels[i]+1], marker='o')
    

    
    name = '2DScatter.png'
    plt.savefig(name)
    plt.close()

# DATA
pixels = np.asarray(Image.open('resized6.jpg'))
        
pixels_list = []
     

for i in range(0, len(pixels), 1):
    for j in range(0, len(pixels[0]), 1):
        pixels_list.append(tuple(pixels[i,j].tolist()))




# HDBSCAN
from hdbscan import HDBSCAN
#from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import calinski_harabaz_score

#pixels_list = pixels_list[::1000]
#best = -1
#clbest = 0
#sabest = 0
#for cl in np.linspace(10,500,50):
#    for sa in np.linspace(10,500,50):
#        cl, sa = int(cl), int(sa)
#        hd = HDBSCAN(leaf_size=40, metric='euclidean', min_cluster_size=cl, min_samples=sa)
#        
#        start_time = time()
#        hd.fit(pixels_list)
#        end_time = time()
#        
#        try:
#            if calinski_harabaz_score(pixels_list, hd.labels_) > best:
#                best = calinski_harabaz_score(pixels_list, hd.labels_)
#                clbest, sabest = cl, sa
#                print(best)
#        except ValueError:
#            b = 1
            


pixels_list = pixels_list[::5]
print(len(pixels_list))

hd = HDBSCAN(leaf_size=40, metric='euclidean', min_cluster_size=10000, min_samples=int(len(pixels_list)/4500))
        
start_time = time()
hd.fit(pixels_list)
end_time = time()

print(end_time - start_time)
print('calinski = {}'.format(calinski_harabaz_score(pixels_list, hd.labels_)))


pixels_list = pixels_list[::100]

print('showing')
show(pixels_list, hd.labels_)








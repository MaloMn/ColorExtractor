# -*- coding: utf-8 -*-

from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

# Generating sample data
centers = [[0.5, -0.2], [0.5, -1], [1.1, -1.2]]
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.3,
                            random_state=0)
X = StandardScaler().fit_transform(X)

# X contains the points

import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg') #Useful to save the graph as an image later


########################## Points
fig = plt.figure(0)
fig.set_size_inches(10,7)

plt.plot(X[:,0],X[:,1], 'ro')

#for i in range(len(coor_pts)):
#    plt.plot(coor_pts[i, 0], coor_pts[i, 1], 'o', color = col[labels[i]+1], markersize=15)
#    #plt.text(coor_pts[i, 0], coor_pts[i, 1], odeurs[i], fontsize= 15, bbox=dict(facecolor=col[labels[i]+1], alpha=0.5))

name = 'result/points.png'
plt.savefig(name)
plt.close(0)

######################### Finding Epsilon

minpts = 75
average_dist = []
    
# We compute the minpts-NN graph
from math import sqrt
for i in range(len(X)):
    dist = []
    for j in range(len(X)):
        dist.append(sqrt((X[i, 0] - X[j, 0])**2 + (X[i, 1] - X[j, 1])**2))
    dist.sort()
    sum = 0.0
    for k in range(int(minpts)):
        sum += dist[k]
    average_dist.append(sum/minpts)
        
average_dist.sort()

###### We figure out the knee of the curve by finding two straight lines which
# can approximate the previous curve.

from numpy import linspace

# We change the abscisse of the collision point

min_g = 999999
(a3,a4) = (0,0)


for xm in linspace(2, len(X)-2, int(len(X)/300)): # For time reasons, 300 can be decreased !!!
    sum_g = 0
    xm = int(xm)
    # First straight line: y = a1*x + y0
    x0, x1 = 0, int(xm/2)
    y0, y1 = (average_dist[x0], average_dist[x1])
    
    # FIRST MMCO
    p = 3 # Precision of the MMCO
    
    mini = 99999
    a1 = 0
    for a in linspace(0,p*(y1-y0)/(x1-x0),50):
        som = 0
        for k in range(xm): # We don't compute it for k = xm
            som += (average_dist[k] - (a*k+y0))**2
        if som < mini:
            mini = som
            a1 = a
    
    sum_g += mini
    
    # Second one: y = a2*x + y3 - a2*x3
    x3 = len(X)-1
    x2 = int((x3-xm)/2 + xm)
    y2, y3 = (average_dist[x2], average_dist[x3])
    
    # SECOND MMCO
    p = 3 # Precision of the MMCO
    
    mini = 99999
    a2 = 0
    for a in linspace(0,p*(y3-y2)/(x3-x2),50):
        som = 0
        for k in range(xm, len(X)):
            som += (average_dist[k] - (a*k+y3-a*x3))**2
        if som < mini:
            mini = som
            a2 = a
            
    sum_g += mini
    
    if sum_g < min_g:
        min_g = sum_g
        (a3,a4) = (a1,a2)


(a1,a2) = (a3,a4)

# We have our equation, now we trace them on their intervals
# We look for the point of encounter of the two straight lines

xe = (y3-a2*x3 - y0)/(a1-a2)

epsilon = a1*xe + y0

xe = int(xe)

line1 = []
inter1 = []
for i in range(xe+2):
    line1.append(a1*i + y0)
    inter1.append(i)

line2 = []
inter2 = []
for i in range(xe, len(X)):
    line2.append(a2*i + y3-a2*x3)
    inter2.append(i)

fig = plt.figure(1)
fig.set_size_inches(10,7)

plt.plot(average_dist) + plt.plot(inter1, line1) + plt.plot(x1,y1, 'ro') + plt.plot(inter2, line2)

name = 'result/Knee.png'
plt.savefig(name)
plt.close(1)

######################### DBSCAN Result
fig = plt.figure(2)
fig.set_size_inches(10,7)

from sklearn.cluster import DBSCAN 

db = DBSCAN(eps=epsilon, min_samples=minpts, metric='euclidean').fit(X)
labels = db.labels_

from random import random

col = [(0,0,0), (1,0,0), (0,1,0), (0,0,1), (1,1,0), 
       (0,1,1), (1,0,1), (0.753,0.753,0.753), (0.5,0.5,0.5), (0.5,0,0), 
       (0.5,0.5,0), (0,0.5,0), (0.5,0,0.5), (0,0.5,0.5), (0,0,0.5)]

while len(col) < 55:
    col.append((random(), random(), random()))
    
for i in range(len(X)):
    plt.plot(X[i, 0], X[i, 1], 'o', color = col[labels[i]+1], markersize=5)
    
name = 'result/dbscan.png'
plt.savefig(name)
plt.close(2)


def EpsilonFinder(X, minpts):
    """Finds an appropriate epsilon following a given minpts using
    the "knee" technique. The knee is computed via multiples approximations
    by straight lines"""
    
    average_dist = []
    
    # We compute the minpts-NN graph
    from math import sqrt
    for i in range(len(X)):
        dist = []
        for j in range(len(X)):
            dist.append(sqrt((X[i, 0] - X[j, 0])**2 + (X[i, 1] - X[j, 1])**2))
        dist.sort()
        sum = 0.0
        for k in range(int(minpts)):
            sum += dist[k]
        average_dist.append(sum/minpts)
            
    average_dist.sort()
    
    ###### We figure out the knee of the curve by finding two straight lines which
    # can approximate the previous curve.
    
    from numpy import linspace
    
    # We change the abscisse of the collision point
    
    min_g = 999999
    (a3,a4) = (0,0)
    
    
    for xm in linspace(2, len(X)-2, int(len(X)/300)): # For time reasons, 300 can be decreased !!!
        sum_g = 0
        xm = int(xm)
        # First straight line: y = a1*x + y0
        x0, x1 = 0, int(xm/2)
        y0, y1 = (average_dist[x0], average_dist[x1])
        
        # FIRST MMCO
        p = 3 # Precision of the MMCO
        
        mini = 99999
        a1 = 0
        for a in linspace(0,p*(y1-y0)/(x1-x0),50):
            som = 0
            for k in range(xm): # We don't compute it for k = xm
                som += (average_dist[k] - (a*k+y0))**2
            if som < mini:
                mini = som
                a1 = a
        
        sum_g += mini
        
        # Second one: y = a2*x + y3 - a2*x3
        x3 = len(X)-1
        x2 = int((x3-xm)/2 + xm)
        y2, y3 = (average_dist[x2], average_dist[x3])
        
        # SECOND MMCO
        p = 3 # Precision of the MMCO
        
        mini = 99999
        a2 = 0
        for a in linspace(0,p*(y3-y2)/(x3-x2),50):
            som = 0
            for k in range(xm, len(X)):
                som += (average_dist[k] - (a*k+y3-a*x3))**2
            if som < mini:
                mini = som
                a2 = a
                
        sum_g += mini
        
        if sum_g < min_g:
            min_g = sum_g
            (a3,a4) = (a1,a2)
    
    
    (a1,a2) = (a3,a4)
    
    # We have our equation, now we trace them on their intervals
    # We look for the point of encounter of the two straight lines
    
    xe = (y3-a2*x3 - y0)/(a1-a2)
    
    epsilon = a1*xe + y0
    
    # PLOTTING THE KNEE FOUND
    # =============================================================================
    import matplotlib
    matplotlib.use('Agg') #Useful to save the graph as an image later
    xe = int(xe)
    
    line1 = []
    inter1 = []
    for i in range(xe+2):
        line1.append(a1*i + y0)
        inter1.append(i)
    
    line2 = []
    inter2 = []
    for i in range(xe, len(X)):
        line2.append(a2*i + y3-a2*x3)
        inter2.append(i)
    
    fig = plt.figure(1)
    fig.set_size_inches(10,7)
    
    plt.plot(average_dist) + plt.plot(inter1, line1) + plt.plot(inter2, line2)
    
    name = 'Knee.png'
    plt.savefig(name)
    plt.close(1)
    # =============================================================================
    
    return epsilon
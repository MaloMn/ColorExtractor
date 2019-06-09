# -*- coding: utf-8 -*-
from sklearn.cluster import DBSCAN

### DBSCAN Time-test
from random import random
from time import time

rec_points, rec_time = ([],[])

for i in range(713053, 713054, 25000):
    X = []
    for j in range(i):
        a = (int(random()*256), int(random()*256), int(random()*256))
        X.append(a)
    
    start = time()
    db = DBSCAN(eps=20, min_samples=500).fit(X)
    
    print('{} points, {} seconds spent.'.format(i, time() - start))
    
    rec_points.append(i)
    rec_time.append(time() - start)
    
import matplotlib.pyplot as plt
import numpy as np

plt.plot(rec_points, rec_time)
plt.show()

### Methode des moindres carrés ordinaires
# On recherche une fonction du type a*x²

# Données collectées
#rec_points = [0,50000, 75000, 100000, 125000, 150000, 175000, 200000, 225000, 250000,
#              275000, 300000, 325000, 350000, 375000, 400000, 425000, 450000, 475000,
#              500000, 525000, 550000, 575000, 600000, 625000, 650000, 675000, 700000,
#              725000, 750000, 775000, 800000, 825000, 850000, 875000, 900000, 925000,
#              950000, 975000]
#
#rec_time = [0,0.7647526264190674, 1.5564854145050049, 2.2602577209472656, 3.850755214691162,
#            5.0113794803619385, 6.3078625202178955, 7.970263481140137, 9.357180118560791,
#            12.06627082824707, 13.946923971176147, 15.00095510482788, 16.51467776298523,
#            18.318153142929077, 20.461386919021606, 22.861075162887573,
#            25.157883882522583, 27.550094604492188, 30.005300521850586, 35.24760580062866,
#            38.00173234939575, 40.63408708572388, 43.48294425010681, 46.59003162384033,
#            49.7859320640564, 52.84991645812988, 56.06894636154175, 59.13490343093872,
#            62.53978395462036, 66.08463788032532, 70.08534502983093, 73.3963086605072,
#            77.12208318710327, 80.86688828468323, 85.687429189682, 92.4910991191864,
#            102.3302857875824, 107.97424626350403, 114.60747194290161]

plt.plot(rec_points, rec_time)

amin = 0
x = np.linspace(0,0.0002,1001)
rec_sums = []
min = 999999

for a in x:
    sum = 0
    for i in range(len(rec_time)):
        sum += (rec_time[i] - a*rec_points[i]**2)**2
    rec_sums.append(sum)
    if sum < min:
        min = sum
        amin = a

model = []  
for i in range(len(rec_points)):
    model.append(amin*rec_points[i]**2)
    
plt.plot(rec_points, rec_time) + plt.plot(rec_points, model)
        
        

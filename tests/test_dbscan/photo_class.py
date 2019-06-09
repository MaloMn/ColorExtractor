# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN
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

def short(l, length):
    """ Deletes some random elements of a list to make it shorter according to
    a given length"""
    
    a = len(l)/length
    
    if a > 1:
        o = []
        o.append(l[0])
        b = a - int(a)
        while True:
            b += a
            if int(b) >= len(l):
                break
            else:
                o.append(l[int(b)])
        return o
    else:
        return l
            

def distSq(el2, el1):
    """Computes the euclidean distance between two given tuples of same dimension"""
    
    sum_ = 0
    for i in range(len(el1)):
        sum_ += (el1[i] - el2[i])**2
    return sum_

def EpsilonFinder(X, minpts):
    """Finds an appropriate epsilon following a given minpts using
    the "knee" technique. The knee is computed via multiples approximations
    by straight lines"""
    
    avg_dist = []
    
    from sklearn.neighbors import NearestNeighbors
    NN = NearestNeighbors(n_neighbors=minpts).fit(X)
    
    # Now we have the distances of the k-Nearest-Neighbors
    kNN = NN.kneighbors(n_neighbors=minpts)
    kNN = kNN[0]
    
    from numpy import average
    
    for i in range(len(X)):
        avg_dist.append(average(kNN[i]))
            
    avg_dist.sort()
    
    # On supprime toutes les valeurs inférieures ou égales à 0 et supérieures ou égales à 255*sqrt(3)
    avg_dist = list(filter(lambda x: x >= 0.01 and x <= 441.5, avg_dist))
    
    # Now we reduce our list to 300 elements.
    avg_dist = short(avg_dist, 300)
    
    ###### We figure out the knee of the curve by finding two straight lines which
    # can approximate the previous curve.
    #print('Starting to compute the knee! Almost there.')
    from numpy import linspace
    
    min_g = 999999
    (a3,a4) = (0,0)
    
    for xm in linspace(2, len(avg_dist)-2, len(avg_dist)-3): 
        sum_g = 0
        xm = int(xm)
        # First straight line: y = a1*x + y0
        x0, x1 = 0, int(xm/2)
        y0, y1 = (avg_dist[x0], avg_dist[x1])
        
        # FIRST MMCO
        p = 2 # Precision of the MMCO
        
        mini = 99999
        a1 = 0
        for a in linspace(0,p*(y1-y0)/(x1-x0),50):
            som = 0
            for k in range(xm): # We don't compute it for k = xm
                som += (avg_dist[k] - (a*k+y0))**2
            if som < mini:
                mini = som
                a1 = a
        
        sum_g += mini
        
        # Second one: y = a2*x + y3 - a2*x3
        x3 = len(avg_dist)-1
        x2 = int((x3-xm)/2 + xm)
        y2, y3 = (avg_dist[x2], avg_dist[x3])
        
        # SECOND MMCO
        p = 3 # Precision of the MMCO
        
        mini = 99999
        a2 = 0
        for a in linspace(0,p*(y3-y2)/(x3-x2),50):
            som = 0
            for k in range(xm, len(avg_dist)):
                som += (avg_dist[k] - (a*k+y3-a*x3))**2
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
#    import matplotlib
#    matplotlib.use('Agg') #Useful to save the graph as an image later
#    import matplotlib.pyplot as plt
#    xe = int(xe)
#    
#    line1 = []
#    inter1 = []
#    for i in range(xe+2):
#        line1.append(a1*i + y0)
#        inter1.append(i)
#    
#    line2 = []
#    inter2 = []
#    for i in range(xe, len(avg_dist)):
#        line2.append(a2*i + y3-a2*x3)
#        inter2.append(i)
#    
#    fig = plt.figure(1)
#    fig.set_size_inches(10,7)
#    
#    plt.plot(avg_dist) + plt.plot(inter1, line1) + plt.plot(inter2, line2)
#    
#    name = 'Knee.png'
#    plt.savefig(name)
#    plt.close(1)
    # =============================================================================
    
    return epsilon

class Photo:
    
    def __init__(self, path, reduce = True):    
        self.path = path
             
        self.pixels = np.asarray(Image.open(self.path))
        
        # We are "cutting" our data into 16 squares, so each side is divided in 4
        sq = 4
        self.pixels_list = []
        # We create 16 boxes
        for i in range(sq**2):
             self.pixels_list.append([])
             
        # We store each point in the corresponding box
        for i in range(0, len(self.pixels), 1):
            for j in range(0, len(self.pixels[0]), 1):
                a = int(len(self.pixels)/4)
                b = int(len(self.pixels[0])/4)
                
                x = int((i - i%a)/a)
                y = int((j - j%b)/b)
                x = sq - 1 if x > sq - 1 else x
                y = sq - 1 if y > sq - 1 else y
                
                self.pixels_list[x*sq+y].append(tuple(self.pixels[i,j].tolist()))

        print(len(self.pixels_list))        
        
        # We reduce the numper of pixels to a number <= 100 000
        # self.pixels_list = short(self.pixels_list, 100000)
        # print(self.pixels_list[0][1])
        
    def make_dbscan(self, minpts):  
        """Finds Epsilon, and applies DBSCAN to the pixels of the photo"""
        
        # We apply DBSCAN locally
        # Will contain the list of locals cores.
        self.cores_list = []
        for i in range(len(self.pixels_list)):
            epsilon = EpsilonFinder(self.pixels_list[i], minpts)
            epsilon = 0.001 if epsilon <= 0 else epsilon
            db = DBSCAN(eps = epsilon, min_samples = minpts, algorithm='ball_tree').fit(self.pixels_list[i]) 
            self.cores_list.extend(db.components_)

            print(i)
        
        print(len(self.cores_list))
        
        self.cores_list = short(self.cores_list, 100000)
        epsilon = EpsilonFinder(self.cores_list, minpts)        
        epsilon = 0.001 if epsilon <= 0 else epsilon
        db = DBSCAN(eps = epsilon, min_samples = minpts, algorithm='ball_tree').fit(self.cores_list)

        self.labels = db.labels_
    
    def show(self):

        self.points = [] # Will contain the coordinates of the average point
        self.points_avg = []
        
        from numpy import amax
        for i in range(amax(self.labels) + 1):
            self.points.append([])
        
        for i in range(len(self.cores_list)):
            if self.labels[i] >= 0 :
                self.points[self.labels[i]].append(self.cores_list[i])
        
        # We get number of points in the largest cluster to draw some circles according to that
        self.biggest = 0
        for i in range(len(self.points)):
            if len(self.points[i]) > self.biggest:
                self.biggest = len(self.points[i])
        
        # Now we average the points in each cluster
        for i in range(len(self.points)):
            N = float(len(self.points[i]))
            self.points_avg.append((sum(t[0] for t in self.points[i])/N,
                              sum(t[1] for t in self.points[i])/N,
                              sum(t[2] for t in self.points[i])/N))
            
        # Now we plot the averaged points
            
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        fig.set_size_inches(10,7)
        ax = fig.add_subplot(111, projection='3d')
        
        for i in range(len(self.points_avg)):
            color = RGBtoHEXA(self.points_avg[i])
            
            x = self.points_avg[i][0]
            y = self.points_avg[i][1]
            z = self.points_avg[i][2]
            
            # We plot the point
            ax.scatter(x, y, z, c=color, marker = 'o', s=1500*len(self.points[i])/self.biggest)
        
        name = '3DScatter.png'
        plt.savefig(name)
        plt.close()
    
    #def save(self, ):
        
#==============================================
#start = time() 

img = Photo('resized6.jpg')
img.make_dbscan(50)

#end = time() - start
#print(end)        

#img.show()
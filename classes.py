from functions import *
from PIL import Image
from sklearn.cluster import DBSCAN
import numpy as np
 
class Photo:
    
    def __init__(self, path, reduce = True):    
        self.path = path
             
        self.pixels = np.asarray(Image.open(self.path))
        
        # We list the pixels in an array of dimension 2
        self.pixels_list = []
        for i in range(0, len(self.pixels), 1):
            for j in range(0, len(self.pixels[0]), 1):
                self.pixels_list.append(tuple(self.pixels[i,j].tolist()))
                
        # We reduce the numper of pixels to a number <= 100 000
        self.pixels_list = short(self.pixels_list, 100000)
        
    def make_dbscan(self, minpts):  
        """Finds Epsilon, and applies DBSCAN to the pixels of the photo"""
        print('Searching for Epsilon...')
        epsilon = EpsilonFinder(self.pixels_list, minpts)
        if epsilon <= 0:
            epsilon = 0.001
            
        print('Epsilon found : ' + str(epsilon))
        db = DBSCAN(eps = epsilon, min_samples = minpts, algorithm='ball_tree').fit(self.pixels_list)
        self.labels = db.labels_
    
    def show(self):

        self.points = [] # Will contain the coordinates of the average point
        self.points_avg = []
        
        from numpy import amax
        for i in range(amax(self.labels) + 1):
            self.points.append([])
        
        for i in range(len(self.labels)):
            if self.labels[i] >= 0 :
                self.points[self.labels[i]].append(self.pixels_list[i])
        
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
            x = self.points_avg[i][0]
            y = self.points_avg[i][1]
            z = self.points_avg[i][2]
            
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
            color = '#' + r + g + b
            
            # We plot the point
            ax.scatter(x, y, z, c=color, marker = 'o', s=1500*len(self.points[i])/self.biggest)
        
        name = '3DScatter.png'
        plt.savefig(name)
        plt.close()
    
    def save(self, )
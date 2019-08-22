from functions import *
from PIL import Image
from sklearn.cluster import DBSCAN
import numpy as np
 
class Photo:
    
    def __init__(self, path, reduce = True):    
        """
            Opens up an image, and puts its pixels in self.pixels.
            It also lists them in self.pixels_list.
        """
        self.path = path
             
        self.pixels = np.asarray(Image.open(self.path))
        
        # We list the pixels in an array of dimension 2
        self.pixels_list = []
        for i in range(0, len(self.pixels), 1):
            for j in range(0, len(self.pixels[0]), 1):
                self.pixels_list.append(tuple(self.pixels[i,j].tolist()))
                
    def compute(self, nb_wished_colors, hue_rez, sat_rez, val_rez):
        """
            To get the main colors, we plot virtually the colors in a 3d space, 
            and we cut some smaller cubes in that space. The cubes containing 
            most points are kept.
        """
        self.nb_wished_colors = nb_wished_colors #= 16
        self.hue_rez = hue_rez #= 20   # 0 <= hue < 360
        self.sat_rez = sat_rez #= 0.075 # 0 <= saturation <= 1
        self.val_rez = val_rez #= 0.075 # 0 <= value <= 1
        
        repartition = np.zeros((int(360/hue_rez), int(1/sat_rez), int(1/val_rez)), dtype=int)
        
        for c in self.pixels_list:
            hue = c[0]
            # We remove the sat/val = 1 from the equation
            sat = c[1] if c[1] < 1 - self.sat_rez else 1 - self.sat_rez
            val = c[2] if c[2] < 1 - self.val_rez else 1 - self.val_rez
            
            repartition[int(hue/self.hue_rez), int(sat/self.sat_rez), int(val/self.val_rez)] += 1
        
        # Collecting the fourth most important colors
        self.colors = []
        
        def generator():
            for x in range(len(repartition)):
                for y in range(len(repartition[0])):
                    for z in range(len(repartition[0][0])):
                        yield x, y, z
        
        for i in range(self.nb_wished_colors):
            m = np.amax(repartition)
        
            # Looking for the coordinates of the maximum
            for x, y, z in generator():
                if repartition[x, y, z] == m:
                    self.colors.append([x*hue_rez + hue_rez/2, y*sat_rez + sat_rez/2, z*val_rez + val_rez/2])
                    repartition[x,y,z] = 0
                    break
                
        #self.colors now contains the most important colors.
    
#    def make_dbscan(self, minpts):  
#        """Finds Epsilon, and applies DBSCAN to the pixels of the photo"""
#        print('Searching for Epsilon...')
#        epsilon = EpsilonFinder(self.pixels_list, minpts)
#        if epsilon <= 0:
#            epsilon = 0.001
#            
#        print('Epsilon found : ' + str(epsilon))
#        db = DBSCAN(eps = epsilon, min_samples = minpts, algorithm='ball_tree').fit(self.pixels_list)
#        self.labels = db.labels_
#    
#    def show(self):
#
#        self.points = [] # Will contain the coordinates of the average point
#        self.points_avg = []
#        
#        from numpy import amax
#        for i in range(amax(self.labels) + 1):
#            self.points.append([])
#        
#        for i in range(len(self.labels)):
#            if self.labels[i] >= 0 :
#                self.points[self.labels[i]].append(self.pixels_list[i])
#        
#        # We get number of points in the largest cluster to draw some circles according to that
#        self.biggest = 0
#        for i in range(len(self.points)):
#            if len(self.points[i]) > self.biggest:
#                self.biggest = len(self.points[i])
#        
#        # Now we average the points in each cluster
#        
#        for i in range(len(self.points)):
#            N = float(len(self.points[i]))
#            self.points_avg.append((sum(t[0] for t in self.points[i])/N,
#                              sum(t[1] for t in self.points[i])/N,
#                              sum(t[2] for t in self.points[i])/N))
#            
#        # Now we plot the averaged points
#            
#        import matplotlib.pyplot as plt
#        from mpl_toolkits.mplot3d import Axes3D
#        fig = plt.figure()
#        fig.set_size_inches(10,7)
#        ax = fig.add_subplot(111, projection='3d')
#        
#        for i in range(len(self.points_avg)):
#            x = self.points_avg[i][0]
#            y = self.points_avg[i][1]
#            z = self.points_avg[i][2]
#            
#            # Color as hexadecimal
#            r = hex(int(x)).split('x')[-1]
#            g = hex(int(y)).split('x')[-1]
#            b = hex(int(z)).split('x')[-1]
#            
#            if len(r) < 2:
#                r = '0' + r
#            if len(g) < 2:
#                g = '0' + g
#            if len(b) < 2:
#                b = '0' + b
#            color = '#' + r + g + b
#            
#            # We plot the point
#            ax.scatter(x, y, z, c=color, marker = 'o', s=1500*len(self.points[i])/self.biggest)
#        
#        name = '3DScatter.png'
#        plt.savefig(name)
#        plt.close()
    
    def save(self, name):
        factor = int(len(self.colors) ** (1/2))
        size = 100
        width = size * factor
        
        grid = np.empty((width, width, 3), dtype=int)
        
        for x in range(width):
            for y in range(width):
                index = factor * (x // size) + (y // size) #x+factor*y
                
                hue = self.colors[index][0]
                sat = self.colors[index][1]
                val = self.colors[index][2]
                
                r, g, b = HSBtoRGB((hue, sat, val))
                
                color = [r, g, b]
                for z in range(len(color)):
                    grid[x, y, z] = color[z]
        
        grid = grid.reshape((width, width*3))
        
        output = []
        for i in range(len(grid)):
            output.append(tuple(grid[i]))
        
        from png import Writer
        with open('output.png', 'wb') as f:
            w = Writer(width, width, greyscale=False, alpha=False)
            w.write(f, output)
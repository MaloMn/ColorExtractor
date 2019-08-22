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
from functions import *
from PIL import Image
from sklearn.cluster import DBSCAN
import numpy as np

# =============================================================================
# class Blob:
#     # Works well when tested out
#     """Creates a sphere with a size and a number of points needeed"""
# 
#     def __init__(self, center):
#         """Needs a size (or range) and a starting center as a tuple (x, y, z)"""
#         self.center = center
#         self.points_nb = 1
# 
#     def add_point(self, pos):
#         """Adds a point and changes the center of the Blob"""
#         self.points_nb += 1
#         self.center = ((self.center[0] + pos[0])/2, (self.center[1] + pos[1])/2, (self.center[2] + pos[2])/2)
#     
#     def __str__(self):
#         return 'The Blob ({}, {}, {}) contains {} points.'.format(self.center[0], self.center[1], self.center[2], self.points_nb)
# 
# class Photo:
#     """This class represents a Photo, with its four dominant colors in RGB
#     and in HSV and its position amoungst the color reference"""
# 
#     def __init__(self, path, radius, step = 50):
#         """We construct the object by assigning it a new size"""
# 
#         self.step = step
#         self.path = path
#         self.radius = radius
#         
#         # We load the image pixels, and we shorten the image by the given stepping
#         self.pixels = np.asarray(Image.open('data/' + self.path))
#         self.pixels = self.pixels[::self.step, ::self.step]
#         
#         self.width = len(self.pixels[0])
#         self.height = len(self.pixels)
#         
#         self.blobs_list = []
#         self.color = (0,0,0)
#         self.colorHSB = (0,0,0)
#         
#         print("We suppose the image is {}x{} pixels.".format(self.width, self.height))
#                 
#     def __repr__(self):
#         """Showing the path of the Photo"""
#         string = "Name: " + self.path  + '; ' + str(len(self.blobs_list)) + ' colors found' +  '.'
#         return string
#     
#     def make_blob(self):
#         """Uses the blobs technique to extract the main colors"""
#         
#         self.blobs_list = []
#         
#         # We add one element to the Blob list to prevent futur errors
#         self.blobs_list.append(Blob(self.pixels[0,0]))
#         # We run through the pixels to create some blobs accordingly
#         for i in range(self.width):
#             for j in range(self.height):
#                 # TODO : We take the average of the points missed with the stepping
# 
#                 # For each pixel, we run though the Blob list
#                 # We don't look at the first pixel as we already added it                
#                 a = 1000000 # Bigger than any distance that will be computed
#                 index = 0 # Doesn't matter what first index we use
#                 for k in range(len(self.blobs_list)):
#                     # If the distance from the current point to the center
#                     # of the current Blob is lower than range, the blobs
#                     # size in increased. Otherwise, we create a new Blob.
#                     if dist(self.pixels[i,j], self.blobs_list[k].center) < a:
#                         a = dist(self.pixels[i,j], self.blobs_list[k].center)
#                         index = k
# 
#                 if a <= self.radius:
#                     self.blobs_list[index].add_point(self.pixels[i,j])
#                 else:
#                     self.blobs_list.append(Blob(self.pixels[i,j]))
#                 
#                 #TODO correction due to new size (width, height)
#                 progress(j+i*self.height, self.height*self.width, status = 'Scanning picture')
#                 #print('{}, {}'.format(i, self.width))
# 
#         # Now that we have all of our blobs created, we sort them decreasingly
#         self.blobs_list.sort(key= lambda Blob: Blob.points_nb, reverse = True)
# 
#         # Now we can pick the biggest Blob center as our main color
#         self.color = self.blobs_list[0].center
# 
#         # Quick conversion to HSV
#         self.colorHSB = RGBtoHSB(self.color)
#         
#     def make_dbscan(self):
#         """Uses the DBSCAN Algorithm to find the main color"""
#         db = DBSCAN()
#         
# 
#     def save(self, x, time = 0):
#         """Saves the picture with its name modified"""
#         # We change the name
#         b = ''
#         for j in self.path:
#             if j != '.':
#                 b += j
#             else:
#                 break
#         # We save the main picture resized
#         Image.fromarray(np.uint8(self.pixels)).save('result/' + str(x) + '_' + str(time) + b + '.bmp')
# 
#         # We save a small square indicating the colors found
#         g = Image.new( 'RGB', (400,400), "black") # create a new black image
#         pixels = g.load() # create the pixel map
# 
#         for i in range(g.size[0]):    # for every col:
#             for j in range(g.size[1]):    # For every row
#                 # We compute the location of the color
#                 h = int(i//(g.size[0]/4)+4*(j//(g.size[1]/4)))
#                 #We get the color at this position
#                 c = self.blobs_list[h].center
#                 c = (int(c[0]), int(c[1]), int(c[2]))
# 
#                 pixels[i,j] = (c[0], c[1], c[2]) # set the colour accordingly
#         g.save('result/' + str(x) + 'sq' + '_' + str(time) + '_' + b + '.bmp')
# =============================================================================
 
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
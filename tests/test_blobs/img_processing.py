from functions import dist, RGBtoHSB, progress 
from PIL import Image
from sklearn.cluster import DBSCAN
import numpy as np

class Blob:
    # Works well when tested out
    """Creates a sphere with a size and a number of points needeed"""

    def __init__(self, center):
        """Needs a size (or range) and a starting center as a tuple (x, y, z)"""
        self.center = center
        self.points_nb = 1

    def add_point(self, pos):
        """Adds a point and changes the center of the Blob"""
        self.points_nb += 1
        self.center = ((self.center[0] + pos[0])/2, (self.center[1] + pos[1])/2, (self.center[2] + pos[2])/2)
    
    def __str__(self):
        return 'The Blob ({}, {}, {}) contains {} points.'.format(self.center[0], self.center[1], self.center[2], self.points_nb)

class Photo:
    """This class represents a Photo, with its four dominant colors in RGB
    and in HSV and its position amoungst the color reference"""

    def __init__(self, path, radius, step = 50):
        """We construct the object by assigning it a new size"""

        self.step = step
        self.path = path
        self.radius = radius
        
        # We load the image pixels, and we shorten the image by the given stepping
        self.pixels = np.asarray(Image.open('data/' + self.path))
        self.pixels = self.pixels[::self.step, ::self.step]
        
        self.width = len(self.pixels[0])
        self.height = len(self.pixels)
        
        self.blobs_list = []
        self.color = (0,0,0)
        self.colorHSB = (0,0,0)
        
        print("We suppose the image is {}x{} pixels.".format(self.width, self.height))
                
    def __repr__(self):
        """Showing the path of the Photo"""
        string = "Name: " + self.path  + '; ' + str(len(self.blobs_list)) + ' colors found' +  '.'
        return string
    
    def make_blob(self):
        """Uses the blobs technique to extract the main colors"""
        
        self.blobs_list = []
        
        # We add one element to the Blob list to prevent futur errors
        self.blobs_list.append(Blob(self.pixels[0,0]))
        # We run through the pixels to create some blobs accordingly
        for i in range(self.width):
            for j in range(self.height):
                # TODO : We take the average of the points missed with the stepping

                # For each pixel, we run though the Blob list
                # We don't look at the first pixel as we already added it                
                a = 1000000 # Bigger than any distance that will be computed
                index = 0 # Doesn't matter what first index we use
                for k in range(len(self.blobs_list)):
                    # If the distance from the current point to the center
                    # of the current Blob is lower than range, the blobs
                    # size in increased. Otherwise, we create a new Blob.
                    if dist(self.pixels[i,j], self.blobs_list[k].center) < a:
                        a = dist(self.pixels[i,j], self.blobs_list[k].center)
                        index = k

                if a <= self.radius:
                    self.blobs_list[index].add_point(self.pixels[i,j])
                else:
                    self.blobs_list.append(Blob(self.pixels[i,j]))
                
                #TODO correction due to new size (width, height)
                progress(j+i*self.height, self.height*self.width, status = 'Scanning picture')
                #print('{}, {}'.format(i, self.width))

        # Now that we have all of our blobs created, we sort them decreasingly
        self.blobs_list.sort(key= lambda Blob: Blob.points_nb, reverse = True)

        # Now we can pick the biggest Blob center as our main color
        self.color = self.blobs_list[0].center

        # Quick conversion to HSV
        self.colorHSB = RGBtoHSB(self.color)
        
    def make_dbscan(self):
        """Uses the DBSCAN Algorithm to find the main color"""
        db = DBSCAN()
        

    def save(self, x, time = 0):
        """Saves the picture with its name modified"""
        # We change the name
        b = ''
        for j in self.path:
            if j != '.':
                b += j
            else:
                break
        # We save the main picture resized
        Image.fromarray(np.uint8(self.pixels)).save('result/' + str(x) + '_' + str(time) + b + '.bmp')

        # We save a small square indicating the colors found
        g = Image.new( 'RGB', (400,400), "black") # create a new black image
        pixels = g.load() # create the pixel map

        for i in range(g.size[0]):    # for every col:
            for j in range(g.size[1]):    # For every row
                # We compute the location of the color
                h = int(i//(g.size[0]/4)+4*(j//(g.size[1]/4)))
                #We get the color at this position
                c = self.blobs_list[h].center
                c = (int(c[0]), int(c[1]), int(c[2]))

                pixels[i,j] = (c[0], c[1], c[2]) # set the colour accordingly
        g.save('result/' + str(x) + 'sq' + '_' + str(time) + '_' + b + '.bmp')
 
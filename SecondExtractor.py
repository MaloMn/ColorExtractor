# Things that can be improved :
#  - Checking how much we can resize the picture down while keeping the
#    main color exact

import sys
import os
import PIL
from PIL import Image
import numpy
import math
import time

sat = 0
hue = 0
value = 0
radius = 20**2

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush() # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def RVBtoHSB(tuple):
    # Basic conversion formulas
    r = tuple[0]/255
    g = tuple[1]/255
    b = tuple[2]/255
    Cmax = max(r, g, b)
    Cmin = min(r, g, b)
    delta = Cmax - Cmin

    hue = 0
    sat = 0
    value = Cmax

    if Cmax == r and delta != 0:
        hue = 60*((g-b)/delta % 6)
    elif Cmax == g and delta != 0:
        hue = 60*((b-r)/delta + 2)
    elif Cmax == b and delta != 0:
        hue = 60*((r-g)/delta + 4)

    if Cmax != 0:
        sat = delta/Cmax

    return (hue, sat, value)

def dist(p, q):
    #This function works well
    """Returns the distance between two given tuples squared"""
    return (p[0] - q[0])**2 +  (p[1] - q[1])**2 + (p[2] - q[2])**2

class Blob:
    # Works well when tested out
    """Creates a sphere of a certain size that has a number of points"""

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

    def __init__(self, path, step):
        """We construct the object by assigning to its 4 dominant colors in
        RGB and HSV"""

        self.step = step
        self.path = path
        # self.colors_rgb = []
        self.blobs_list = []

        #print("[{}] {}".format(i, file_list[i]))
        # We load one image, and load its pixels
        self.img = Image.open('data/' + self.path)
        self.width = self.img.size[0]
        self.height = self.img.size[1]
        print("We suppose the image is {}x{} pixels.".format(int(self.width/self.step), int(self.height/self.step)))
        pixels = self.img.load()

        # We add one element to the Blob list to prevent futur errors
        self.blobs_list.append(Blob(pixels[0,0]))
        # We run through the pixels to create some blobs accordingly
        for i in range(0, self.width, self.step):
            for j in range(0, self.height, self.step):
                # For each pixel, we run though the Blob list
                # We don't look at the first pixel as we already added it
                
                a = 1000000 # Bigger than any distance that will be computed
                index = 0 # Doesn't matter what first index we use
                for k in range(len(self.blobs_list)):
                    # If the distance from the current point to the center
                    # of the current Blob is lower than range, the blobs
                    # size in increased. Otherwise, we create a new Blob.
                    if dist(pixels[i,j], self.blobs_list[k].center) < a:
                        a = dist(pixels[i,j], self.blobs_list[k].center)
                        index = k

                if a <= radius:
                    self.blobs_list[index].add_point(pixels[i,j])
                else:
                    self.blobs_list.append(Blob(pixels[i,j]))
                
                progress(j+i*self.height, self.height*self.width, status = 'Scanning picture')
                #print('{}, {}'.format(i, self.width))

        # Now that we have all of our blobs created, we sort them decreasingly
        self.blobs_list.sort(key= lambda Blob: Blob.points_nb, reverse = True)

        # Now we can pick the biggest Blob center as our main color
        self.color = self.blobs_list[0].center

        # Quick conversion to HSV
        self.colorHSB = RVBtoHSB(self.color)

    def __repr__(self):
        """Showing the path of the Photo"""
        string = "Name: " + self.path  + '; ' + str(len(self.blobs_list)) + ' colors found' +  '.'
        return string

    def save(self, x):
        """Saves the picture with its name modified"""
        # We change the name
        b = ''
        for j in self.path:
            if j != '.':
                b += j
            else:
                break
        # We save the main picture
        self.img = self.img.resize((int(self.width/self.step), int(self.height/self.step)), Image.ANTIALIAS)
        self.img.save('result/' + str(x) + b + '.bmp')

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
        g.save('result/' + str(x) + 'sq' + b + '.bmp')
    
def entry(message, answers):
    var = True
    while var:
        b = input(message)
        for i in range(len(answers)):
            if b == answers[i]:
                var = False
    return b

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array
#print(file_list)

###############################################################
######### Choosing between batch or single processing #########
###############################################################

choice = str(entry('Are you processing a single image or a batch of file ? (single/batch) : ', ['single', 'batch']))

if choice == 'single':
    for c in range(1, 61, 5):
        
        # We record the time spent on the action
        t1 = time.time()
        main = Photo(file_list[16], c)
        print(main)
        t2 = time.time()

        # We print the time spent on the processing
        print('Image processed in {}:{}.'.format(int((t2-t1) // 60), int((t2-t1) % 60)))

        main.save(c)

else:    
    # We store each picture once analysed in an array
    photos_list = []
    for a in file_list:
        photos_list.append(Photo(a, 150))
        print(photos_list[len(photos_list) - 1])

    # We sort the picture by hue, then by saturation
    # and finally by value if necessary
    photos_list.sort(key= lambda Photo: Photo.colorHSB[2])
    photos_list.sort(key= lambda Photo: Photo.colorHSB[1])
    photos_list.sort(key= lambda Photo: Photo.colorHSB[0])

    # We save pictures once resized so it doesn't take too much space on the disk
    # as it is saved in bitmap, and hence, uncompressed
    for i in range(len(photos_list)):
        print('Saving pictures: {} %'.format(int(i/len(file_list)*100)))
        photos_list[i].save(i)

os.system("pause")

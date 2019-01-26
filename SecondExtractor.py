# Things that can be improved :
#  - Checking how much we can resize the picture down while keeping the
#    main color exact


import os
import PIL
from PIL import Image
import numpy
import math

sat = 0
hue = 0
value = 0
range = 3.5

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
    """Returns the distance between two given tuples"""
    return math.sqrt((p[0] - q[0])**2 +  (p[1] - q[1])**2 + (p[2] - q[2])**2)

class blob:
    """Creates a sphere of a certain size that has a number of points"""

    def __init__(self, center):
        """Needs a size (or range) and a starting center as a tuple (x, y, z)"""
        self.center = center
        self.points_nb = 1

    def add_point(self, pos):
        """Adds a point if the distance to
        the average center is lower or equal than the range"""
        self.points_nb += 1
        self.center = ((center[0] + pos[0])/2, (center[1] + pos[1])/2, (center[2] + pos[2])/2)

class photo:
    """This class represents a photo, with its four dominant colors in RGB
    and in HSV and its position amoungst the color reference"""

    def __init__(self, path):
        """We construct the object by assigning to its 4 dominant colors in
        RGB and HSV"""

        self.path = path
        # self.colors_rgb = []
        self.blobs_list = []

        #print("[{}] {}".format(i, file_list[i]))
        # We load one image, and load its pixels
        img = Image.open('data/' + self.path)
        self.width, self.height = img.size
        img = img.resize((width/2,height/2), Image.ANTIALIAS)
        pixels = img.load()

        # We add one element to the blob list to prevent futur errors
        self.blobs_list.append(blob(pixels[0,0]))

        # We run through the pixels to create some blobs accordingly
        for i in range(pixels.length):
            for j in range(pixels[0].length):
                # For each pixel, we run though the blob list
                # We don't look at the first pixel as we already added it
                if not(i == 0 and j == 0):
                    for k in range(len(self.blobs_list)):
                        # If the distance from the current point to the center
                        # of the current blob is lower than range, the blobs
                        # size in increased. Otherwise, we create a new blob.
                        if (dist(pixels[i,j], blobs_list[k].center) <= range):
                            self.blobs_list[k].add_point(pixels[i,j])
                        else:
                            self.blobs_list.append(blob(pixels[i,j]))

        # Now that we have all of our blobs created, we sort them decreasingly
        blobs_list.sort(key= lambda blob: blob.points_nb, reverse = True)

        # Now we can pick the biggest blob center as our main color
        self.color = blobs_list[0].center

        # Quick conversion to HSV
        self.color = RVBtoHSB(self.color)

    def __str__(self):
        """Showing the path of the photo"""
        string = "Location: " + self.path + "; main color = " + self.color + " (in HSV)."
        return string

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

# We store each picture once analysed in an array
photos_list = []
for i in range(len(file_list)):
    photos_list.append(photo(file_list[i]))
    print('Analysing pictures: {} %'.format(int(i/len(file_list)*100)))

# We sort the picture by hue, then by saturation
# and finally by value if necessary
photos_list.sort(key= lambda photo: photo.color[2])
photos_list.sort(key= lambda photo: photo.color[1])
photos_list.sort(key= lambda photo: photo.color[0])

# We save pictures once resized so it doesn't take too much space on the disk
# as it is saved in bitmap, and hence, uncompressed
for i in range(len(photos_list)):
    print('Saving pictures: {} %'.format(int(i/len(file_list)*100)))
    new = Image.open('data/' + photos_list[i].path)
    new = new.resize((1000,700), Image.ANTIALIAS)
    # Quickly renaming files, removing the original extension (.jpg or .png)
    b = ''
    for j in photos_list[i].path:
        if j != '.':
            b += j
        else:
            break

    new.save('result/' + str(i) + b + '.bmp')

    # Create a small square image to indicate overall color found by algorithm
    a = photos_list[i].colors
    a = (a[0], a[1], a[2])

    im = Image.new('RGB', (100,100), color=a)
    im.save('result/' + str(i) + 'sq' + b + '.bmp')

os.system("pause")

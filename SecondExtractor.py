# New way of doing things

import os
import PIL
from PIL import Image
import numpy
import math

sat = 0
hue = 0
value = 0

def RVBtoHSB(r,g,b):
    # We now store it in HSV
    r = r/255
    g = g/255
    b = b/255
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
    # We add the same color in hsv to the hsv list

    return (hue, sat, value)

def dist(p, q):
    """Returns the distance between two given tuples"""
    return math.sqrt

class photo:
    """This class represents a photo, with its four dominant colors in RGB
    and in HSV and its position amoungst the color reference"""

    def __init__(self, path):
        """We construct the object by assigning to its 4 dominant colors in
        RGB and HSV"""

        self.path = path
        self.colors_rgb = []
        self.blobs_list = []

        #print("[{}] {}".format(i, file_list[i]))
        # We load one image, and load its pixels
        img = Image.open('data/' + self.path)
        pixels = img.load()

        # We store each color in the colors_rgb array
        for i in range(pixels.length):
            for j in range(pixels[0].length):
                self.colors_rgb.append(pixels[i,j])

        # We run through the array created to create some blobs accordingly
        for i in colors_rgb:



    def __str__(self):
        """Showing the path of the photo"""
        return self.path

class Blob:
    """Creates a sphere of a certain size that has a number of points"""
    def __init__(self, size, center)
    self.size = size
    self.center = center

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

photos_list = []

for i in range(len(file_list)):
    photos_list.append(photo(file_list[i]))
    print('Analysing pictures: {} %'.format(int(i/len(file_list)*100)))

photos_list.sort(key= lambda photo: photo.colors_hsv[2])
photos_list.sort(key= lambda photo: photo.colors_hsv[1])
photos_list.sort(key= lambda photo: photo.colors_hsv[0])

for i in range(len(photos_list)):
    print('Saving pictures: {} %'.format(int(i/len(file_list)*100)))
    new = Image.open('data/' + photos_list[i].path)
    new = new.resize((1000,700), Image.ANTIALIAS)

    b = ''
    for j in photos_list[i].path:
        if j != '.':
            b += j
        else:
            break

    new.save('result/' + str(i) + b + '.bmp')

    # Create a small image to indicate overall color found by algorithm
    a = photos_list[i].colors_rgb
    a = (a[0], a[1], a[2])

    im = Image.new('RGB', (100,100), color=a)
    im.save('result/' + str(i) + 'sq' + b + '.bmp')

os.system("pause")

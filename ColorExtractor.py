import os
import PIL
from PIL import Image

sat = 0
hue = 0
value = 0

class photo:
    """This class represents a photo, with its four dominant colors in RGB
    and in HSV and its position amoungst the color reference"""

    # We define the reference color range
    colors_ref = []
    for i in range(360):
        colors_ref.append(i)

    def __init__(self, path):
        """We construct the object by assigning to it 4 dominant colors in
        RGB and HSV"""

        print(path)

        self.path = path
        self.colors_rgb = []
        self.colors_hsv = []
        #print("[{}] {}".format(i, file_list[i]))
        # We load one image, resize it to a 2x2,
        img = Image.open('data/' + self.path)
        img = img.resize((1,1), Image.ANTIALIAS)
        pixels = img.load()
        # We store the color of each pixel in pixcolor and then in color_list
        # We store one color in RGB first just in case
        # so it has the r, g and b components
        for k in range(len(pixels[0,0])):
            self.colors_rgb.append(pixels[0,0][k])
        # We now store it in HSV
        r = pixels[0,0][0]/255
        g = pixels[0,0][1]/255
        b = pixels[0,0][2]/255
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
        self.colors_hsv.append(hue)
        self.colors_hsv.append(sat)
        self.colors_hsv.append(value)
        # Now we have two lists with 3*4 elements each.

    def __str__(self):
        """Showing the path a photo"""
        return self.path

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

photos_list = []

for i in range(len(file_list)):
    photos_list.append(photo(file_list[i]))

photos_list.sort(key= lambda photo: photo.colors_hsv[0])

for i in range(len(photos_list)):
    print(photos_list[i])
    new = Image.open('data/' + photos_list[i].path)
    new.save('result/' + str(i) + '.bmp')


# We create a list of the colors converted from rgb to hsv without the value

os.system("pause")

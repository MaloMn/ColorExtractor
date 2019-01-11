import os
import PIL
from PIL import Image

sat = 0
hue = 0
value = 0

# We define the range of degrees for HSV, ignoring 360
colors_ref = []
for i in range(360):
    colors_ref.append(i)

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

# We define the variables we will used to store our colors
pixcolor = []
color_list = []
color_list_hsv = []

for i in range(len(file_list)):
    pixcolor = []
    print("[{}] {}".format(i, file_list[i]))
    # We load one image, resize it to a 2x2,
    img = Image.open('data/' + file_list[i])
    img = img.resize((2,2), Image.ANTIALIAS)
    pixels = img.load()
    # We store the color of each pixel in pixcolor and then in color_list
    for i in range(2):
        for j in range(2):
            # We store it in RGB first just in case
            pixcolor.append(pixels[i,j])
            # We now store it in HSV
            r = pixels[i,j][0]/255
            g = pixels[i,j][1]/255
            b = pixels[i,j][2]/255
            Cmax = max(r, g, b)
            Cmin = min(r, g, b)
            delta = Cmax - Cmin

            hue = 0
            sat = 0
            value = Cmax

            if Cmax == r:
                hue = 60*((g-b)/delta % 6)
            elif Cmax == g:
                hue = 60*((b-r)/delta + 2)
            elif Cmax == b:
                hue = 60*((r-g)/delta + 4)

            if Cmax != 0:
                sat = delta/Cmax

            color_list_hsv.append(hue)
            color_list_hsv.append(sat)
            color_list_hsv.append(value)

    color_list.append(pixcolor)
print(color_list)
print('hsv =', color_list_hsv)

    # We create a list of the colors converted from rgb to hsv without the value

os.system("pause")

class photo:
    """This class represents a photo, with its four dominant colors in RGB
    and in HSV and its position amoungst the color reference"""

    colors_ref = []
    for i in range(360):
        colors_ref.append(i
        

    def __init__(self, red, blue, green):
        self.red = red
        self.blue = blue
        self.green = green

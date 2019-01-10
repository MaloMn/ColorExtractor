import os
import PIL
from PIL import Image

sat = 0
hue = 0

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

# We define the variables we will used to store our colors
pixcolor = []
color_list = []

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
            #print(pixels[i,j])
            pixcolor.append(pixels[i,j])

    color_list.append(pixcolor)
    print(color_list)

    # We create a list of the colors converted from rgb to hsv without the value




os.system("pause")


def hue(R, G, B):
    r = R/255
    g = G/255
    b = B/255
    Cmax = max(r, g, b)
    Cmin = min(r, g, b)
    delta = Cmax - Cmin

    H = 0
    S = 0

    if Cmax == r:
        H = 60*((g-b)/delta % 6)
    elif Cmax == g:
        H = 60*((b-r)/delta + 2)
    elif Cmax == b:
        H = 60*((r-g)/delta + 4)

    if Cmax != 0:
        S = delta/Cmax

    sat = S
    hue = H

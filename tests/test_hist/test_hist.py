def RGBtoHSB(tuple):
    # Wikipedia conversion formulas
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

def HSBtoRGB(tuple):
    H = tuple[0]
   
    C = tuple[2]*tuple[1]
    X = C * (1 - abs(H/60 % 2 - 1))
    m = tuple[2] - C
    
    if H >= 0 and H < 60:
        r, g, b = (C, X, 0)
    elif H >= 60 and H < 120:
        r, g, b = (X, C, 0)
    elif H >= 120 and H < 180:
        r, g, b = (0, C, X)
    elif H >= 180 and H < 240:
        r, g, b = (0, X, C)
    elif H >= 240 and H < 300:
        r, g, b = (X, 0, C)
    else:
        r, g, b = (C, 0, X)
        
    return ((r+m)*255, (g+m)*255, (b+m)*255)


def unique_pairs(step, m):
    """Produce pairs of indexes in range(n)"""
    for i in np.linspace(step, m, m//step):
        for j in np.linspace(step, m, m//step):
            yield i, j


import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from png import Writer
from math import ceil

#####################################################################
pixels = np.asarray(Image.open('index.jpg'))
        
# We list the pixels in an array of dimension 2
pixels_list = []
for i in range(0, len(pixels), 1):
    for j in range(0, len(pixels[0]), 1):
        pixels_list.append(RGBtoHSB(tuple(pixels[i,j].tolist())))
#####################################################################


nb_wished_colors = 16
hue_rez = 20   # 0 <= hue < 360
sat_rez = 0.075 # 0 <= saturation <= 1
val_rez = 0.075 # 0 <= value <= 1

repartition = np.zeros((int(360/hue_rez), int(1/sat_rez), int(1/val_rez)), dtype=int)

for c in pixels_list:
    hue = c[0]
    # We remove the sat/val = 1 from the equation
    sat = c[1] if c[1] < 1 - sat_rez else 1 - sat_rez
    val = c[2] if c[2] < 1 - val_rez else 1 - val_rez
    
    repartition[int(hue/hue_rez), int(sat/sat_rez), int(val/val_rez)] += 1

# Collecting the fourth most important colors
colors = []   

def generator():
    for x in range(len(repartition)):
        for y in range(len(repartition[0])):
            for z in range(len(repartition[0][0])):
                yield x, y, z

for i in range(nb_wished_colors):
    m = np.amax(repartition)

    # Looking for the coordinates of the maximum
    for x, y, z in generator():
        if repartition[x, y, z] == m:
            colors.append([x*hue_rez + hue_rez/2, y*sat_rez + sat_rez/2, z*val_rez + val_rez/2])
            repartition[x,y,z] = 0
            break

grid = np.empty((m, m, 3), dtype=int)

factor = int(len(colors) ** (1/2))
size = 100
width = size * factor

grid = np.empty((width, width, 3), dtype=int)

for x in range(width):
    for y in range(width):
        index = factor * (x // size) + (y // size) #x+factor*y
        
        hue = colors[index][0]
        sat = colors[index][1]
        val = colors[index][2]
        
        r, g, b = HSBtoRGB((hue, sat, val))
        
        color = [r, g, b]
        for z in range(len(color)):
            grid[x, y, z] = color[z]

grid = grid.reshape((width, width*3))

output = []
for i in range(len(grid)):
    output.append(tuple(grid[i]))

with open('output.png', 'wb') as f:
    w = Writer(width, width, greyscale=False, alpha=False)
    w.write(f, output)
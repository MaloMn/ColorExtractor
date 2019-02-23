import random

from PIL import Image

I = []

for i in range(16):
    a = random.randrange(255)
    b = random.randrange(255)
    c = random.randrange(255)
    I.append((a, b, c))

print(I) 

# PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
img = Image.new( 'RGB', (200,200), "black") # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every col:
    for j in range(img.size[1]):    # For every row
        pixels[i,j] = (I[(i//50)+4*(j//50)][0], I[(i//50)+4*(j//50)][1], I[(i//50)+4*(j//50)][2]) # set the colour accordingly

img.show()
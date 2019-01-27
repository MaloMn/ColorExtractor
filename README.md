# ColorExtractor

This tool extracts the dominant color of images, and then classifies them
according to that color.

## Simple Extractor

This program was created first, and works really simply : it just takes one image,
resizes it to a 1x1 image, and the main color is the one of the one pixel composing
the image. As you might expect it, it doesn't really work as it does an average of
all the colors, and that is not really what we want.

## Second Extractor

This program is the current version of the code. It works rather differently than
the original program : instead of doing an average of all the colors, it does a
local average, on the pixels that are already kind of the same color.

Algorithm explained :
 * The image is resized, just for speed purpose.
 * Each pixel becomes a point with its red, green and blue components as its coordinates
 * Blobs of a certain range (defined by the .pde files in tests folder) are created
 around the points, and we average the one that has most points to get the average
 color.
 * One we have every image dominant color, we classify them following the hue, then
 the saturation, and finally the value in needed

## Improvements in mind

Maybe using the median instead of doing an average is more accurate.
I also need to rethink the way image are classified, hue isn't that pretty.

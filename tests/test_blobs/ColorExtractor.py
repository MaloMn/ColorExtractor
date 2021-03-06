# Things that can be improved :
#  - Checking how much we can resize the picture down while keeping the
#    main color exact

import os
import time

from functions import entry
from img_processing import Photo

sat = 0
hue = 0
value = 0
radius = 40**2

# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array
print(file_list)

###############################################################
######### Choosing between batch or single processing #########
###############################################################

choice = str(entry('Are you processing a single image or a batch of file ? (single/batch) : ', ['single', 'batch']))

if choice == 'single':
    for c in range(50, 52, 1):
        
        # We record the time spent on the action
        t1 = time.time()
        main = Photo(file_list[23], radius, c)
        main.make_blob()
        print(main)
        t2 = time.time()

        # We print the time spent on the processing
        print('Image processed in {}:{}.'.format(int((t2-t1) // 60), int((t2-t1) % 60)))

        main.save(c, int(t2-t1))

else:    
    # We store each picture once analysed in an array
    photos_list = []
    for a in file_list:
        photos_list.append(Photo(a, 150))
        photos_list[len(photos_list) - 1].make_blobs()
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
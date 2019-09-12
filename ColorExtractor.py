import os, time, pickle
from scipy.spatial import distance
from c_photo import Photo


def min_greater_than_0(array):
    """Returns the index of the smallest element greater than 0."""

    # Checking array type:
    if array != list(array):
        raise TypeError("min_greater_than_0 requires a list.")

    # We define m as the max of the list as a starting point
    m = max(array)
    index_m = array.index(m)

    for i, el in enumerate(array):
        if (el < m) and (el > 0):
            m = el
            index_m = i

    if m != 0:
        return index_m
    else:
        return None


# First, we get the list of the pictures
dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = dir_path + "\data"
file_list = os.listdir(data_path) # file_list is an array

for a in range(len(file_list)):
    file_list[a] = "data/" + file_list[a]

print("There are {} files.".format(len(file_list)))

saving = 'saved/photos_list'

if not os.path.exists(saving):
    # We store each picture once analysed in photos_list
    photos_list = []
    for index, a in enumerate(file_list):
        t1 = time.time()
        photo = Photo(a)
        photo.compute(9, 30, 0.17, 0.1)
        t2 = time.time()

        photos_list.append(photo)

        minutes = int((t2 - t1) // 60)
        seconds = int((t2 - t1) % 60)
        percent = int(index/len(file_list)*100)

        print('Image processed in {0}:{1}. We\'re at {2} percent.'.format(minutes, seconds, percent))

    with open(saving, 'wb') as file:
        # dump information to that file
        pickle.dump(photos_list, file)
else:
    with open(saving, 'rb') as file:
        # dump information to that file
        photos_list = pickle.load(file)

saving = 'saved/dist_matrix'

if not os.path.exists(saving):
    dist_matrix = []
    for i, p in enumerate(photos_list):
        line = []

        # Computing the distance between one picture and the others
        for j, o in enumerate(photos_list):
            final_dist = 0.0
            i = len(o.colors)
            frac = 1/i

            for pc, oc in zip(p.colors, o.colors):
                final_dist += distance.euclidean(pc, oc) * frac * i
                i -= 1
            line.append(final_dist)

        dist_matrix.append(line)

    with open(saving, 'wb') as file:
        # dump information to that file
        pickle.dump(dist_matrix, file)
else:
    with open(saving, 'rb') as file:
        # dump information to that file
        dist_matrix = pickle.load(file)

# Sorting the pictures using dist-matrix
index = 0
sorted_pictures = []

while 'index returned is real':

    sorted_pictures.append(index)
    # We add some 0 to make sure we don't fall back on that picture
    for i in range(len(dist_matrix)):
        dist_matrix[i][index] = 0

    # We look for the minimum greater than 0 to have a new index
    index = min_greater_than_0(dist_matrix[index])

    if index is None:
        break


for i, el in enumerate(sorted_pictures):
    print('Saving pictures: {} %'.format(int(i/len(file_list)*100)))
    name = photos_list[el].path
    name = name.split('/')[1]

    photos_list[i].save("result/" + str(el) + "_" + str(name) + ".png")


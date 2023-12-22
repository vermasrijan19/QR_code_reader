import math

import cv2
import numpy as np


def calculate_ascii(array, down=False):
    up_mask = [128, 64, 32, 16, 8, 4, 2, 1]
    down_mask = [2, 1, 8, 4, 32, 16, 128, 64]
    up_horizontal_mask = [128, 64, 2, 1, 32, 16, 8, 4]
    down_horizontal_mask = [32, 16, 8, 4, 128, 64, 2, 1]
    if array.shape == (4, 2):
        if down:
            array_mask = down_mask
        else:
            array_mask = up_mask
    else:
        if down:
            array_mask = down_horizontal_mask
        else:
            array_mask = up_horizontal_mask

    array = array.flatten()[::-1]
    s = 0
    for i in range(len(array)):
        s = s + array[i] * array_mask[i]
    return s

image = cv2.imread("cropped_image.jpg", cv2.IMREAD_GRAYSCALE)
for i in range(21):
    for j in range(21):
        if image[i][j] > 50:
            image[i][j] = 255
        else:
            image[i][j] = 0

        if image[i][j] == 255:
            image[i][j] = 1

        image[i][j] = 1 - image[i][j]

# Define the mask based on the version
mask = []
version = 1
if version == 1:
    mask = image.copy()[8, 2:5]

for i in range(21):
    for j in range(21):
        if np.array_equal(mask, [0, 0, 1]):
            if (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0:
                # Flip the bit using XOR with 1
                image[i][j] = 1 - image[i][j]

# Store bottom right corner 4 cells and reverse it
mode_indicator = ((image[19:21, 19:21]).flatten())[::-1]
print("The mode indicator is:", mode_indicator)
if np.array_equal(mode_indicator, [0, 1, 0, 0]):
    print("The encoding mode is byte")

# Now get the 8 values above these 4 values, store them in a list, and reverse the list
length = (image[15:19, 19:21])
# First letter:
v1 = (image[11:15, 19:21])
v2 = (image[9:11, 17:21])

v3 = (image[11:15, 17:19])

v4 = (image[15:19, 17:19])

v5 = (image[19:21, 15:19])

v6 = (image[15:19, 15:17])

v7 = (image[11:15, 15:17])

v8 = (image[9:11, 13:17])

v9 = (image[11:15, 13:15])

# Continue this pattern for the remaining values
v10 = (image[15:19, 13:15])

v11 = (image[19:21, 11:15])

v12 = (image[15:19, 11:13])

v13 = (image[11:15, 11:13])

print("The Decoded QR code is:",
      chr(calculate_ascii(v1)) + chr(calculate_ascii(v2)) + chr(calculate_ascii(v3, True)) + chr(
          calculate_ascii(v4, True)) + chr(calculate_ascii(v5, True)) + chr(calculate_ascii(v6)) + chr(
          calculate_ascii(v7)) + chr(calculate_ascii(v8)) + chr(calculate_ascii(v9, True)) + chr(
          calculate_ascii(v10, True)) + chr(calculate_ascii(v11, True)) + chr(calculate_ascii(v12)) + chr(
          calculate_ascii(v13)))

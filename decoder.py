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


image = cv2.imread("Images/qrcode/Detected.jpg", cv2.IMREAD_GRAYSCALE)
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
matrix_size = 0
if version == 1:
    mask = image.copy()[8, 2:5]
    matrix_size = 21
    forbidden_row = 9
else:
    forbidden_row = 0

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
matrix_size = 21
length = (image[matrix_size - 6:matrix_size - 2, matrix_size - 2:matrix_size])
print(calculate_ascii(length))
a = matrix_size - 6
b = matrix_size - 2
c = matrix_size - 2
d = matrix_size
word = ""
# for loop 0 to 13
down = False
enable_down = False
letter = 1
while True:
    if 10 <= c < 13:
        forbidden_row = 7
    else:
        forbidden_row = 9
    print("letter: ", letter)
    letter = letter + 1
    if a - 4 >= forbidden_row and down is False and b < matrix_size:  # up
        print("case 1")
        b = a
        a = a - 4
    elif a > forbidden_row and down is False and b < matrix_size:  # up_left
        print("case 2")
        b = a
        a = a - 2
        c = c - 2
        enable_down = True
    elif down and a + 4 < matrix_size and a == forbidden_row:  # down
        print("case 3")
        a = a + 2
        b = b + 4
        d = d - 2
    elif down and b + 4 < matrix_size:  # down
        print("case 4")
        a = a + 4
        b = b + 4
    elif down and b + 2 == matrix_size:  # down_left
        print("case 5")
        a = a + 4
        b = b + 2
        c = c - 2
        d - 2
        enable_down = False
    elif b - 2 < matrix_size:  # up_after_down
        a = a - 4
        b = b - 2
        d = d - 2
        print("case 6")
    v = (image[a:b, c:d])

    print(a, b, c, d)
    word = word + chr(calculate_ascii(v, down))
    print(len(word))
    down = enable_down
    if len(word) >= (calculate_ascii(length)) :
        print("The Decoded QR code is:", word)
        break

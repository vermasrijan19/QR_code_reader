import sys
import cv2
import numpy as np
image = cv2.imread("cropped_image.jpg",cv2.IMREAD_GRAYSCALE)
image = np.where(image>128,255,0).astype('uint8')

for row in range(image.shape[0]):
    for row in range(image.shape[0]):
        print(f"Row {row}:")
        for col in range(image.shape[1]):
            pixel_value = image[row, col]
            print(f"{pixel_value} ", end='')
        print()  # Move to the next line after printing a row


import os

import cv2
import numpy as np


def display(img):
    # img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    cv2.imshow("edges", img)
    cv2.waitKey(0)


def histogram_equalize(img):
    b, g, r = cv2.split(img)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    return cv2.merge((blue, green, red))


def crop(image, firstPass=False):
    global squares
    img = image.copy()
    image = histogram_equalize(image)
    edges = cv2.Canny(image, 0, 125)
    # display(edges)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    squares = []
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # Tolerance for aspect ratio to consider as a square
            aspect_ratio_tolerance = 0.1

            if 1 - aspect_ratio_tolerance <= aspect_ratio <= 1 + aspect_ratio_tolerance:
                squares.append(approx)
    print(len(squares))
    squares = sorted(squares, key=cv2.contourArea, reverse=True)
    cv2.drawContours(image, squares, -1, (0, 255, 0), 3)
    # display(image)

    squares = squares[:1]
    # print(cv2.minAreaRect(squares[0]))

    # Draw the selected squares
    if len(squares) == 1:
        x1, y1, w1, h1 = cv2.boundingRect(squares[0])
        # Crop the image
        if firstPass:
            cropped_image = img
        # cropped_image = image[y_start - 10:y_end + 10, x_start - 10:x_end + 10]
        else:
            cropped_image = img[y1:y1 + h1, x1:x1 + w1]

    return cropped_image


image_name = "Images/excel.png"

folder_name = image_name.split(".")[0]
image = cv2.imread(image_name)
# image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
og_img = image.copy()
# cv2.imshow("Cropped image", image)

image = cv2.medianBlur(image, 3)

image = crop(image, False)
# display(image)
for row in range(image.shape[0]):
    for col in range(image.shape[1]):
        if image[row][col][0] > image[row][col][1] and image[row][col][0] > image[row][col][2]:
            image[row][col] = [255, 0,0]
        elif image[row][col][1] > image[row][col][0] and image[row][col][1] > image[row][col][2]:
            image[row][col] = [0, 255,0]
        elif image[row][col][2] > image[row][col][0] and image[row][col][2] > image[row][col][1]:
            image[row][col] = [0, 0,255]

# display(image)
image = cv2.resize(image, (3, 3), interpolation=None)
for row in range(image.shape[0]):
    for col in range(image.shape[1]):
        print(image[row][col])
        if image[row][col][0] > image[row][col][1] and image[row][col][0] > image[row][col][2]:
            image[row][col] = [255, 0,0]
        elif image[row][col][1] > image[row][col][0] and image[row][col][1] > image[row][col][2]:
            image[row][col] = [0, 255,0]
        elif image[row][col][2] > image[row][col][0] and image[row][col][2] > image[row][col][1]:
            image[row][col] = [0, 0,255]

path = os.path.join(folder_name, 'Detected.png')
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
# cv2.imshow("og image", og_img)
cv2.imwrite(path, image)
# display(image)

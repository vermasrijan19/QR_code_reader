import os

import cv2
import numpy as np


def crop(image, firstPass=False):
    global squares
    edges = cv2.Canny(image, 50, 150)
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
    # print(squares)
    squares = sorted(squares, key=cv2.contourArea, reverse=True)
    squares = squares[:3]
    print(cv2.minAreaRect(squares[0]))

    # Draw the selected squares
    if len(squares) >= 3:
        x1, y1, w1, h1 = cv2.boundingRect(squares[0])
        x2, y2, w2, h2 = cv2.boundingRect(squares[1])
        x3, y3, w3, h3 = cv2.boundingRect(squares[2])

        # Determine the y-axis range for cropping
        y_start = min(y1, y2, y3)
        y_end = max(y1 + h1, y2 + h2, y3 + h3)

        x_start = min(x1, x2, x3)
        x_end = max(x1 + w1, x2 + w2, x3 + w3)

        # Crop the image
        if (firstPass):
            cropped_image = image
        # cropped_image = image[y_start - 10:y_end + 10, x_start - 10:x_end + 10]
        else:
            cropped_image = image[y_start:y_end, x_start:x_end]

    return cropped_image


def align(img):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = 255 - img
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Compute rotated bounding box
    coords = np.column_stack(np.where(thresh > 0))
    # print("angle",cv2.minAreaRect(squares[1])[-1])
    angle = cv2.minAreaRect(coords)[-1]
    angle = -cv2.minAreaRect(squares[1])[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    print("Skew angle: ", angle)

    # Rotate image to deskew
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # cv2.imshow("Cropped image", rotated)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return rotated


image_name = "Images/old images/tilted.jpg"
folder_name = image_name.split(".")[0]
image = cv2.imread(image_name)
image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
# image = np.where(image>50,255,0).astype('uint8')
# image= cv2.GaussianBlur(image, (5, 5), 0)

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sharpening_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

# Apply the sharpening kernel using filter2D
image = cv2.filter2D(gray_img, -1, sharpening_kernel)
image = cv2.medianBlur(image, 3)
# image =align(image)
cropped_image = crop(image, True)
cropped_image = align(cropped_image)
cropped_image = crop(cropped_image)
# cropped_image=cv2.resize(cropped_image,(100,100))
print(squares)
ret, cropped_image = cv2.threshold(cropped_image, 120, 255, cv2.THRESH_BINARY)

cropped_image = cv2.erode(cropped_image, (3, 3), iterations=1)
cropped_image = cv2.dilate(cropped_image, (3, 3), iterations=1)
cropped_image = cv2.resize(cropped_image, (21, 21))

#check if folder exists
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
path=os.path.join(folder_name, 'Detected.jpg')
cv2.imwrite(path, cropped_image)

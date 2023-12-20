import cv2
import numpy as np

image = cv2.imread("QR.jpg")
image = cv2.resize(image,(0,0),fx=0.25,fy=0.25)
ret,image=cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
# image = np.where(image>50,255,0).astype('uint8')
# image= cv2.GaussianBlur(image, (5, 5), 0)

gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sharpening_kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])

# Apply the sharpening kernel using filter2D
image = cv2.filter2D(gray_img, -1, sharpening_kernel)

# image=cv2.erode(image,(3,3),iterations=6)
# image=cv2.dilate(image,(3,3),iterations=2)

edges = cv2.Canny(image, 50, 150)

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
squares = []
for contour in contours:
    epsilon = 0.04 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    print(approx)

    if len(approx) == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h

        # Tolerance for aspect ratio to consider as a square
        aspect_ratio_tolerance = 0.1

        if 1 - aspect_ratio_tolerance <= aspect_ratio <= 1 + aspect_ratio_tolerance:
            squares.append(approx)

# Draw the selected squares
image= cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
cv2.drawContours(image, squares, -1, (0, 255, 0), 2)
cv2.imshow("Cropped image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

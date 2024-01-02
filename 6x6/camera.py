import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)


def display(img):
    # img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    cv2.imshow("edges", img)
    # cv2.waitKey(0)

def apply_contrast_stretching(image, min_intensity, max_intensity):
    # Split the image into its color channels
    b, g, r = cv2.split(image)

    # Apply contrast stretching to each channel
    b_stretched = np.clip((b - b.min()) / (b.max() - b.min()) * (max_intensity - min_intensity) + min_intensity, 0, 255).astype(np.uint8)
    g_stretched = np.clip((g - g.min()) / (g.max() - g.min()) * (max_intensity - min_intensity) + min_intensity, 0, 255).astype(np.uint8)
    r_stretched = np.clip((r - r.min()) / (r.max() - r.min()) * (max_intensity - min_intensity) + min_intensity, 0, 255).astype(np.uint8)

    # Merge the stretched channels back into an image
    stretched_image = cv2.merge([b_stretched, g_stretched, r_stretched])

    return stretched_image
def histogram_equalize(img):
    b, g, r = cv2.split(img)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    return cv2.merge((blue, green, red))


def crop(image, firstPass=False):
    global squares, cropped_image
    img = image.copy()
    ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    # image = np.where(image>50,255,0).astype('uint8')
    # image= cv2.GaussianBlur(image, (5, 5), 0)

    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sharpening_kernel = np.array([[-2, -2, -2], [-2, 18, -2], [-2, -2, -2]])

    # Apply the sharpening kernel using filter2D
    image = cv2.filter2D(gray_img, -1, sharpening_kernel)
    image = cv2.medianBlur(image, 3)
    image=cv2.morphologyEx(image, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8),iterations=2)
    edges = cv2.Canny(image, 0, 100)
    display(edges)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow('og_frame', cv2.drawContours(image, contours, -1, (0, 255, 0), 3))
    squares = []
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            # Tolerance for aspect ratio to consider as a square
            aspect_ratio_tolerance = 0.5

            if 1 - aspect_ratio_tolerance <= aspect_ratio <= 1 + aspect_ratio_tolerance:
                squares.append(approx)
    squares = sorted(squares, key=cv2.contourArea, reverse=True)
    cv2.imshow('squares', cv2.drawContours(image, squares, -1, (0, 255, 0), 3))

    # cv2.drawContours(image, squares, -1, (0, 255, 0), 3)
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


while (True):

    # Capture the video frame
    # by frame
    ret, image = vid.read()
    image = cv2.medianBlur(image, 3)
    # cv2.imshow('og_frame', image)

    image = crop(image)
    cv2.imshow('frame', image)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

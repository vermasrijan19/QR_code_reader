import cv2

# 0 R=1 G=2 B=3
image = cv2.imread("../Images/excel/Detected.png", cv2.IMREAD_COLOR)
key = [4, 0, 1, 2, 5, 8, 7, 3, 6]
value = []
for row in range(image.shape[0]):
    for col in range(image.shape[1]):
        if image[row][col][0] > image[row][col][1] and image[row][col][0] > image[row][col][2]:
            value.append(1)
        elif image[row][col][1] > image[row][col][0] and image[row][col][1] > image[row][col][2]:
            value.append(2)
        elif image[row][col][2] > image[row][col][0] and image[row][col][2] > image[row][col][1]:
            value.append(3)
        elif image[row][col] == [0, 0, 0]:
            value.append(0)
og_value = value.copy()
for i in range(len(key)):
    value[i] = og_value[key[i]]
print(value)

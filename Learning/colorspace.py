import cv2
image_path = './data/bird image.jpeg'
image = cv2.imread(image_path)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
new_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('image', image)
cv2.imshow('new_img', new_img)
cv2.imshow('img_gray', img_gray)
cv2.imshow('img_hsv', img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
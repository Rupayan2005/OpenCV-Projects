import cv2
image_path = './data/bear.jpeg'

image = cv2.imread(image_path)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,threshold = cv2.threshold(img_gray, 60,255,cv2.THRESH_BINARY)
# Clearing Noise
threshold = cv2.blur(threshold,(10,10))
ret,threshold = cv2.threshold(threshold, 60,255,cv2.THRESH_BINARY)
cv2.imshow('image', image)
cv2.imshow('threshold', threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
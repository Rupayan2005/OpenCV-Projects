import cv2
image_path = './data/handwritting.png'

image = cv2.imread(image_path)
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,30)
cv2.imshow('image', image)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
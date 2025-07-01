import cv2
image_path = './data/freelancer image.jpg'
#Read Image
image = cv2.imread(image_path)
k_size = 7
img_blur = cv2.blur(image, (k_size, k_size))
img_gaussianblur = cv2.GaussianBlur(image, (k_size, k_size), 3)
cv2.imshow('image', image)
cv2.imshow('blurred_image', img_blur)
cv2.imshow('gaussian_blurred_image', img_gaussianblur)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
image_path = './data/cool boy image.jpg'
#Read Image
image = cv2.imread(image_path)
print(image.shape)
#Resize image
resized_image = cv2.resize(image, (280, 400))
cv2.imshow('image', image)
cv2.imshow('resized_image', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np
image_path = './data/player_messi.webp'

image = cv2.imread(image_path)
img_edge = cv2.Canny(image,100,300)
img_edge_d = cv2.dilate(img_edge,np.ones((3,3),dtype = np.int8))
img_edge_e = cv2.erode(img_edge_d,np.ones((3,3),dtype = np.int8))
cv2.imshow('image', image)
cv2.imshow('edge', img_edge)
cv2.imshow('edge_d', img_edge_d)
cv2.imshow('edge_e', img_edge_e)
cv2.waitKey(0)
cv2.destroyAllWindows()
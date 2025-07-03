import cv2
import numpy as np
image_path = './data/bird sky.jpg'
image = cv2.imread(image_path)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(image_gray,127,255,cv2.THRESH_BINARY_INV)
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
    #print(area)
    #cv2.drawContours(image,cnt,-1,(0,255,0),1) #Draw contours
    x1,y1,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(image,(x1,y1),(x1+w,y1+h),(0,255,0),2) #Bounding with rectangle
cv2.imshow('img', image)
cv2.imshow('thresh', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
image_path = './data/whiteboard.jpg'
image = cv2.imread(image_path)
print(image.shape)

#Line
cv2.line(image,(100,150),(200,250),(0,255,0),5)
#Rectangle
cv2.rectangle(image,(50,100),(200,300),(0,0,255),5) #for a complete filled rectangle select the thickness to -1
#Circle
cv2.circle(image,(200,200),100,(255,0,0),5)
#Text
cv2.putText(image,'Hello',(500,450),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
cv2.imshow('image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
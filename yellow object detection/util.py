import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])
    hsvColor = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    lower = hsvColor[0][0][0] - 10,100,100
    upper = hsvColor[0][0][0] + 10,255,255

    lower = np.array(lower, dtype = np.uint8)
    upper = np.array(upper, dtype = np.uint8)
    return lower, upper
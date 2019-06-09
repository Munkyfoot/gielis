import os
import sys
import random
import time
import math
import numpy as np
import cv2 as cv

RESOLUTION = 720
CENTER = (RESOLUTION // 2, RESOLUTION // 2)

img = np.zeros((RESOLUTION,RESOLUTION,3), 'uint8')

for phi in range(360):
    x = CENTER[0] + int(math.cos(phi) * RESOLUTION * 0.25)
    y = CENTER[1] + int(math.sin(phi) * RESOLUTION * 0.25)

    cv.circle(img, (x,y), 1, (255,255,255), 1, cv.LINE_AA)

while True:
    cv.imshow('Gielis', img)
    key = cv.waitKey(1)

    if key == ord('q'):
        break

cv.destroyAllWindows()

import os
import sys
import random
import time
import math
import numpy as np
import cv2 as cv

RESOLUTION = 720
CENTER = (RESOLUTION // 2, RESOLUTION // 2)

START_TIME = time.time()
LAST_TIME = time.time()
WAIT_TIME = 3

a = 1
b = 1
n1 = 1
n2 = 1
n3 = 1
m = 0

while True:
    img = np.zeros((RESOLUTION, RESOLUTION, 3), 'uint8')

    cur_time = time.time() - START_TIME

    time_passed = time.time() - LAST_TIME

    if time_passed >= WAIT_TIME:
        a = random.randint(1, 16)
        b = random.randint(1, 16)
        n1 = random.randint(1, 16)
        n2 = random.randint(1, 16)
        n3 = random.randint(1, 16)
        m = random.randint(1, 16)
        LAST_TIME = time.time()

    readout = "a: {}, b: {}, n1: {}, n2: {}, n3: {}, m: {}".format(
        a, b, n1, n2, n3, m)
    readout_time = "Next generation in {:.1f}...".format(
        WAIT_TIME - time_passed)
    first_point = None
    recent_point = None

    for deg in range(360):
        phi = math.radians(deg)
        scale = RESOLUTION * 0.25

        gielis = abs((1/a) * math.cos(m / 4 * phi)) * n2 + \
            abs((1/b) * math.sin(m / 4 * phi)) * n3
        gielis = math.pow(gielis, 1/n1)

        r = 1/gielis * scale

        x = CENTER[0] + int(math.cos(phi) * r)
        y = CENTER[1] + int(math.sin(phi) * r)

        color_sin = (math.sin(cur_time + phi * math.pi) + 1) * 0.5
        color_cos = (math.cos(cur_time + phi * math.pi) + 1) * 0.5
        color = (int(255 * color_sin), 255 -
                 int(255 * color_sin), int(255 * color_cos))

        if recent_point != None:
            cv.line(img, recent_point, (x, y), color, 1, cv.LINE_AA)

        if deg == 359:
            cv.line(img, (x, y), first_point, color, 1, cv.LINE_AA)

        if deg == 0:
            first_point = (x, y)

        recent_point = (x, y)

    cv.putText(img, readout, (32, 32), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, readout_time, (32, 48), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)

    cv.imshow('Gielis', img)
    key = cv.waitKey(1)

    if key == ord('q'):
        break

cv.destroyAllWindows()

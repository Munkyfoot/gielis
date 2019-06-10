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
        a = 1
        b = 1
        n = random.randrange(0, 3)
        n1 = random.uniform(0.1, 3)
        if n == 0:
            n2 = n1
            n3 = n1
        elif n == 1:
            n2 = random.uniform(0.1, 3)
            n3 = n2
        elif n == 2:
            n2 = random.uniform(0.1, 3)
            n3 = random.uniform(0.1, 3)

        m = random.randint(1, 8)
        LAST_TIME = time.time()

    readout = "a: {:.2f}, b: {:.2f} n1: {:.2f} n2: {:.2f} n3: {:.2f} m: {}".format(
        a, b, n1, n2, n3, m)
    readout_time = "Next generation in {:.1f}...".format(
        WAIT_TIME - time_passed)

    point_data = []
    scale = RESOLUTION * 0.25

    for deg in range(360):
        phi = math.radians(deg)

        gielis = abs((1/a) * math.cos(m / 4 * phi)) * n2 + \
            abs((1/b) * math.sin(m / 4 * phi)) * n3
        gielis = math.pow(gielis, 1/n1)

        r = 1/gielis * scale

        x = math.cos(phi) * r
        y = math.sin(phi) * r

        color_sin = (math.sin(cur_time + phi * math.pi) + 1) * 0.5
        color_cos = (math.cos(cur_time + phi * math.pi) + 1) * 0.5
        color = (int(255 * color_sin), 255 -
                 int(255 * color_sin), int(255 * color_cos))

        point_data.append([(x, y), color])

    max_coord = 0
    for point, color in point_data:
        max_coord = max(max_coord, max(abs(point[0]), abs(point[1])))

    for i in range(len(point_data)):
        point_data[i][0] = (CENTER[0] + int(point_data[i][0][0] / max_coord *
                                            scale), CENTER[1] + int(point_data[i][0][1] / max_coord * scale))

    for i in range(len(point_data)):
        if i < len(point_data) - 1:
            cv.line(img, point_data[i][0], point_data[i + 1]
                    [0], point_data[i][1], 2, cv.LINE_AA)
        else:
            cv.line(img, point_data[i][0], point_data[0]
                    [0], point_data[0][1], 2, cv.LINE_AA)

    cv.putText(img, readout, (32, 32), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(img, readout_time, (32, 48), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)

    cv.imshow('Gielis', img)
    key = cv.waitKey(1)

    if key == ord('q'):
        break

cv.destroyAllWindows()

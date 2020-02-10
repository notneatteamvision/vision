import cv2
import numpy as np
import math

import consts

def houghCircles_fix(frame, min_radius, max_radius, limit, **kwargs):
    step = kwargs.get('step', 5)
    circles = []
    size = max_radius
    


def find_circles(frame):
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, consts.CELL_COLOR_RANGE_LOWER, consts.CELL_COLOR_RANGE_UPPER)
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    edges = cv2.Canny(morph, 10, 200, 3)
    bedges = cv2.GaussianBlur(edges, (7, 7), 0)

    circles = cv2.HoughCircles(bedges, cv2.HOUGH_GRADIENT, 2, 100, minRadius=10, maxRadius=200)

    if (isinstance(circles, np.ndarray) and len(circles)) or circles != None:
        return list(map(list, np.uint16(np.around(circles))[0])), mask
    return [], mask

def max_circle(circles):
    return max(circles, key=lambda circle: circle[2])

def draw_circle(frame, circle, biggest=False):
    cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 0, 255) if biggest else (0, 255, 0), 2) # outer
    cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3) # inner

def draw_circles(frame, circles):
    if len(circles) == 0: return
    biggest = max_circle(circles)
    for circle in circles:
        if circle == biggest:
            continue
        draw_circle(frame, circle)
    draw_circle(frame, biggest, True)


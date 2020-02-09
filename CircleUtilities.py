import cv2
import numpy as np

import consts

def findCircles(frame):
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, consts.CELL_COLOR_RANGE_LOWER, consts.CELL_COLOR_RANGE_UPPER)
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    edges = cv2.Canny(morph, 10, 200, 3)
    bedges = cv2.GaussianBlur(edges, (7, 7), 0)

    circles = cv2.HoughCircles(bedges, cv2.HOUGH_GRADIENT, 2, 100, maxRadius=200)
    if (isinstance(circles, np.ndarray) and len(circles)) or circles != None:
        return (np.uint16(np.around(circles))[0], mask)
    return ([], mask)

def drawCircles(frame, circles):
    for circle in circles:
        # draw the outer circle
        cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)
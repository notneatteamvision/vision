import cv2
import numpy as np
import math

import consts

houghCircles_notempty = lambda c: ((isinstance(c, np.ndarray) and len(c)) or c != None)
houghCircles_format = lambda c: list(map(list, np.uint16(np.around(c))[0])) if houghCircles_notempty(c) else []


def houghCircles_fix(edges, **kwargs):
    # get kwargs
    min_radius: int = kwargs.get('min_radius', 100)
    max_radius: int = kwargs.get('max_radius', 200)
    limit: int = kwargs.get('limit', 1)
    step: int = kwargs.get('step', 5)
    hough_settings: tuple = kwargs.get('hough_settings', (cv2.HOUGH_GRADIENT, 2, 100))

    circles = []
    for moving_max in range(max_radius, min_radius - 1, -step):
        moving_min = max([moving_max - step + 1, min_radius])
        moving_circles = houghCircles_format(
            cv2.HoughCircles(edges, *hough_settings, minRadius=moving_min, maxRadius=moving_max))

        # print(f"{moving_max}:{moving_min} -> {len(moving_circles)} found")

        # add the circles found to the circles array
        if len(moving_circles) == 0:
            continue
        elif len(moving_circles) == 1:
            circles.append(moving_circles[0])
        else:
            circles.extend(sorted(moving_circles, key=lambda c: c[2], reverse=True))

        # return if reached circle limit
        if len(circles) >= limit:
            return circles[0:limit]
    return circles


def find_circles(frame):
    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, consts.CELL_COLOR_RANGE_LOWER, consts.CELL_COLOR_RANGE_UPPER)
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    edges = cv2.Canny(morph, 10, 200, 3)
    bedges = cv2.GaussianBlur(edges, (7, 7), 0)

    circles = houghCircles_fix(bedges, min_radius=30, max_radius=200, step=30)

    return circles, mask


def max_circle(circles):
    return max(circles, key=lambda circle: circle[2])


def draw_circle(frame, circle, biggest=False):
    cv2.circle(frame, (circle[0], circle[1]), circle[2], (0, 0, 255) if biggest else (0, 255, 0), 2)  # outer
    cv2.circle(frame, (circle[0], circle[1]), 2, (0, 0, 255), 3)  # inner


def draw_circles(frame, circles):
    if len(circles) == 0: return
    biggest = max_circle(circles)
    for circle in circles:
        if circle == biggest:
            continue
        draw_circle(frame, circle)
    draw_circle(frame, biggest, True)

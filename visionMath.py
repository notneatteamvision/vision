#imports not from the code

import math
import numpy as np

#imports not from the code

import consts


clamp = lambda x: 1 if x > 1 else -1 if x < -1 else x

pi = math.pi

angleAbs = lambda x: (x + pi) % (pi * 2)


def getHotizontalAngle(X: int) -> float:
    return math.radians((1 - 2 * X / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV_HORIZONTAL / 2)

#returns distance and angle from 1 circle with 1 camera
#used on guido
def locateCell(circle) -> tuple:
    """
    Calculates relative position btwn cell and robot from position and size in video
    """
    X, Y, radius = circle
    # print(circle[2])
    # calculate distance from camera to object
    l = (consts.LIFECAM_FOCAL_LENGTH * consts.CELL_RADIUS) / radius
    # calculate planar distance from robot to object
    try:
        if l ** 2 > consts.CAMERA_HEIGHT ** 2:
            d = math.sqrt(l ** 2 - consts.CAMERA_HEIGHT ** 2)
        else:
            d = 0.01  # ball is too close too camera
    except Exception as e:
        print(((X, Y, radius), l))
        raise e
    # calculate angle between cell and robot
    angle = getHotizontalAngle(X)
    return (d, angle)

#returns distance and angle from circles with 2 cameras
#not used on guido
def triangulatePoint(Xl: int, Xr: int) -> tuple:
    if Xl <= Xr:
        return False, None
    try:
        l = consts.CAMERA_DISTANCE
        Bl, Br = getHotizontalAngle(Xl), getHotizontalAngle(Xr)
        Dl = l * math.cos(Br) / math.sin(Bl - Br)
        x = math.sqrt((l / 2) ** 2 + Dl ** 2 - l * Dl * math.cos(pi / 2 - Bl))
        a = angleAbs(math.asin(clamp(math.cos(Bl) * Dl / x)) - pi / 2)
        return True, (x, a)
    except Exception as e:
        print((Xl, Xr))
        raise e  # TODO REMOVE THIS AAAAAAAA

import consts
import math
import numpy as np

pi = math.pi

angleAbs = lambda x: (x + pi) % (pi*2) - pi

def getHotizontalAngle(X: int) -> float:
    return (1 - 2 * X / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV / 2

def triangulatePoint(Bl: float, Br: float) -> tuple:
    l = consts.CAMERA_DISTANCE
    # Bl, Br = getHotizontalAngle(Xl), getHotizontalAngle(Xr)
    Dl = l * math.cos(Br) / math.sin(Bl - Br)
    x = math.sqrt((l/2)**2 + Dl**2 - l*Dl*math.cos(pi/2-Bl))
    a = angleAbs(math.asin(math.sin(pi/2-Bl)*Dl/x)-pi/2)
    return x, a

def locateCell(circle: np.array) -> tuple:
    """
    Calculates relative position btwn cell and robot from position and size in video
    """
    X, Y, radius = circle
    # calculate distance from camera to object
    l = (consts.LIFECAM_FOCAL_LENGTH * consts.CELL_RADIUS) / radius

    # calculate planar distance from robot to object
    try:
        d = math.sqrt(l ** 2 - consts.CAMERA_HEIGHT ** 2)
    except Exception as e:
        print(((X, Y, radius), l))
        raise e

    # calculate angle between cell and robot
    angle = getHotizontalAngle(X)

    return (d, angle)
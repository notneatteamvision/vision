import consts
import math
import numpy as np


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
    angle = (1 - 2 * X / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV / 2

    return (d, angle)
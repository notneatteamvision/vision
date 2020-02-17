# imports not from the code

import math

from pi import consts

# imports not from the code

pi = math.pi


def clamp(x):
    return 1 if x > 1 else -1 if x < -1 else x


def angle_abs(x):
    return (x + pi) % (pi * 2)


# finds angle cell to robot with 1 camera
def get_horizontal_angle(x: int) -> float:
    return math.radians((1 - 2 * x / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV_HORIZONTAL / 2)


# returns distance and angle from 1 circle with 1 camera
# used on guido
def locate_cell(circle) -> tuple:
    """
    Calculates relative position btwn cell and robot from position and size in video
    """
    X, Y, radius = circle  # center point + radius
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
    angle = get_horizontal_angle(X)
    return d, angle

# returns distance and angle from circles with 2 cameras
# not used on guido
# full calculation is on the vision paper with all the details/on drive in "general"
# def triangulate_point(xl, xr):
#     if xl <= xr:
#         return False, None
#     try:
#         l = consts.CAMERA_DISTANCE
#         bl, br = get_horizontal_angle(xl), get_horizontal_angle(xr)
#         dl = l * math.cos(br) / math.sin(bl - br)
#         x = math.sqrt((l / 2) ** 2 + dl ** 2 - l * dl * math.cos(pi / 2 - bl))
#         a = angle_abs(math.asin(clamp(math.cos(bl) * dl / x)) - pi / 2)
#         return True, (x, a)
#     except Exception as e:
#         print((xl, xr))
#         raise e  # TODO REMOVE THIS AAAAAAAA

import numpy as np

VIDEO_WIDTH = 640
#VIDEO_WIDTH = 1280 increases the quality but lowers the speed
VIDEO_HEIGHT = 480
#VIDEO_HEIGHT = 720

LIFECAM_FOCAL_LENGTH = 678.5
LIFECAM_FOV_HORIZONTAL = 60
LIFECAM_FOV_VERTICAL = 34.3

CAMERA_HEIGHT = 0.33  # 0.6 # (unit: m) TODO: change the value according to the robot sketch
CAMERA_DISTANCE = 0.37

CELL_RADIUS = 0.089
CELL_COLOR_RANGE_LOWER = np.array([19, 70, 20])
CELL_COLOR_RANGE_UPPER = np.array([40, 255, 255])
CELL_COLOR_RANGE = (CELL_COLOR_RANGE_LOWER, CELL_COLOR_RANGE_UPPER)

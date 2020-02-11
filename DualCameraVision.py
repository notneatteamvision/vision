import cv2
import math

import visionMath
from Camera import Camera
import CircleUtilities as Cutils

def do_vision(frame_left, frame_right):
    circles_left, mask_left = Cutils.find_circles(frame_left)
    circles_right, mask_right = Cutils.find_circles(frame_right)
    Cutils.find_circles(frame_right)
    if len(circles_left) == len(circles_right) == 1:
        suc, point = visionMath.triangulatePoint(circles_left[0][0], circles_right[0][0])
        if suc:
            text = f"{point[0] * 100:.1f} cm  {math.degrees(point[1]):.1f} deg"
            cv2.putText(frame_left, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    elif len(circles_right)>len(circles_left):
        d, a = visionMath.locateCell(circles_right)
        text = f"{d[0] * 100:.1f} cm  {math.degrees(a):.1f} deg"
        cv2.putText(frame_right, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        d, a = visionMath.locateCell(circles_left)
        text = f"{d[0] * 100:.1f} cm  {math.degrees(a):.1f} deg"
        cv2.putText(frame_left, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    Cutils.draw_circles(frame_left, circles_left)
    Cutils.draw_circles(frame_right, circles_right)

    cv2.imshow('LOFT', frame_left)
    cv2.imshow('ROGHT', frame_right)
    cv2.imshow('LOFT MASK', mask_left)
    cv2.imshow('ROGHT MASK', mask_right)


PORT_LEFT = 0
PORT_RIGHT = 1

cam_left = Camera(PORT_LEFT, exposure=-6)
cam_right = Camera(PORT_RIGHT, exposure=-6)

while True:
    frame_left, frame_right = cam_left.read(), cam_right.read()
    do_vision(frame_left, frame_right)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
cam_left.die()
cam_right.die()
import cv2
import math

import visionMath
from Camera import Camera
import CircleUtilities as Cutils

PORT_LEFT = 1
PORT_RIGHT = 0

camLeft = Camera(PORT_LEFT, exposure=-6)
camRight = Camera(PORT_RIGHT, exposure=-6)

while True:
    frameLeft, frameRight = camLeft.read(), camRight.read()
    circlesLeft, maskLeft = Cutils.findCircles(frameLeft)
    circlesRight, maskRight = Cutils.findCircles(frameRight)
    Cutils.findCircles(frameRight)
    if len(circlesLeft) == len(circlesRight) == 1:
        point = visionMath.triangulatePoint(circlesLeft[0][0], circlesRight[0][0])
        text = f"{point[0] * 100:.1f} cm  {math.degrees(point[1]):.1f} deg"
        cv2.putText(frameLeft, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    Cutils.drawCircles(frameLeft, circlesLeft)
    Cutils.drawCircles(frameRight, circlesRight)

    cv2.imshow('LOFT', frameLeft)
    cv2.imshow('ROGHT', frameRight)
    cv2.imshow('LOFT MASK', maskLeft)
    cv2.imshow('ROGHT MASK', maskRight)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
camLeft.die()
camRight.die()
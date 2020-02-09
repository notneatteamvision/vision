import cv2

import visionMath
from Camera import Camera
import CircleUtilities as Cutils

PORT_LEFT = 1
PORT_RIGHT = 2

camLeft = Camera(PORT_LEFT, exposure=-6)
camRight = Camera(PORT_RIGHT, exposure=-6)

while True:
    frameLeft, frameRight = camLeft.read(), camRight.read()
    circlesLeft, circlesRight = Cutils.findCircles(frameLeft), Cutils.findCircles(frameRight)
    if len(circlesLeft) == len(circlesRight) == 1:
        point = visionMath.triangulatePoint(circlesLeft[0][0], circlesRight[0][0])
        text = f"{point[0] * 100:.1f} cm  {point[1]:.1f} deg"
        cv2.putText(display, text, (circle[0], circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    Cutils.drawCircles(frameLeft, circlesLeft)
    Cutils.drawCircles(frameRight, circlesRight)

    cv2.imshow('LOFT', frameLeft)
    cv2.imshow('ROGHT', frameRight)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
camLeft.die()
camRight.die()
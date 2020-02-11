import cv2
import numpy as np
import visionMath
import consts
import math
from Camera import Camera
import CircleUtilities as Cutils
running = True
frameCounter = 0
havingcells = []
def do_vision(frame):
    circles, mask = Cutils.find_circles(frame)
    if len(circles) == 1:
        # assuming one circle in circles
        d, a = visionMath.locateCell(circles[0])
        havingcells.append(1)
        text = f"{d * 100:.1f} cm  {math.degrees(a):.1f} deg"
        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        Cutils.draw_circles(frame, circles)
    havingcells.append(0)
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

cap = Camera(consts.PORT, exposure=-6)

while True:
    frameCounter +=1
    if frameCounter == 3:
        if havingcells[0] == 1 or havingcells[1] == 1 or havingcells[2] == 1:
            anyCells = True
        else:
            anyCells = False
        #Add sending the info to guys group if theres any cells and the cells themselfs
        frameCounter = 0
    frame = cap.read()
    do_vision(frame)

    key = cv2.waitKey(1 if running else 0)
    if key & 0xff == ord('q'):
        break
    elif key > 0:
        running = not running

cv2.destroyAllWindows()
cap.die()

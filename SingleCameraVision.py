import cv2
import numpy as np
import visionMath
import consts
import math
from Camera import Camera
import CircleUtilities as Cutils
running = True
cellCounter = 0
result = [-999,-999] #it's impossible to get these values, i just failproofed this part so deal with these numbers
def do_vision(frame, cellCounter):
    circles, mask = Cutils.find_circles(frame)
    if len(circles) == 1:
        # assuming one circle in circles
        d, a = visionMath.locateCell(circles[0])
        result[0] = d
        result[1] = a
        cellCounter = 0
        if result[0] == -999 and result[1] == -999:
            text = "There are no circles in sight for now, oh no! This is not work! Call someone! Help me!"  # delete this later
        elif result[0] < 0.45:
            text = "THe Ball is too close to the camera!"
        else:
            text = f"{result[0] * 100:.1f} cm  {math.degrees(result[1]):.1f} deg"
        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        Cutils.draw_circles(frame, circles)
    else:
        cellCounter +=1
        text = "There are no circles in sight for now, oh no! This is not work! Call someone! Help me!" # delete this too
        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        result[0] = 100000
        result[1] = 100
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    return result
cap = Camera(consts.PORT, exposure=-6)

while True:
    if cellCounter > 2:
        result[0] = None
        result[1] = None
    frame = cap.read()
    do_vision(frame, cellCounter)
    #add sending to guy the result from do_vision something like : return result
    key = cv2.waitKey(1 if running else 0)
    if key & 0xff == ord('q'):
        break
    elif key > 0:
        running = not running

cv2.destroyAllWindows()
cap.die()

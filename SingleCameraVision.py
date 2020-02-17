# imports not from the code

import cv2
import math

# imports from the code

import transmit
import consts
import visionMath
from Camera import Camera
import CircleUtilities as Cutils

running = True  # important for stoping the runing of the code
cellCounter = 0  # number of frames in a row with no circles , if >2 returning no circles
result = [-999, -999]  # it's impossible to get these values, i just failproofed this part so deal with these numbers


# main func for finding circles
def do_vision(frame):
    global cellCounter  # counts how much frames were without circles in a row' if >2 returns no circles

    circles, mask = Cutils.find_circles(frame)

    if len(circles) == 1:  # if there is only one circle:
        cellCounter = 0  # init cellCounter
        result[0], result[1] = visionMath.locateCell(circles[0])  # result[0] = d , result[1] = a
        if result[0] == -999 and result[1] == -999:  # if there are no circles at all
            text = "There are no circles in sight for now, oh no! This is not work! Call someone! Help me!"  # delete this later
            transmit.send(result)  # sends result
        elif result[0] < 0.45:
            text = "The Ball is too close to the camera!"
            result[0] = -999
            result[1] = -999
            transmit.send(result)  # sends result
        else:
            text = f"{result[0] * 100:.1f} cm  {math.degrees(result[1]):.1f} deg"
            result[0] = int(result[0] * 10000) / 10000
            result[1] = int(result[1] * 10000) / 10000
            transmit.send(result)  # sends result

        # draws the circles and the text on the frame
        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        Cutils.draw_circles(frame, circles)
    else:
        cellCounter += 1
        text = "There are no circles in sight for now, oh no! This is not work! Call someone! Help me!"  # delete this too
        cv2.putText(frame, text, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        result[0] = -999  # means no circles
        result[1] = -999  # means no circles
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    return result


# capturing the video
cap = Camera(consts.PORT, exposure=-6)

while True:
    if cellCounter > 2:
        result[0] = -999
        result[1] = -999
    frame = cap.read()
    do_vision(frame)

    # stop when q is pressed
    key = cv2.waitKey(1 if running else 0)
    if key & 0xff == ord('q'):
        break
    elif key > 0:
        running = not running

cv2.destroyAllWindows()
cap.die()

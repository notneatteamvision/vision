# imports not from the code

import math

import cv2

from pi import transmit, visionMath, consts, CircleUtilities as Cutils
from pi.Camera import Camera

# imports from the code

running = True  # important for stoping the runing of the code
cellCounter = 0  # number of frames in a row with no circles , if >2 returning no circles
result = [-999,
          -999]  # it's impossible to get these values, i just failproofed this part so deal with these numbers


# main func for finding circles
def do_vision(frame):
    global cellCounter  # counter if 0 circles were found cellCounter ++, if cellCounter > 2 : -> no circles

    circles, mask = Cutils.find_circles(frame)

    if len(circles) == 1:  # if there is only one circle:
        cellCounter = 0  # init cellCounter
        result[0], result[1] = visionMath.locate_cell(circles[0])  # result[0] = d , result[1] = a
        if result[0] == -999 and result[1] == -999:  # if there are no circles at all
            transmit.send(result)  # sends result

        elif result[0] < 0.45:  # if the ball is too close - ignore
            # TODO: CHECK IF 0.45 IS CORRECT
            result[0] = -999
            result[1] = -999
            transmit.send(result)  # sends result
        else:
            result[0] = int(result[0] * 10000) / 10000
            result[1] = int(result[1] * 10000) / 10000
            result[1] = math.degrees(result[1])  # change to deg
            transmit.send(result)  # transmit result

    else:
        cellCounter += 1
        result[0] = -999  # means no circles
        result[1] = -999  # means no circles

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
    cv2.waitKey(1 if running else 0)

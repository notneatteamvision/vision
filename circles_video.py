import cv2
import imutils, math
import numpy as np

FOCAL_LENGTH = 678.5

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

print(cap.isOpened())

while True:
    ret, frame = cap.read()
    # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, np.array([21, 56, 30]), np.array([47, 255, 255]))
    # filter = cv2.bitwise_and(frame, frame, mask=mask)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 100, maxRadius=100)
    edges = cv2.Canny(frame, 5, 200, 3)
    bedges = cv2.GaussianBlur(edges, (7, 7), 0)
    circles = cv2.HoughCircles(bedges, cv2.HOUGH_GRADIENT, 2, 100, maxRadius=100)

    if (isinstance(circles, np.ndarray) and len(circles)) or circles != None:
        circles = np.uint16(np.around(circles))
        # gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

    cv2.imshow('frame', frame)


    if cv2.waitKey(1) > 0:
        break

cv2.destroyAllWindows()

cap.release()



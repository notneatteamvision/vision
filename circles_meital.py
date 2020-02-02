import cv2
import numpy as np
import cellsLocator
import consts

yellow = [np.array([19, 70, 20]), np.array([40, 255, 255])]

cap = cv2.VideoCapture(0 )
cap.set(cv2.CAP_PROP_EXPOSURE, -6)

running = True


def checkCircle(image, circle, crange=yellow):
    global cx, cy
    cx, cy, cr = circle
    hr = int(cr / 2)  # half radius
    pixels = (
        (cx, cy), (cx + hr, cy), (cx - hr, cy), (cx, cy + hr),
        (cx, cy - hr))  # [center, righter, lefter, higher, lower]
    avgColor = np.mean(np.array([image[y, x] for (x, y) in pixels]))
    # lower = np.greater_equal(crange[0])
    print(f"height {consts.VIDEO_HEIGHT} object height: {cy}")


def drawCircles(image, circles):
    global cy, cx
    for i in circles:
        cx = i[0]
        cy = i[1]
        # draw the outer circle
        cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)


while True:
    ret, frame = cap.read()
    assert ret  # TODO REMOVE THIS AAAAA

    blurred = cv2.GaussianBlur(frame, (7, 7), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, yellow[0], yellow[1])
    morph = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

    edges = cv2.Canny(morph, 10, 200, 3)
    bedges = cv2.GaussianBlur(edges, (7, 7), 0)

    circles = cv2.HoughCircles(bedges, cv2.HOUGH_GRADIENT, 2, 100, maxRadius=100)

    display = frame.copy()
    if (isinstance(circles, np.ndarray) and len(circles)) or circles != None:
        # draw the circles
        circles = np.uint16(np.around(circles))[0]
        drawCircles(display, circles)
        # find the cell's relative location
        for circle in circles:
            cell_location = cellsLocator.locateCell(circle)
            # print(cell_location)
            text = f"{cell_location[0]*100:.1f} cm  {cell_location[1]:.1f} deg"
            cv2.putText(display, text, (circle[0], circle[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Display', display)

    key = cv2.waitKey(1 if running else 0)
    if key & 0xff == ord('q'):
        break
    elif key > 0:
        running = not running

cv2.destroyAllWindows()
cap.release()

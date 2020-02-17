# imports not from the code

import cv2
from imutils import grab_contours
import numpy as np
from math import sqrt

<<<<<<< Updated upstream
# imports from the code

import consts

# only green (there are green leds on the camera)
LOWER_GREEN = np.array([20, 150, 25])
UPPER_GREEN = np.array([90, 255, 110])
=======
LOWER_GREEN = np.array([10, 200, 30])
UPPER_GREEN = np.array([100, 255, 160])
>>>>>>> Stashed changes

ACTUAL_TARGET_AREA = ((50.8 + 101.6) * 43.3578) / 2

TARGET_NOT_FOUND = 'Target not found'
TARGET_FOUND = 'Angle to target {} deg'


class Camera:
    def __init__(self, port, fov, focal_length):
        """
        :param port: the camera port for the cap read
        :param fov: the field of view
        """
        self.port = port
        self.fov = fov
        self.focal_length = focal_length
        self.cap = cv2.VideoCapture(port)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, -13)

    def camera_feed(self):
        while True:
            ret, frame = self.cap.read()
            filtered = self.filter(frame)
<<<<<<< Updated upstream
            filled = self.fill(filtered)
            edged, contours = self.find_contours(filled)
=======
            cv2.imshow("blah",filtered)
            edged, contours = self.find_contours(filtered)
            # --------------------------------------------->
            cv2.circle(frame, ROBOT_POINT, 8, (0, 0, 255), -1)
            cv2.line(frame, MIDDLE_LINE[0], MIDDLE_LINE[1], (0, 0, 255), 3)
            # <---------------------------------------------
>>>>>>> Stashed changes

            if not contours:  # if contours aren't empty/ none
                text = TARGET_NOT_FOUND
            else:
                # get the largest contour
                target = max(contours, key=cv2.contourArea)
                if cv2.contourArea(target) <= 100:
                    # in case we got some noise - limit the area to be greater than 100
                    text = 'Target not found'
                else:
<<<<<<< Updated upstream
                    #distance = self.focal_length * sqrt(ACTUAL_TARGET_AREA / cv2.contourArea(target))

=======
                    distance = self.focal_length * sqrt(ACTUAL_TARGET_AREA / cv2.contourArea(target))
                    # TODO: FIX THIS AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
>>>>>>> Stashed changes
                    self.draw_contours(frame, target)
                    self.draw_center(frame, target)
                    cx, cy = self.get_center(target)
                    angle = self.get_angle(cx)
                    print(angle)
                    #print(distance)

                    #distance = int(distance * 100) / 100
                    text = TARGET_FOUND.format(angle)

            # show images and put text
            self.display_result(frame, filtered, edged, text)
            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        self.die()

    def filter(self, frame):
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)# BGR->HSV
        filter = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)# only green
        morph = cv2.morphologyEx(filter, cv2.MORPH_DILATE, np.ones((2, 2), np.uint8))#Morphology
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))#Morphology
        return morph

    def find_contours(self, filtered): #finds contours
        edged = cv2.Canny(filtered, 35, 125)
        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return edged, grab_contours(contours)

    def draw_contours(self, frame, target): # draws the contours and creates convex hull
        hull = cv2.convexHull(target)
        cv2.drawContours(frame, [hull], 0, (255, 0, 0), 1)

    def draw_center(self, frame, target): # draws the center of a contour
        m = cv2.moments(target)
        cx = np.int(m['m10'] / m['m00'])
        cy = np.int(m['m01'] / m['m00'])
        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

    def fill(self, frame):  #fills the contours
        # fills the empty image
        th, threshed = cv2.threshold(frame, 220, 255, cv2.THRESH_BINARY_INV)
        threshed_floodfill = threshed.copy()
        # Notice the size needs to be 2 pixels than the image.
        h, w = threshed.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        cv2.floodFill(threshed_floodfill, mask, (0, 0), 255)
        floodfill_inverted = cv2.bitwise_not(threshed_floodfill)
        # result = threshed | floodfill_inverted
        cv2.imshow("Thresholded Image", threshed)
        cv2.imshow("Floodfilled Image", threshed_floodfill)
        cv2.imshow("Inverted Floodfilled Image", floodfill_inverted)
        return floodfill_inverted

    def display_result(self, frame, filtered, edged, text):
        cv2.putText(frame, text, (5, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow('Display', frame)
        cv2.imshow('Filter', filtered)
        cv2.imshow('Edger', edged)

    def die(self): #die
        cv2.destroyAllWindows()
        self.cap.release()

    def get_center(self, target): #center of contour
        m = cv2.moments(target)
        cx = np.int(m['m10'] / m['m00'])
        cy = np.int(m['m01'] / m['m00'])
        return cx, cy

    def get_angle(self, cx): #finds angle to contour
        angle = (1 - 2 * cx / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV_HORIZONTAL / 2
        return angle


if __name__ == '__main__':
    cam = Camera(consts.PORT,  # camera port
                 consts.LIFECAM_FOV_HORIZONTAL,
                 consts.LIFECAM_FOCAL_LENGTH)
    try:
        cam.camera_feed()
    except Exception as e:
        cam.die()
        raise e

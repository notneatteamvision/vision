import cv2
import imutils, math
import consts
import numpy as np

LOWER_GREEN = np.array([60, 30, 30])
UPPER_GREEN = np.array([80, 255, 255])

ACTUAL_TARGET_AREA = 33.6 * 10.1

TARGET_NOT_FOUND = 'Target not found'
TARGET_FOUND = 'Distance to target {} cm'

ROBOT_POINT = (320, 480)
MIDDLE_LINE = [(320, 480), (320, 0)]


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
            edged, contours = self.find_contours(frame)
            # --------------------------------------------->
            cv2.circle(frame, ROBOT_POINT, 8, (0, 0, 255), -1)
            cv2.line(frame, MIDDLE_LINE[0], MIDDLE_LINE[1], (0, 0, 255), 3)
            # <---------------------------------------------

            if not contours:  # if contours aren't empty/ none
                text = TARGET_NOT_FOUND
            else:
                # get the largest contour
                target = max(contours, key=cv2.contourArea)
                if cv2.contourArea(target) <= 100:
                    # in case we got some noise - limit the area to be greater than 100
                    text = 'Target not found'
                else:
                    distance = self.focal_length * (ACTUAL_TARGET_AREA / cv2.contourArea(target)) ** 0.5
                    displacement = self.get_displacement(distance)
                    self.draw_contours(frame, target)
                    self.draw_center(frame, target)

                    cx, cy = self.get_center(target)
                    angle = self.get_angle(cx)
                    cv2.line(frame, (320, cy), (cx, cy), (0, 255, 0), 3)
                    cv2.line(frame, ROBOT_POINT, (cx, cy), (255, 0, 0), 3)
                    line1 = abs(320 - cx)
                    line2 = abs(cy - ROBOT_POINT[1])
                    angle = math.atan(line1 / line2) * 180 / math.pi
                    print(angle)

                    distance = int(distance * 100) / 100
                    text = TARGET_FOUND.format(distance)  # change to displacement

            # show images and put text
            self.display_result(frame, filtered, edged, text)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        self.die()

    def filter(self, frame):
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        return cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

    def find_contours(self, filtered):
        edged = cv2.Canny(filtered, 35, 125)
        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return edged, imutils.grab_contours(contours)

    def draw_contours(self, frame, target):
        hull = cv2.convexHull(target)
        cv2.drawContours(frame, [hull], 0, (255, 0, 0), 1)

    def draw_center(self, frame, target):
        m = cv2.moments(target)
        cx = np.int(m['m10'] / m['m00'])
        cy = np.int(m['m01'] / m['m00'])
        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

    def display_result(self, frame, filtered, edged, text):
        cv2.putText(frame, text, (5, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        cv2.imshow('Display', frame)
        cv2.imshow('Filter', filtered)
        cv2.imshow('Edger', edged)

    def die(self):
        cv2.destroyAllWindows()
        self.cap.release()

    def get_center(self, target):
        m = cv2.moments(target)
        cx = np.int(m['m10'] / m['m00'])
        cy = np.int(m['m01'] / m['m00'])
        return cx, cy
    
    def get_displacement(self, distance):
        # TODO FIX THE CONST- UNITS -------------------------------------------------------------------------------ASAP
        # finds the distance vector from the robot to the target
        height_diff = consts.CAMERA_HEIGHT - consts.TARGET_HEIGHT_CENTER
        displaced_distance = math.sqrt(distance ** 2 - height_diff ** 2)
        return displaced_distance

    def get_angle(self, cx):
        angle = (1 - 2 * cx / consts.VIDEO_WIDTH) * consts.LIFECAM_FOV_HORIZONTAL / 2
        return angle


if __name__ == '__main__':
    cam = Camera(1,  # camera port
                 consts.LIFECAM_FOV_HORIZONTAL,
                 consts.LIFECAM_FOCAL_LENGTH)
    try:
        cam.camera_feed()
    except Exception as e:
        cam.die()
        raise e

import cv2
import consts

class Camera:
    def __init__(self, port:int, **kwargs):
        self.port = port
        self.exposure = kwargs.get('exposure', -4)
        self.focal_length = kwargs.get('focal_length', consts.LIFECAM_FOCAL_LENGTH)
        self.fov = kwargs.get('fov', (consts.LIFECAM_FOV_HORIZONTAL, consts.LIFECAM_FOV_VERTICAL))

        self.cap = cv2.VideoCapture(self.port)
        self.cap.set(cv2.CAP_PROP_EXPOSURE, self.exposure)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, consts.VIDEO_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, consts.VIDEO_HEIGHT)

    def read(self):
        assert(self.cap.isOpened(), "can't read from closed camera")
        ret, frame = self.cap.read()
        assert(ret, "unable to read from camera")
        return frame

    def die(self):
        self.cap.release()
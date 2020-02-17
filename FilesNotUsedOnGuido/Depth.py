import cv2
from Camera import Camera

PORT_LEFT = 1
PORT_RIGHT = 0

camLeft = Camera(PORT_LEFT, exposure=-6)
camRight = Camera(PORT_RIGHT, exposure=-6)

frameLeft, frameRight = camLeft.read(), camRight.read()

cv2.imshow('Left', frameLeft)
cv2.imshow('Right', frameRight)

cv2.waitKey(0)

stereo = cv2.StereoBM(numDisparities=16, blockSize=15)
disparity = stereo.compute(frameLeft,frameRight)
cv2.imshow('STEREO', disparity)

cv2.waitKey(0)

cv2.destroyAllWindows()
camLeft.die()
camRight.die()
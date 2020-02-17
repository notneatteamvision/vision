import cv2

cap = cv2.VideoCapture(0)
print(cap.isOpened())

while True:
    ret, frame = cap.read()

    assert ret # if failed then something went wrong with the video capture

    cv2.imshow("display", frame)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
import cv2 as cv 
import numpy as np

cam = cv.VideoCapture(0)

def callback(event,x,y,flags,params):
    if event == cv.EVENT_LBUTTONDOWN:
        print('the event is: ' ,event)

while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    cv.namedWindow('S3-Cam',cv.WINDOW_NORMAL)
    cv.resizeWindow('S3-Cam', 800,600)
    cv.setMouseCallback('S3-Cam',callback)

    cv.imshow('S3-Cam',frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
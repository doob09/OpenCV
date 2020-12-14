import cv2 as cv 
import numpy as np

cam = cv.VideoCapture(0)
cv.namedWindow('S3-Cam',cv.WINDOW_NORMAL)
cv.resizeWindow('S3-Cam', 800,600)

while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    
    cv.imshow('S3-Cam',frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
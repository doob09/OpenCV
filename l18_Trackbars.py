
import cv2 as cv 
import numpy as np 

cam = cv.VideoCapture(0)

while True:
    resl,frame = cam.read()
    if resl == False:
        print('There is no input')
        break
    cv.namedWindow('Note3-Cam',cv.WINDOW_NORMAL)
    cv.resizeWindow('Note3-Cam',800,600)
    cv.imshow('Note3-Cam',frame)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()    
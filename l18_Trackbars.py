import cv2 as cv 
import numpy as np 

def callback(x):
    pass

cam = cv.VideoCapture(0)
#Create a window/canvas with title and resize to 800 x 600
cv.namedWindow('Note3-Cam',cv.WINDOW_NORMAL)
cv.resizeWindow('Note3-Cam',800,600)
#Create Trackbar on window/canvas
cv.createTrackbar('xSlide' ,'Note3-Cam', 20, 800, callback)
cv.createTrackbar('ySlide', 'Note3-Cam', 20, 600, callback)

while True:
    resl,frame = cam.read()
    if resl == False:
        print('There is no input')
        break
    xVal = cv.getTrackbarPos('xSlide','Note3-Cam')
    yVal  = cv.getTrackbarPos('ySlide','Note3-Cam')
    cv.circle(frame,(xVal,yVal), 10 , (110,153,135), -1)
    cv.imshow('Note3-Cam',frame)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()    
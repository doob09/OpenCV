import cv2 as cv 
import numpy as np 

def callback(x):
    pass

cam = cv.VideoCapture(0)
#Create a window/canvas with title and resize to 800 x 600
cv.namedWindow('Note3-Cam',cv.WINDOW_NORMAL)
cv.resizeWindow('Note3-Cam',800,600)
#Create Trackbar on window/canvas
cv.createTrackbar('xSlide' ,'Note3-Cam', 20, 1200, callback)
cv.createTrackbar('ySlide', 'Note3-Cam', 20, 800, callback)

cv.createTrackbar('box-width', 'Note3-Cam', 60,1200, callback)
cv.createTrackbar('box-height', 'Note3-Cam', 30,800, callback)
w = 80
h = 60

while True:
    resl,frame = cam.read()
    if resl == False:
        print('There is no input')
        break
    xVal = cv.getTrackbarPos('xSlide','Note3-Cam')
    yVal  = cv.getTrackbarPos('ySlide','Note3-Cam')
    b_w = cv.getTrackbarPos('box-width','Note3-Cam')
    b_h = cv.getTrackbarPos('box-height','Note3-Cam')

    cv.rectangle(frame,(xVal,yVal),(xVal+b_w,yVal+b_h),(0,255,0), 3)
    cv.imshow('Note3-Cam',frame)

    if cv.waitKey(1)==ord('q'):
        break

cam.release()
cv.destroyAllWindows()    
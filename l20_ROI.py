
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
    roi = frame[75:400, 100:600].copy() # Region Of Interest
    roiGray = cv.cvtColor(roi,cv.COLOR_BGR2GRAY) # convert into Gray ->reduce channel to 1

    frame[75:400,100:600] = [0,255,0] # paint Green for the region
    cv.imshow('ROI', roi)
    cv.moveWindow('ROI', 0, 700)
    cv.imshow('S3-Cam',frame)
    keyEvent = cv.waitKey(1) # this create key event list if any  match will do ..
    if keyEvent == ord('q'):
        break
    if keyEvent == ord('f'):
        print(frame.shape)

cam.release()
cv.destroyAllWindows()
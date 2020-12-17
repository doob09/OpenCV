import cv2 as cv 
import numpy as np

def callback(x):
    pass

cv.namedWindow('Trackbars')
cv.moveWindow('Trackbars',800,10)

# hue: 0 -> 180 : a circle
cv.createTrackbar('hueLower','Trackbars',50,179,callback)
cv.createTrackbar('hueUpper','Trackbars',100,179 ,callback)
# saturation : line : 0 -> 255
cv.createTrackbar('satLow','Trackbars',100,255 ,callback)
cv.createTrackbar('satHigh','Trackbars',255,255 ,callback)
# value/lightness: line: 0 -> 255
cv.createTrackbar('valLow','Trackbars',100,255 ,callback)
cv.createTrackbar('valHigh','Trackbars',100,255 ,callback)


cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)

while True:
    #resl , frame = cam.read()
    frame = cv.imread('images/smarties.png')
    # if resl == False:
    #     print('There is no Video')
    #     break
    
    #resize the resolution of the frame
    ratio = 0.6
    new_width = int(frame.shape[1] * ratio)
    new_height = int(frame.shape[0] * ratio)
    #dim = (new_width, new_height)
    dim = (640,480)
    resized_frame = cv.resize(frame,dim, interpolation = cv.INTER_AREA)

    #convert BGR image into  HSV
    hsv = cv.cvtColor(resized_frame,cv.COLOR_BGR2HSV)

    cv.imshow('LG-Cam',resized_frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()


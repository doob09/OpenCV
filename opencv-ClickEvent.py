import cv2 as cv 
import numpy as np

cam = cv.VideoCapture(0)
evt = False
point = ()
points_list = []

def callback(event,x,y,flags,params):
    global evt
    #global point
    if event == cv.EVENT_LBUTTONDOWN:
        print('the event is: ' ,event)
        evt = event
        point=(x,y)
        print(point)
        points_list.append(point)

while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    cv.namedWindow('S3-Cam',cv.WINDOW_NORMAL)
    cv.resizeWindow('S3-Cam', 800,600)
    cv.setMouseCallback('S3-Cam',callback) # give the mouse event and location of the mouse
    if bool(evt) == True:
        # print(bool(evt))
        #cv.circle(frame, point ,10, (142,142,123),-1)
        pass
    for p in points_list:
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.circle(frame, p , 10 , (0,255,255), -1)
        cv.putText(frame, str(p), p, font, 2, (0,255,0),3 )
    cv.imshow('S3-Cam',frame)
    keyEvent = cv.waitKey(1)
    if keyEvent == ord('q'):
        break
    if keyEvent == ord('c'):
        points_list = []

cam.release()
cv.destroyAllWindows()
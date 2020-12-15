
import cv2 as cv 
import numpy as np
import math

draw = False

dx = 30
dy = 30

# callback function for Mouse Events
def callback(event,x,y,flags,params):
    #Define varibale for local and set as global to be accessible by other function
    global x1,y1,x2,y2
    global draw 
    if event == cv.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        draw = False # reset the value when draw another rectangle
    if event == cv.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        draw = True 

# def cal_distance(point1,point2):
#     rel = math.sqrt(  (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2  )
#     return rel


''' 
Capture the video
Create window with title
Set mouse event listener to the window
'''
cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)
cv.setMouseCallback('LG-Cam',callback)

#Show the video
while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    
    #resize the resolution of the frame
    ratio = 0.6
    new_width = int(frame.shape[1] * ratio)
    new_height = int(frame.shape[0] * ratio)
    dim = (new_width, new_height)
    resized_frame = cv.resize(frame,dim, interpolation = cv.INTER_AREA)

    # Create A condition - True or False to go to another path
    # OR do change the conditon of global variable to void this path
    # ONLY Create a rectangle if there are 2 points or sth True
    # not -- to check empty variable
    if draw and  x1 != x2 :
        
        cv.rectangle(resized_frame, (x1,y1), (x2,y2), (0,255,0) , 3)
        roi = resized_frame[y1:y2, x1:x2]
        cv.imshow('ROI',roi)

    
    cv.imshow('LG-Cam',resized_frame)
    keyEvent = cv.waitKey(1)
    if keyEvent == ord('q'):
        break
    if keyEvent == ord('d'):
        x1 += dx
        x2 += dx
        if x2 >= new_width:
            pass
            x2 = new_width  
    if keyEvent == ord('a'):
        x1 -= dx
        x2 -= dx
        if x1 < 0:
            pass
cam.release()
cv.destroyAllWindows()
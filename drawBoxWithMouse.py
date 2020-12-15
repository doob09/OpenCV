
import cv2 as cv 
import numpy as np
import math

st_point = ()
ed_point = ()

# callback function for Mouse Events
def callback(event,x,y,flags,params):
    global st_point
    global ed_point 
    if event == cv.EVENT_LBUTTONDOWN:
        ed_point =()
        st_point = (x,y)
    if event == cv.EVENT_LBUTTONUP:
        ed_point =(x,y)

# def cal_distance(point1,point2):
#     rel = math.sqrt(  (point2[0] - point1[0])**2 + (point2[1] - point1[1])**2  )
#     return rel


''' 
Capture the video
Create window with title
Set mousr event listener to the window
'''
cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)
cv.setMouseCallback('LG-Cam',callback)

col =0
row =0 
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
    # ONLY Create a rectangle if there are 2 points
    if  st_point and ed_point: 
        cv.rectangle(resized_frame, st_point, ed_point, (0,255,0), 3)
        # Create Region Of Interest
        roi = resized_frame[st_point[1]: ed_point[1], st_point[0]: ed_point[0]]
        cv.imshow('ROI',roi)
    
    cv.imshow('LG-Cam',resized_frame)
    if cv.waitKey(1) == ord('q'):
        break
    
cam.release()
cv.destroyAllWindows()
import cv2 as cv
import numpy as np 

cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)

x_start = 50
y_start = 50
box_ratio = 0.15
dx = 1
dy = 2

while True:
    resl, frame = cam.read()
    if resl == False:
        print ('There is no Video')
        break
    
    #resize the resolution of the frame
    ratio = 0.6
    new_width = int(frame.shape[1] * ratio)
    new_height = int(frame.shape[0] * ratio)
    dim = (new_width, new_height)
    resized_frame = cv.resize(frame,dim, interpolation = cv.INTER_AREA)
    
    #Boucing Box
    b_w = int(box_ratio * new_width) #define width of the box
    b_h = int(box_ratio * new_height) # define the height of the box
    ''' 
    copy the color region
    convert frame into gray
    convert frame back into color to get the right shape = color image shape
    assign color region -> gray region
    '''    
    roi = resized_frame [ y_start: y_start + b_h,  x_start: x_start + b_w].copy() 
    gray_frame = cv.cvtColor(resized_frame, cv.COLOR_BGR2GRAY)
    fake_color = cv.cvtColor(gray_frame, cv.COLOR_GRAY2BGR)
    fake_color[ y_start: y_start + b_h, x_start:x_start + b_w] = roi
    cv.rectangle(fake_color,(x_start,y_start),(x_start + b_w, y_start + b_h), (0,255,0), 3)
    x_start = x_start + dx
    y_start = y_start + dy
    if x_start <= 0 or x_start + b_w > new_width :
        dx = -1 * dx
    if  y_start <= 0 or y_start +b_h >= new_height :
        dy = -1 * dy
        
    cv.imshow('LG-Cam', fake_color)
    keyEvent = cv.waitKey(1)
    if keyEvent == ord('q'):
        break

cam.release()
cv.destroyAllWindows()



import cv2 as cv 
import numpy as np

def callback(x):
    pass

cv.namedWindow('Trackbars')
cv.moveWindow('Trackbars',800,10)

# hue: 0 -> 180 : a circle - Need to refer to opencv hsv Color picker
cv.createTrackbar('hueLower','Trackbars',77,179,callback)
cv.createTrackbar('hueUpper','Trackbars',134,179 ,callback)

#Another hue selection to solve RED range picker
cv.createTrackbar('hL2','Trackbars',179,179, callback)
cv.createTrackbar('hU2','Trackbars',179,179,callback)

# saturation : line : 0 -> 255
cv.createTrackbar('satLow','Trackbars',135,255 ,callback)
cv.createTrackbar('satHigh','Trackbars',255,255 ,callback)
# value/lightness: line: 0 -> 255
cv.createTrackbar('valLow','Trackbars',35,255 ,callback)
cv.createTrackbar('valHigh','Trackbars',154,255 ,callback)


cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)

while True:
    resl , frame = cam.read()
    #frame = cv.imread('images/smarties.png')
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
    #add Blur to frame to reduce noise
    resized_frame = cv.GaussianBlur(resized_frame, (5,5), 0)
    #convert BGR image into  HSV
    hsv = cv.cvtColor(resized_frame,cv.COLOR_BGR2HSV)

    #* get the value from Trackbar
    # Get color in a range (hueLower,hueUpper) to get wide cover than a number
    hueLower = cv.getTrackbarPos('hueLower','Trackbars')
    hueUpper = cv.getTrackbarPos('hueUpper', 'Trackbars')
    # Pick another hue section to show 
    hL2 = cv.getTrackbarPos('hL2','Trackbars')
    hU2 = cv.getTrackbarPos('hU2', 'Trackbars')

    # Saturation from a range not by specific number to get wideq cover
    satLow = cv.getTrackbarPos('satLow','Trackbars')
    satHigh = cv.getTrackbarPos('satHigh', 'Trackbars')

    # Lightness
    liLow = cv.getTrackbarPos('valLow','Trackbars')
    liHigh = cv.getTrackbarPos('valHigh','Trackbars')

    # Create bound in hsv format: low - high
    low_bound = np.array([hueLower, satLow, liLow])
    high_bound = np.array([hueUpper, satHigh, liHigh])

    # Another set of bound since another hue section is selected
    l_b2 =np.array([hL2,satLow,liLow])
    h_b2 = np.array([hU2,satHigh,liHigh])
    
    #* Create Foreground Mask - filter what you care
    # get the value in range hsv : value turn into White: 1  if in range
    # inRange function convert image into gray
    fgMask = cv.inRange(hsv,low_bound, high_bound)
    fgMask2 = cv.inRange(hsv,l_b2,h_b2)
    maskComp = cv.add(fgMask, fgMask2)
    cv.imshow('FG-MASKComp',maskComp)

    # Create a contour around the object from the mask
    # get a simple outside bound of contour with at least dot 
    contours,_ = cv.findContours(maskComp,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    
    # Calculate contour area 
    # Sort  0 to max , reverse to get max value first
    #contours = sorted(contours, key = lambda x: cv.contourArea(x),reverse=True)
    #draw first one or all of the contour on frame with value -1
    #cv.drawContours(resized_frame,contours,0,(0,255,0),3)
    
    # Draw more contour with threshode area
    for cnt in contours:
        area = cv.contourArea(cnt)
        # get the coordinate of rectangle of each contour
        # cv function create rectagle based on the mask
        # based on the region of color is hightlight => create roi[r,c]
        (x,y,w,h) = cv.boundingRect(cnt)
        if area >= 150:
            #cv.drawContours(resized_frame, [cnt],0,(0,0,255),3)
            #draw the rectangle
            cv.rectangle(resized_frame,(x,y),(x+w,y+h),(0,255,255),3)
    
    cv.imshow('LG-Cam',resized_frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()


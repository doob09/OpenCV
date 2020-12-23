import cv2 as cv 
import numpy as np
import time
from adafruit_servokit import ServoKit

timeMark = time.time()
dtFIL = 0

camW = 640
camH = 480

ser = ServoKit(channels=16)                                                   
pan = 90
ser.servo[0].angle = 90

dPan = 3
obj = False

def callback(x):
    pass

cv.namedWindow('Trackbar')
cv.createTrackbar('HueLower','Trackbar',71,179,callback)
cv.createTrackbar('HueUpper','Trackbar',130,179, callback)
cv.createTrackbar('HueLower_2','Trackbar',179,179, callback)
cv.createTrackbar('HueUpper_2','Trackbar',179,179, callback)

cv.createTrackbar('SatLower','Trackbar',150,255,callback)
cv.createTrackbar('SatUpper','Trackbar',255,255,callback)

cv.createTrackbar('LightLower','Trackbar',29,255,callback)
cv.createTrackbar('LightUpper','Trackbar',255,255,callback)

cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)


while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    #filter the frame
    dt = time.time() - timeMark
    timeMark = time.time()
    dtFIL = .9*dtFIL + .1*dt
    fps = 1/dtFIL

    #resize the resolution of the frame
    ratio = 0.6
    new_width = int(frame.shape[1] * ratio)
    new_height = int(frame.shape[0] * ratio)
    #dim = (new_width, new_height)
    dim = (camW,camH)
    resized_frame = cv.resize(frame,dim, interpolation = cv.INTER_AREA)
    cv.putText(resized_frame,'fps: '+ str(round(fps,2)), (10,20), cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
    #reduce noise
    cv.GaussianBlur(resized_frame, (5,5), 0 )
    #convert color RGB into HSL
    hsv = cv.cvtColor(resized_frame, cv.COLOR_BGR2HSV)
   

    #* Get value from trackbar
    HueLower = cv.getTrackbarPos('HueLower','Trackbar')
    HueUpper = cv.getTrackbarPos('HueUpper','Trackbar')
    HueLower_2 = cv.getTrackbarPos('HueLower_2','Trackbar')
    HueUpper_2 = cv.getTrackbarPos('HueUpper_2','Trackbar')

    SatLower = cv.getTrackbarPos('SatLower','Trackbar')
    SatUpper = cv.getTrackbarPos('SatUpper','Trackbar')

    LiLower = cv.getTrackbarPos('LightLower','Trackbar')
    LiUpper = cv.getTrackbarPos('LightUpper','Trackbar')

    # Save value in HSV format in numpy array
    low_bound = np.array([HueLower,SatLower,LiLower])
    up_bound = np.array([HueUpper,SatUpper,LiUpper])
    low_bound_2 =  np.array([HueLower_2,SatLower,LiLower])
    up_bound_2 = np.array([HueUpper_2,SatUpper,LiUpper])
    
    #Create FG-Mask
    fg_1 = cv.inRange(hsv, low_bound, up_bound)
    fg_2 =  cv.inRange(hsv, low_bound_2, up_bound_2)
    fg = cv.add(fg_1,fg_2)
    cv.imshow('FG-Mask', fg)

    #Create Contour
    contours,_ = cv.findContours(fg,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #Sort the area
    contours = sorted(contours, key = lambda x: cv.contourArea(x), reverse = True)
    #Calculate area and show the one above threshold
    for cnt in contours:
        area = cv.contourArea(cnt)
        # Use cv function to create rectangle around the highlight object
        (x,y,wb,hb) = cv.boundingRect(cnt)
        if area >= 150:
            wb = int(x+ wb/2)
            hb = int(y+ hb/2)
            #center point for the Rectangle   
            cv.circle(resized_frame,(wb,hb),4,(125,165,56),-1)

            ''' calculate the error:
            err/distance = center of the cam - center of rectangle
            if the error is more than in range 0~5 
                Cr needs to move forward to the Cc to reduce the distance
                unitl err = 0~5 => 2 point a the same
                (or dx , dy of Cr need to move => Creating Verlocity)
            => pan needs to move
            => til needs to move
            '''
            err = camW/2 - wb
            #abs return an inter, float, or a complex number without sign
            print('abs(err): ',abs(err))
            if abs(err) > 10:
                print('scale error: ',err/100)
                pan = pan + err/100
            if pan > 180:
                pan = 180
                print('Out of range 180')
            if pan < 0:
                pan = 0    
                print('Out of range 0')
            ser.servo[0].angle = pan
            # put break to loop through array for the first element only 
            # not for the whole array
            break

    #Center of the Rexct (x+wb/2, y+hb/2)
    ''' Pan  or x-axis : PanTil Position at 90
    center of the Cemara -  center of the box = distance 
    if distance > 0 : PanTil move negative way 
    if distance < 0 : PanTil move positive way
    '''
    print('pan init',pan)      
    print('--------------')
    cv.circle(resized_frame, (320,240),3, (0,0,255), 3) 
    cv.imshow('LG-Cam',resized_frame)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
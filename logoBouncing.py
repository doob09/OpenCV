
import cv2 as cv 
import numpy as np


x = 100
y = 100
b_w = 70
b_h = 50

dx = 5
dy = 5

#Read the video
cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)

#Read the image
pyLogo = cv.imread('images/pl.jpg')
pyLogo = cv.resize(pyLogo,(b_w,b_h))
cv.imshow('PyLogo', pyLogo)
cv.moveWindow('PyLogo',10,800)
print(pyLogo.shape)

#! Create MASKS
grayLogo = cv.cvtColor(pyLogo, cv.COLOR_BGR2GRAY)
cv.imshow('GRAY',grayLogo)
cv.moveWindow('GRAY',650,10)

#* Creating Background MASK - need threshold to take the shape needed 
#*  -> set the pixel to be 0-BlACK 
# pixel > threshold: =>255 = White - 1
# pixel < threshold: => 0 = BLACK - 0  
_,bgMask = cv.threshold(grayLogo,225, 255, cv.THRESH_BINARY)
cv.imshow('BG-MASK',bgMask)
cv.moveWindow('BG-MASK',650,400)

#* Foreground MASK 
fgMask = cv.bitwise_not(bgMask)
cv.imshow('FG-MASK',fgMask)
cv.moveWindow('FG-MASK',1300,400)

while True:
    resl , frame = cam.read()
    if resl == False:
        print('There is no Video')
        break
    
    #resize the resolution of the frame
    ratio = 0.6
    new_width = int(frame.shape[1] * ratio)
    new_height = int(frame.shape[0] * ratio)
    #dim = (new_width, new_height)
    dim = (640,480)
    resized_frame = cv.resize(frame,dim, interpolation = cv.INTER_AREA)

    #Bouncing Box : Cut row and column from image 
    #rect = cv.rectangle(resized_frame,(x,y),(x+b_w, y+b_h), (0,255,0),-1)
    rect = resized_frame[y:y+b_h,x:x+b_w]
    
    x += dx
    y += dy
    if x <=0 or x+b_w >= 640:
        dx = -1 * dx
    if y <=0 or y+b_h >= 480:
        dy = -1 * dy
    
    #* Combine background with BG-Mask
    bg = cv.bitwise_and(rect,rect, mask=bgMask)
    cv.imshow('BG-img + BG-MASK',bg)
    cv.moveWindow('BG-img + BG-MASK',650,600)
    
    #* Combine PyLogo with FG-Mask
    fg = cv.bitwise_and(pyLogo,pyLogo, mask=fgMask)
    cv.imshow('PyLogo + FG-MASK',fg)
    cv.moveWindow('PyLogo + FG-MASK',1300,600)
    
    #! Add 2 Regions together
    bolo =cv.add(bg,fg)
    cv.imshow('Final',bolo)
    cv.moveWindow('Final',650,1000)
    
    #assign the value from final result to rectangle in camera
    rect[:] = bolo[:]

    cv.imshow('LG-Cam',resized_frame)
    cv.moveWindow('LG-Cam',10,10)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
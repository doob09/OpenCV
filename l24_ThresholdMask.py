
import cv2 as cv 
import numpy as np

''' 
Mask technique to take out what you want of 2 images and combine them together
'''
def callback(x):
    pass

# Create slide bar for blended image:
cv.namedWindow('Bld-Img')
cv.createTrackbar('Blend Value','Bld-Img',25,100,callback)


cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)
# Gray the image to create a MASK: 
cvLogo =  cv.imread('images/cv.jpg')
cvLogo = cv.resize(cvLogo,(640,480))
grayLogo = cv.cvtColor(cvLogo,cv.COLOR_BGR2GRAY)
cv.imshow('GRAY',grayLogo)
cv.moveWindow('GRAY',10 ,800)

#Create a Binary Mask : 0-1
# BLACK:0 -- WHITE:1
# Gray Logo have colors: [ text:0 - C:150 - C:76 - C:29 - BG:255] 
# if a pixel > threshold => 1 :WHITE
# if a pixel < threshold => 0 :BLACK
# threshold test: 50 , 150 , 170
''' 
background Mask with AND logic operation : 
use with frame camera as background
color image = 1 AND background =1 => color image will shown as background =1
'''
_ , bgMask = cv.threshold(grayLogo, 220 ,255, cv.THRESH_BINARY)
cv.imshow('BG MASK', bgMask)
cv.moveWindow('BG MASK',680,10)
''' 
Frontground mask with AND GATE:
Invert the value of background: 3C and Text will be 1: White 
Use with the Original cv.jpg
logo color = 1 AND logo =1 => logo color should show up
'''
fgMask = cv.bitwise_not(bgMask)
cv.imshow('FG MASK',fgMask)
cv.moveWindow('FG MASK', 660,700)

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
    
    #Combine the background with MASK
    bg = cv.bitwise_and(resized_frame, resized_frame, mask = bgMask)
    cv.imshow('BG-img + BG-MASK', bg)
    cv.moveWindow('BG-img + BG-MASK', 1300,10)

    #Combine the original cv.jpg with MASK
    fg = cv.bitwise_and(cvLogo,cvLogo, mask = fgMask)
    cv.imshow('Org-CV + FG-MASK',fg)
    cv.moveWindow('Org-CV + FG-MASK',1300,700)

    #! Version 1
    #!Combine/Add 2 matrices 'BG-img + BG-MASK' + 'Org-CV + FG-MASK' together
    # 0:BLACK + Anything/Color => Anything/Color
    bov = cv.add(bg,fg)
    cv.imshow('Add 2 Regions',bov)
    cv.moveWindow('Add 2 Regions', 10 , 1400)

    # * Create Blended Image 
    # Add slide
    # devide by 100 to get the value from 0 - 1
    bl_val1 = cv.getTrackbarPos('Blend Value','Bld-Img')/100 
    bl_val2 = 1 - bl_val1

    blended = cv.addWeighted(resized_frame, bl_val1, cvLogo, bl_val2, 0)
    cv.imshow('Bld-Img',blended)
    cv.moveWindow('Bld-Img', 650 , 1400)

   

    # * NEW FG-MASK  =  Bld-Img + FG-MASK
    fg_bl = cv.bitwise_and(blended,blended, mask = fgMask)
    cv.imshow('FG-MASK_2',fg_bl)
    cv.moveWindow('FG-MASK_2', 1300, 1400)

    #! Version 2 - More control
    #! Combine/Add 2 matrices 'BG-img + BG-MASK' + 'Bld-Img + FG-MASK' 
    bov_2 = cv.add(bg,fg_bl)
    cv.imshow('Version_2', bov_2)
    cv.moveWindow('Version_2', 1950, 1400)

    cv.imshow('LG-Cam',resized_frame)
    cv.moveWindow('LG-Cam', 10,10)
    #cv.imshow('CV LOGO',cvLogo)
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
import cv2 as cv 
import numpy as np

img1 = np.zeros((480,640,1),np.uint8) # 0 for BLACK - 1 for WHITE
img1[0:480,0:300] = [255] # assgin color for 1 channel image

img2 = np.zeros((480,640,1), np.uint8)
img2[190:290,290:370] = [255]

bitAnd = cv.bitwise_and(img1,img2) # AND logic for 2 images - 1 & 1 => 1 WHITE
bitOr = cv.bitwise_or(img1,img2) # OR logic 0 & 0 => 0 BLACK
bitXOr = cv.bitwise_xor(img1,img2) # Xor Logic

cam = cv.VideoCapture(0)
cv.namedWindow('LG-Cam',cv.WINDOW_AUTOSIZE)

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

    cv.imshow('LG-Cam',resized_frame)

    cv.imshow('Image 1',img1)
    #cv.moveWindow('Image 1', 100 ,1400)

    cv.imshow('Image 2',img2)
    #cv.moveWindow('Image 2', 760,1400)

    cv.imshow('AND LOGIC', bitAnd)
    #cv.moveWindow('AND LOGIC',100 ,760 )

    cv.imshow('OR LOGIC', bitOr)

    cv.imshow('Xor LOGIC', bitXOr)

    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()

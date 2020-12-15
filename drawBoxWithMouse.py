
import cv2 as cv 
import numpy as np

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
    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
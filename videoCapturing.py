import cv2
import os
import time



print(os.path.isfile("sample.mp4"))

def extractImages():
    count = 0
    vidcap = cv2.VideoCapture("sample.mp4")
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
        success,image = vidcap.read()
        print ('Read a new frame: ', success)
        cv2.imwrite("data/frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
    

extractImages()








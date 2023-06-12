import face_recognition
import os
import numpy as np
import cv2


mydict ={"face1":{"encoding":"asdasd","frame":"1 2 3"},
         "face2":{"encoding":"qweqweqwe","frame":"4 5 6"}}

for i in mydict:
    print(mydict[i]["encoding"])

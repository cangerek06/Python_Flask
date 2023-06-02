import cv2
import os
import time
import face_recognition
import numpy as np
import db_operations



KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2


known_faces = []
known_names = []

bilgiler = []
celalKayit =[]
aliKayit =[]
besimKayit=[]


def KisiTanimla(Id):

    """
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))"""

    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            image =cv2.imread(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            print(encoding)
            known_faces.append(encoding)
            known_names.append(name)


    print("*******************************")
    print(known_names)

    print("*******************************")

    print("bilinmeyen yüzlere bakiliyor...")
    print("*******************************")
    
    for i in range(80,len(os.listdir("data"))):
        filename = f"frame{i}.jpg"
        face_list =[]
        face_ratio_list =[]
        print("#########################")
        print(filename)
        
        print("Dosya var mi :"+str(os.path.exists(f"data/{filename}")))
        print("*****************")
        image =cv2.imread(f"data/{filename}")
        imageWidth, imageHeight, imageChannel= image.shape
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        locations = face_recognition.face_locations(image,2)
        encoding = face_recognition.face_encodings(image,locations)
        image =cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        for face_encoding, face_location, (x,y,w,h)  in zip(encoding, locations, faces):
            results = face_recognition.compare_faces(known_faces,face_encoding,TOLERANCE)
            match = None
            face_area =w * h
            print("İmage Width : "+str(imageWidth))
            print("İmage Height : "+str(imageHeight))
            print("***********************")
            print("Face Width : "+str(w))
            print("Face Height : "+str(h))
            print("***********************")
            print("İmage Area : "+str(imageHeight * imageWidth))
            print("Face Area : "+str(h * w))
            print("***********************")
            FaceRatio = (((h * w) /(imageHeight * imageWidth))*100)
            print("Ratio of Face to Image : %"+str(((h * w) /(imageHeight * imageWidth))*100))

        
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found : {match}")
                if(match =="celal"):
                    celalKayit.append((i))
                    face_list.append(("CelalSengor"))
                    face_ratio_list.append(FaceRatio)
                if(match=="ali"):
                    aliKayit.append((i))
                    face_list.append(("MehmetAliBirand"))
                    face_ratio_list.append(FaceRatio)
                if(match=="besim"):
                    besimKayit.append((i))
                    face_list.append(("BesimTibuk"))
                    face_ratio_list.append(FaceRatio)
            print("###################")

            print("facelist : "+str(face_list))
            print("face_ratio_list : "+str(face_ratio_list))
        
        db_operations.DbInitiliazer(host="localhost",dbname="flask_db",user="postgres",password="1",port=5432)
        db_operations.InsertDataToAnalyzePerFrame(host="localhost",dbname="flask_db",user="postgres",password="1",port=5432,RecievedData1=face_list,RecievedData2=face_ratio_list,videoId=Id,frameNumber = i)



                    
"""    


liste1=[1,2,3,4]
liste2=[5,6,7,8]
liste3=[9,10,11,12]

for i, j, k in zip(liste1,liste2,liste3):
    print("i : "+str(i))
    print("j : "+str(j))
    print("k : "+str(k))
    print("***********")"""


KisiTanimla(1)
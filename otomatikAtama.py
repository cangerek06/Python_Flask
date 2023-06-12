import cv2
import face_recognition
import os
import numpy
import matplotlib
import psycopg2
from dotenv import load_dotenv, dotenv_values

load_dotenv()

def deneme():
    videoURL = "videos/video2.mp4"
    savedFaces = {}
    """
    savedFaces = {"face1":{"encoding":"1.123 1.8734","SeenFrames":[1,2,5,12,15,23],"ratios":[0.78, 0.88, 0.87],"matchPoint":[]}}
    
    """
    
    videoCaptured =cv2.VideoCapture(videoURL)
    count = 0
    i = 0
    while True:
        videoCaptured.set(cv2.CAP_PROP_POS_MSEC,(count * 1000  / int(os.getenv("FRAMESPERSECOND"))))
        count +=1
        success, image = videoCaptured.read()
        try:
            image=cv2.resize(image,(0,0),fx=0.4,fy=0.4,interpolation=cv2.INTER_AREA)
        except Exception as e:
            print(e)
        
        if success:
            imageWidth, imageHeight, imageChannel = image.shape()
            img_area = imageWidth * imageHeight

            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_classifier.detectMultiScale(gray_image,scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

            locations = face_recognition.face_locations(image,model="hog")
            encodings = face_recognition.face_encodings(image,locations)

            for face_encoding,(x,y,w,h) in zip(encodings, faces):
                for savedFace in savedFaces:

                    results = face_recognition.compare_faces(savedFace["encodings"],face_encoding,tolerance=0.6)

                matching = None

                if(True in results):
                    matching = savedFaces[results.index(True)]
                    print(f"Match Found : {matching}")
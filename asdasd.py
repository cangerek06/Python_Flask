import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import psycopg2
import db_operations
import numpy as np

from dotenv import load_dotenv, dotenv_values

load_dotenv()

KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2

isRead =False


known_faces = []
known_names = []


def deneme(videoId):
    video_conn=psycopg2.connect(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
    video_cur = video_conn.cursor()
    sorgu = f"select * from videotable where id = {videoId}"

    video_cur.execute(sorgu)
    cekilenVeri =video_cur.fetchall()
    VIDEO_URL = cekilenVeri[0][1] # video table'dan video linkinin çekilmesi 

    #yazılıma önceden verilen fotolardaki yüzlerin encdo edilmesi ve isimlerinin atanması
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            image =cv2.imread(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            print(encoding)
            known_faces.append(encoding)
            known_names.append(name)

    print("Sisteme yüzler tanıtıldı")
    count = 0
    if(VIDEO_URL !=""):
        celalKayit =[]
        aliKayit =[]
        besimKayit=[]
        bilgiler = []
        print("Veritabınından Cekilen Video : "+VIDEO_URL)
        vidcap = cv2.VideoCapture(VIDEO_URL)
        success,image = vidcap.read()
        i=0
        success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
            success,image = vidcap.read()
            if(success ==False):
                break
            print (f"{str(i)} Read a new frame: "+str(success)) 
            count = count + 1
            face_list =[]
            face_ratio_list =[]
            print("classifier öncesi")
            imageWidth, imageHeight, imageChannel= image.shape
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
            print("classifier sonrası")
            bilgiler.append((i,len(faces)))
            print("face recogantion locations öncesi")
            locations = face_recognition.face_locations(image)
            print("face recogantion locations sonrası")
            encoding = face_recognition.face_encodings(image,locations)
            print("face recogantion encodings sonrası")
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
            db_operations.DbInitiliazer(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
            db_operations.InsertDataToAnalyzePerFrame(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData1=face_list,RecievedData2=face_ratio_list,videoId=videoId,frameNumber = i)
            i+=1

        db_operations.InsertDataToFaceNumberTable(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData=bilgiler,videoId=videoId)
        print("********Bilgiler**********")
        print("Celal Hoca Bilgileri :"+str((celalKayit))+" sn")
        print("Ali Bilgileri :"+str((aliKayit))+" sn")
        print("Besim Bilgileri :"+str((besimKayit))+" sn")
        print("Veritabanına Kaydediliyor.")




if __name__ =='__main__':
    db_operations.DbInitiliazer(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
    deneme(1)
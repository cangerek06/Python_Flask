import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import psycopg2
import db_operations
import numpy as np

KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2

isRead =False


known_faces = []
known_names = []



def videoCek(VideoId):
    video_conn=psycopg2.connect(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
    video_cur = video_conn.cursor()
    sorgu = f"select * from videotable where id = {VideoId}"

    video_cur.execute(sorgu)
    cekilenVeri =video_cur.fetchall()
    VIDEO_URL = cekilenVeri[0][1]
    print("video URL : "+str(VIDEO_URL))
    video_conn.commit()

    video_cur.close()

    video_conn.close()
    return VIDEO_URL



def imgExtracter(Id):
    count = 0
    VIDEO_URL = videoCek(Id)
    if(VIDEO_URL !=""):
        print("Video : "+VIDEO_URL)
        vidcap = cv2.VideoCapture(VIDEO_URL)
        success,image = vidcap.read()
        path="data/video"+str(Id)
        isExists = os.path.exists(path)
        if(isExists==False):
            os.makedirs(path)
        success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
            success,image = vidcap.read()
            print ('Read a new frame: ', success)
            writeString = "data/video"+str(Id)+"/frame"+str(count)+".jpg"
            cv2.imwrite(writeString, image)    # save frame as JPEG file
            count = count + 1
    else:
        print("Veritabanında girilen Id de bir video yok")
    

def KisiTanimla(Id):

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
    celalKayit =[]
    aliKayit =[]
    besimKayit=[]
    for i in range(80, len(os.listdir(f"data/video{Id}"))):
        filename = f"frame{i}.jpg"

        
        face_list =[]
        face_ratio_list =[]
        print("#########################")
        print(filename)
        
        print("Dosya var mi :"+str(os.path.exists(f"data/video{Id}/{filename}")))
        print("*****************")
        image =cv2.imread(f"data/video{Id}/{filename}")
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
        
        db_operations.DbInitiliazer(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
        db_operations.InsertDataToAnalyzePerFrame(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData1=face_list,RecievedData2=face_ratio_list,videoId=Id,frameNumber = i)


                    
                

    print("********Bilgiler**********")
    print("Celal Hoca Bilgileri :"+str((celalKayit))+" sn")
    print("Ali Bilgileri :"+str((aliKayit))+" sn")
    print("Besim Bilgileri :"+str((besimKayit))+" sn")
    print("Veritabanına Kaydediliyor.")
    db_operations.InsertDataToAnalyzeForPerson(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),person="CelalSengor",RecievedData=celalKayit,videoId=Id)
    db_operations.InsertDataToAnalyzeForPerson(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),person="MehmetAliBirand",RecievedData=aliKayit,videoId=Id)
    db_operations.InsertDataToAnalyzeForPerson(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),person="BesimTibuk",RecievedData=besimKayit,videoId=Id)
    print("kaydedildi.")


def KafaSay(videoId):
    bilgiler=[]
    lst = os.listdir("data/video"+str(videoId))
    path ="static/"+"video"+str(videoId)
    isExists = os.path.exists(path)
    if(isExists ==False):
        os.makedirs(path)
    numberFiles = len(lst)
    for i in range(numberFiles):
        image_path ='data/video'+str(videoId)+'/frame'+str(i)+'.jpg'
        img =cv2.imread(image_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        writedPath = "/home/can/Desktop/Calismalar/CanPython/Flask/deneme/static/video"+str(videoId)+'/committed'+str(i)+".png"
        cv2.imwrite(writedPath,img_rgb)
        bilgiler.append((i,len(faces)))
    db_operations.InsertDataToFaceNumberTable(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData=bilgiler,videoId=videoId)
    print("*************************")
    print("!!! BİLGİLER !!!")
    for k in bilgiler:
        print("Saniye :"+str(k[0]))
        print("Kafa Sayısı :"+str(k[1]))


def FullCalculations():
    pass

import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import psycopg2
import db_operations
import numpy as np
import faceViewer as fd
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class faceDetector():

    def __init__(self,KNOWN_FACES_DIR, UNKNOWN_FACES_DIR, TOLERANCE, FRAME_THICKNESS, FONT_THICKNESS,videoId):
        self.KNOWN_FACES_DIR = KNOWN_FACES_DIR
        self.UNKNOWN_FACES_DIR = UNKNOWN_FACES_DIR
        self.TOLERANCE = TOLERANCE
        self.videoId = videoId
        self.FRAME_THICKNESS = FRAME_THICKNESS
        self.FONT_THICKNESS = FONT_THICKNESS

    def getFrameView(self,videoId,frameNo):
        self.videoURL = "videos/video"+str(videoId)+".mp4"
        video =cv2.VideoCapture(self.videoURL)
        video.set(cv2.CAP_PROP_POS_MSEC,frameNo*1000)
        ret, frame =video.read()

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        while True:
            
            cv2.imshow('FrameShowWindow',img_rgb)
            key = cv2.waitKey(1)
            if(key ==ord('q')):
                break

        video.release()
        cv2.destroyAllWindows()

    def face_distance(self,face_encodings, face_to_compare):
        if len(face_encodings) == 0:
            return np.empty((0))
        face_dist_value = np.linalg.norm(face_encodings - face_to_compare, axis=0)
        print('[Face Services | face_distance] Distance between two faces is {}'.format(face_dist_value))
        return face_dist_value 

    def allCalculations(self, videoId):
        known_faces = []
        known_names = []
        video_conn=psycopg2.connect(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
        video_cur = video_conn.cursor()
        sorgu = f"select * from videotable where id = {videoId}"

        video_cur.execute(sorgu)
        cekilenVeri =video_cur.fetchall()
        VIDEO_URL = cekilenVeri[0][1] # video table'dan video linkinin çekilmesi 

        #yazılıma önceden verilen fotolardaki yüzlerin encdo edilmesi ve isimlerinin atanması
        for name in os.listdir(self.KNOWN_FACES_DIR):
            for filename in os.listdir(f"{self.KNOWN_FACES_DIR}/{name}"):
                image = face_recognition.load_image_file(f"{self.KNOWN_FACES_DIR}/{name}/{filename}")
                image =cv2.imread(f"{self.KNOWN_FACES_DIR}/{name}/{filename}")
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
            i=0
            while True:
                vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000 / int(os.getenv("FRAMESPERSECOND"))))    # added this line 
                success,image = vidcap.read()
                try:
                    image =cv2.resize(image,(0, 0),fx=0.4, fy=0.4, interpolation = cv2.INTER_AREA)
                except Exception as e:
                    print(e)
                if(success ==False):
                    break
                print("can")
                print (f"{str(i)} Read a new frame: "+str(success)) 
                count = count + 1
                face_list =[]
                face_ratio_list =[]
                match_point_list = []
                print("classifier öncesi")
                imageWidth, imageHeight, imageChannel= image.shape
                img_area = imageHeight * imageWidth
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
                faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
                print("789879")
                print(faces)
                print(len(faces))
                print("789879")
                print("classifier sonrası")
                locations = face_recognition.face_locations(image,model="hog")
                print("face recogantion locations sonrası")
                encodings = face_recognition.face_encodings(image,locations)
                print("yüz sayısı: "+str(len(faces)))
                bilgiler.append((i,len(faces)))
                print("face recogantion encodings sonrası")
                image =cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
                for face_encoding, (x,y,w,h)  in zip(encodings, faces):
                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)
                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)

                    results = face_recognition.compare_faces(known_faces,face_encoding,self.TOLERANCE)


                    match = None
                    face_area =w * h
                    print("İmage Width : "+str(imageWidth))
                    print("İmage Height : "+str(imageHeight))
                    print("***********************")
                    print("Face Width : "+str(w))
                    print("Face Height : "+str(h))
                    print("***********************")
                    print("İmage Area : "+str(img_area))
                    print("Face Area : "+str(face_area))
                    print("***********************")
                    FaceRatio = (((face_area) /(imageHeight * imageWidth))*100)
                    print("Ratio of Face to Image : %"+str(FaceRatio))

                    if True in results:
                        match = known_names[results.index(True)]
                        print(f"Match Found : {match}")
                        face_distancePoint = 0
                        #print("yüz eşleşme oranı : "+str(face_distance))
                        if(match =="celal"):
                            face_distancePoint = self.face_distance(known_faces[results.index(True)],face_encoding)
                            print("Match Point : "+str((1 - face_distancePoint)* 100))
                            match_point_list.append(str((1 - face_distancePoint)* 100))
                            celalKayit.append((i))
                            face_list.append(("CelalSengor"))
                            face_ratio_list.append(FaceRatio)
                        if(match=="ali"):
                            face_distancePoint = self.face_distance(known_faces[results.index(True)],face_encoding)
                            print("Match Point : "+str((1 - face_distancePoint)* 100))
                            match_point_list.append(str((1 - face_distancePoint)* 100))
                            aliKayit.append((i))
                            face_list.append(("MehmetAliBirand"))
                            face_ratio_list.append(FaceRatio)
                        if(match=="besim"):
                            face_distancePoint = self.face_distance(known_faces[results.index(True)],face_encoding)
                            print("Match Point : "+str((1 - face_distancePoint)* 100))
                            match_point_list.append(str((1 - face_distancePoint)* 100))
                            besimKayit.append((i))
                            face_list.append(("BesimTibuk"))
                            face_ratio_list.append(FaceRatio)
                db_operations.DbInitiliazer(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
                db_operations.InsertDataToAnalyzePerFrame(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData1=face_list,RecievedData2=face_ratio_list,RecievedData3=match_point_list,videoId=videoId,frameNumber = i)
                i+=1

            db_operations.InsertDataToFaceNumberTable(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData=bilgiler,videoId=videoId)
            print("********Bilgiler**********")
            print("Celal Hoca Bilgileri :"+str((celalKayit))+" sn")
            print("Ali Bilgileri :"+str((aliKayit))+" sn")
            print("Besim Bilgileri :"+str((besimKayit))+" sn")
            print("Veritabanına Kaydediliyor.")
    def getVideoView(self):
        videoViewer = fd.faceViewer()
        videoViewer.main(videoLink=1)

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import numpy as np
import psycopg2
import db_operations


KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2



app = Flask(__name__)

isRead =False


known_faces = []
known_names = []

seen_faces = []



def VideoEkle(videoLink):
    video_conn=psycopg2.connect(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432)
    video_cur = video_conn.cursor()
    video_cur.execute("""CREATE TABLE IF NOT EXISTS videotable(
    id SERIAL PRIMARY KEY,
    videoLink VARCHAR(255)
    );""")

    video_conn.commit()

    video_cur.close()

    video_conn.close()

def videoCek(VideoId):
    video_conn=psycopg2.connect(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432)
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
    celalKayit =[]
    aliKayit =[]
    besimKayit=[]
    seen_faces=[]
    unkownPath = UNKNOWN_FACES_DIR+"/video"+str(Id)
    for name in os.listdir(unkownPath):
            image = face_recognition.load_image_file(f"{unkownPath}/{name}")
            image =cv2.imread(f"{unkownPath}/{name}")
            encoding = face_recognition.face_encodings(image)[0]
            print(encoding)
            seen_faces.append(encoding)
            


    print("*******************************")
    

    print("*******************************")

    print("bilinmeyen yüzlere bakiliyor...")
    print("*******************************")
    
    for i in range(80,len(os.listdir("data/video"+str(Id)))):
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
            results = face_recognition.compare_faces(seen_faces,face_encoding,TOLERANCE)
            
            match = None
            face_area =w * h
            
            FaceRatio = (((face_area) /(imageHeight * imageWidth))*100)
        
            if True in results:
                match = known_names[results.index(True)]
                print(known_names)
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
            print("acaseq")
            print("results : "+str(results))
        """ 
        db_operations.DbInitiliazer(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432)
        db_operations.InsertDataToAnalyzePerFrame(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,RecievedData1=face_list,RecievedData2=face_ratio_list,videoId=Id,frameNumber = i)


                    
                

    print("********Bilgiler**********")
    print("Celal Hoca Bilgileri :"+str((celalKayit))+" sn")
    print("Ali Bilgileri :"+str((aliKayit))+" sn")
    print("Besim Bilgileri :"+str((besimKayit))+" sn")
    print("Veritabanına Kaydediliyor.")
    db_operations.InsertDataToAnalyzeForPerson(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,person="CelalSengor",RecievedData=celalKayit,videoId=Id)
    db_operations.InsertDataToAnalyzeForPerson(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,person="MehmetAliBirand",RecievedData=aliKayit,videoId=Id)
    db_operations.InsertDataToAnalyzeForPerson(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,person="BesimTibuk",RecievedData=besimKayit,videoId=Id)
    print("kaydedildi.")"""


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
    db_operations.InsertDataToFaceNumberTable(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,RecievedData=bilgiler,videoId=videoId)
    print("*************************")
    print("!!! BİLGİLER !!!")
    for k in bilgiler:
        print("Saniye :"+str(k[0]))
        print("Kafa Sayısı :"+str(k[1]))


@app.route('/compare/<int:id>/<person>')
def CompareTime(person,id):
    conn=psycopg2.connect(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432)
    cursor =conn.cursor()
    cursor.execute(f"SELECT * FROM analyzeperframe WHERE id={id}")
    data = cursor.fetchall()
    firstFrame=data[0][1]  
    print("Data :"+str(data))
    if(data ==[]):
        return render_template("compareTime.html",person=person,BilgiDurumu=False)
    else:

        onlyPersonFrameList = db_operations.faceComparisonbyFrames(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,person=person)
        ratio_list = db_operations.GiveFaceRatio(host="localhost",dbname="cangerek",user="cangerek",password="3095",port=5432,RecievedData=onlyPersonFrameList,videoId=id)
        return render_template("compareTime.html",person=person,BilgiDurumu=True,onlyPersonFrameList=onlyPersonFrameList,ratio_list=ratio_list,VideoId=id,firstFrame=firstFrame)



@app.route('/show/videoId=<int:id>/frame=<int:frame>',methods=['GET','POST'])
def showFrame(id,frame):
    
        imgsrc="video"+str(id)+"/committed"+str(frame)+".png"
        print(imgsrc)
        return render_template("showFrame.html",imgsrc=imgsrc,frame=frame,id=id)

@app.route('/delete/videoId=<int:id>/frame=<int:frame>',methods=['GET','POST'])
def deleteFrame(id,frame):
    if(request.method=="POST"):
        db_operations.DeleteFrameWithIdentifier("localhost","cangerek","cangerek","3095",5432,id,frame)
        db_operations.DeleteDataFromFaceNumberTable("localhost","cangerek","cangerek","3095",5432,id,frame)
        return render_template('index.html')


@app.route('/info/videoId=<int:Id>')
def Goruntule(Id):
    data =db_operations.SelectAllFaceTableData("localhost","cangerek","cangerek","3095",5432,Id)
    print(data[0])
    transferredData=[]
    try:
        for bilgi in data:
            transferredData.append((bilgi[1],bilgi[2]))
            print("Aktarılıyor.")
    except Exception:
        print(Exception)

    if(transferredData ==[]):
        return render_template("info.html",entries=transferredData,BilgiDurumu = False,videoId=Id)
    else:
        return render_template("info.html",entries=transferredData, BilgiDurumu =True,videoId=Id)



@app.route('/commit/<int:Id>')
def home(Id):
    
    try:
        imgExtracter(Id)
        
    except Exception:
        pass
    print("Video'dan Fotolar Çekildi.")
    try:
        KafaSay(Id)
        KisiTanimla(Id)
    except Exception:
        pass
    print("Fotolara yüz taramasi yapildi.")
    

    return render_template('index.html')

@app.route('/')
def main():
    return 'Flask Opencv Face Recognation App'


if __name__ == '__main__':
    """#KisiTanimla()
    
    
    try:
        db_operations.DbInitiliazer("localhost","cangerek","cangerek","3095",5432)
    except Exception:
        print("hata")
    
    app.run()"""

    KisiTanimla(1)
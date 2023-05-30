from flask import Flask, render_template
import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import psycopg2


KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2


app = Flask(__name__)



known_faces = []
known_names = []

bilgiler = []
celalKayit =[]
aliKayit =[]
besimKayit=[]


def VideoEkle(videoLink):
    video_conn=psycopg2.connect(host ="localhost",dbname="flask_db",user="postgres",password="1",port=5432)
    video_cur = video_conn.cursor()
    video_cur.execute("""CREATE TABLE IF NOT EXISTS VideoTable(
    id SERIAL PRIMARY KEY,
    videoLink VARCHAR(255)
    );""")

    video_conn.commit()

    video_cur.close()

    video_conn.close()

def videoCek(VideoId):
    video_conn=psycopg2.connect(host ="localhost",dbname="flask_db",user="postgres",password="1",port=5432)
    video_cur = video_conn.cursor()
    sorgu = f"select * from VideoTable where id = {VideoId}"

    video_cur.execute(sorgu)
    cekilenVeri =video_cur.fetchall()
    VIDEO_URL = cekilenVeri[0][1]
    print("video URL : "+str(VIDEO_URL))
    video_conn.commit()

    video_cur.close()

    video_conn.close()
    return VIDEO_URL


def VeriKaydet(VideoId):
    conn =psycopg2.connect(host ="localhost",dbname="flask_db",user="postgres",password="1",port=5432)
    cur=conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS SaniyeBazliKayit(
    id PRIMARY KEY,
    saniye VARCHAR(255),
    kisiler VARCHAR(255)
    );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS kisibazlikayit(
    id PRIMARY KEY,
    kisi VARCHAR(255),
    BulunduguSaniyeler VARCHAR(255),
    TotalBulunmaSuresi VARCHAR(255)
    );""") 

    InsertString_kisi = f"""INSERT INTO kisibazlikayit(id,kisi, BulunduguSaniyeler, TotalBulunmaSuresi) VALUES
    ({VideoId},'Celal Şengör', '{str(celalKayit)}', '{str(len(celalKayit))}'),
    ({VideoId}'Mehmet Ali Birand', '{str(aliKayit)}', '{str(len(aliKayit))}'),
    ({VideoId}'Besim Tibuk', '{str(besimKayit)}', '{str(len(besimKayit))}')

"""

    

    cur.execute(InsertString_kisi)
    
    

    conn.commit()

    cur.close()

    conn.close()


def imgExtracter(Id):
    count = 0
    VIDEO_URL = videoCek(Id)
    if(VIDEO_URL !=""):
        print("Video : "+VIDEO_URL)
        vidcap = cv2.VideoCapture(VIDEO_URL)
        success,image = vidcap.read()
        success = True
        while success:
            vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
            success,image = vidcap.read()
            print ('Read a new frame: ', success)
            cv2.imwrite("data/frame%d.jpg" % count, image)    # save frame as JPEG file
            count = count + 1
    else:
        print("Veritabanında girilen Id de bir video yok")
    print("asdasd")

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
    
    for i in range(70,len(os.listdir("data"))):
        filename = f"frame{i}.jpg"
        print(filename)
        print("Dosya var mi :"+str(os.path.exists(f"data/{filename}")))
        image =cv2.imread(f"data/{filename}")
        locations = face_recognition.face_locations(image,2)
        encoding = face_recognition.face_encodings(image,locations)
        image =cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        for face_encoding, face_location in zip(encoding, locations):
            results = face_recognition.compare_faces(known_faces,face_encoding,TOLERANCE)
            match = None
        
            if True in results:
                match = known_names[results.index(True)]
                print(f"Match Found : {match}")
                if(match =="celal"):
                    celalKayit.append((i))
                if(match=="ali"):
                    aliKayit.append((i))
                if(match=="besim"):
                    besimKayit.append((i))
                
                    
                

    print("********Bilgiler**********")
    print("Celal Hoca Bilgileri :"+str((celalKayit))+" sn")
    print("Ali Bilgileri :"+str((aliKayit))+" sn")
    print("Besim Bilgileri :"+str((besimKayit))+" sn")
    print("Veritabanına Kaydediliyor.")
    VeriKaydet(Id)


def KafaSay():
    lst = os.listdir("data")
    print("cassda")
    numberFiles = len(lst)
    for i in range(numberFiles):
        image_path ='data/frame'+str(i)+'.jpg'
        img =cv2.imread(image_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        #print(f"Height of İmage : {img.shape[0]}\nWidth of Image:{img.shape[1]}\nArea of Image:{(img.shape[0] * img.shape[1])}")

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
            """print("***************")
            print(f"Height of İmage : {h}\nWidth of Image:{w}\nArea of Image:{(img.shape[0] * img.shape[1])}")"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        area = w * h      
        writedPath = "/home/can/Desktop/Calismalar/CanPython/Flask/deneme/static/committed"+str(i)+".png"
        cv2.imwrite(writedPath,img_rgb)
        bilgiler.append((i,len(faces)))
    print("*************************")
    print("!!! BİLGİLER !!!")
    for i in bilgiler:
        print("Saniye :"+str(i[0]))
        print("Kafa Sayısı :"+str(i[1]))


@app.route('/info')
def Goruntule():
    if(bilgiler ==[]):
        return render_template("info.html",entries=bilgiler,BilgiDurumu = False)
    else:
        return render_template("info.html",entries=bilgiler, BilgiDurumu =True)


@app.route('/info/detay')
def detayliInfo():
    return render_template("infoDetayli.html",celalKayit=celalKayit,aliKayit=aliKayit,besimKayit=besimKayit)

@app.route('/commit/<int:Id>')
def home(Id):
    
    try:
        imgExtracter(Id)
        print("Video'dan Fotolar Çekildi.")
        KafaSay()
        KisiTanimla(Id)
        
    except Exception:
        pass
    
    print("Fotolara yüz taramasi yapildi.")
    

    return render_template('index.html')



"""
@app.route('/Control/<String : fileName>')
def control(fileName):
    filePath = "data/"
    img = cv2.imread("data/")

    """

if __name__ == '__main__':
    #KisiTanimla()
    
    app.run()

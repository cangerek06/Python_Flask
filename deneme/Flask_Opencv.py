from flask import Flask, render_template
import matplotlib.pyplot as plt
import cv2
import face_recognition
import os


KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2


app = Flask(__name__)



known_faces = []
known_names = []

bilgiler = []
celalKayit =[]
aliKayit =[]
besimKayit=[]


def imgExtracter():
    
    count = 0
    vidcap = cv2.VideoCapture("celal.mp4")
    success,image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))    # added this line 
        success,image = vidcap.read()
        print ('Read a new frame: ', success)
        cv2.imwrite("data/frame%d.jpg" % count, image)    # save frame as JPEG file
        count = count + 1
    
    

def KisiTanimla():
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
    
    for i in range(len(os.listdir("data"))-88):
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


def KafaSay():
    lst = os.listdir("data")
    
    numberFiles = len(lst)
    for i in range(numberFiles):
        image_path ='data/frame'+str(i)+'.jpg'
        img =cv2.imread(image_path)
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
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

@app.route('/commit')
def home():
    try:
        imgExtracter()
        
    except Exception:
        pass
    print("Video'dan Fotolar Çekildi.")
    try:
        KafaSay()
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
    KisiTanimla()
    
    app.run()

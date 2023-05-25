from flask import Flask, render_template
import matplotlib.pyplot as plt
import cv2
import os


app = Flask(__name__)


bilgiler = []


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

       



def FaceInit():
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


@app.route('/commit')
def home():
    try:
        imgExtracter()
        
    except Exception:
        pass
    print("Video'dan Fotolar Çekildi.")
    try:
        FaceInit()
    except Exception:
        pass
    print("Fotolara yüz taraması yapıldı.")

    return render_template('index.html')



"""
@app.route('/Control/<String : fileName>')
def control(fileName):
    filePath = "data/"
    img = cv2.imread("data/")

    """

if __name__ == '__main__':
    app.run()
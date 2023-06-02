from flask import request,Flask, render_template
import os
import cv2


app = Flask(__name__)


def FaceApp(): 
    
    """ imgPath = 'face2.jpeg'  
    img = cv2.imread(imgPath)
    gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite('static/saved.png',img_rgb)
    return render_template('index.html')"""
    return "<h1>Giris Yapıldı.</h1>"

@app.route('/')
def login():
    error = None
    if(request.method =='POST'):
            return "<h1>Giris Yapıldı.</h1>"
    elif(request.method =='GET'):
        FaceApp()
        
        
        


if __name__ == '__main__':
     app.run()
     
    

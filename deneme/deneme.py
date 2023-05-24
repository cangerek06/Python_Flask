from flask import Flask, render_template
import matplotlib.pyplot as plt
import cv2


app = Flask(__name__)

image_path ='face2.jpeg'



def FaceApp():
    img =cv2.imread(image_path)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    for (x, y, w, h) in face:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("/home/can/Desktop/Calismalar/CanPython/Flask/deneme/static/saved.png",img_rgb)


@app.route('/')
def home():
    FaceApp()
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
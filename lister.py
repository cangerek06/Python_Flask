import os
import cv2


"""
lst = os.listdir("data/")
numberFiles =len(lst)
"""
bilgiler =[]







def fonk():
        
        img =cv2.imread("faces.jpg")
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(gray_image.shape)
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_classifier.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        print(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        writedPath = "/home/can/Desktop/Calismalar/CanPython/Flask/deneme/static/committed"
        cv2.imwrite("/home/can/Desktop/Calismalar/CanPython/Flask/deneme/static/saved.png",img_rgb)
        print(len(faces))


number = 0
print(os.path.exists("data"))

for name in os.listdir("data"):
      print(name)


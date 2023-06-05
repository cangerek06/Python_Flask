import cv2
import os

bilgiler = []


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
    print(bilgiler)



print(str(len(os.listdir("data"))))
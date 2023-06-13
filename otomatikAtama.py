import cv2
import face_recognition
import os
import numpy as np
import matplotlib
import psycopg2
from dotenv import load_dotenv, dotenv_values

load_dotenv()


def face_distance(face_encodings, face_to_compare):
        if len(face_encodings) == 0:
            return np.empty((0))
        face_dist_value = np.linalg.norm(face_encodings - face_to_compare, axis=0)
        print('[Face Services | face_distance] Distance between two faces is {}'.format(face_dist_value))
        return face_dist_value 


def deneme():
    videoURL = "videos/video1.mp4"
    Data = {}
    """
    Data = {1:{"encoding":"1.123 1.8734","SeenFrames":[1,2,5,12,15,23],"ratios":[0.78, 0.88, 0.87],"matchPoint":[]}}
    
    """
    
    videoCaptured =cv2.VideoCapture(videoURL)
    count = 0
    i = 0
    #savedFace_encodings =[] */*/*
    while True:
        videoCaptured.set(cv2.CAP_PROP_POS_MSEC,(count * 1000  / int(os.getenv("FRAMESPERSECOND"))))
        
        success, image = videoCaptured.read()
        
        try:
            image=cv2.resize(image,(0,0),fx=0.4,fy=0.4,interpolation=cv2.INTER_AREA)
        except Exception as e:
            break
    
        if success:
            imageWidth, imageHeight, imageChannel = image.shape
            img_area = imageWidth * imageHeight

            gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_classifier.detectMultiScale(gray_image,scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

            locations = face_recognition.face_locations(image,model="hog")
            face_encodings = face_recognition.face_encodings(image,locations)

            savedFace_encodings =[]

            savedNumber = 0 #silinecek diğer yorum satırına kadar
            print(len(Data))
            if len(Data)>0:
                #savedFaceIndex : {1:{.....}} => 1 =savedFaceIndex
                #for loop gets that number in every turn 1,2,3,4
                for savedFaceIndex in Data:
                    print("eklenmiş : "+str(Data[savedFaceIndex]["encodings"]))
                    savedFace_encodings.append(Data[savedFaceIndex]["encodings"])
                    savedNumber +=1

            #savedNumber = len(savedFace_encodings) */*/*

            for face_encoding,(x,y,w,h) in zip(face_encodings, faces):
                

                results = face_recognition.compare_faces(savedFace_encodings,face_encoding,tolerance=0.6)
                print("************")
                print("frame : "+str(count)+"encoding : "+str((face_encoding)))
                print("************")

                matching = None
                print("results : "+str(results))
                if(True in results):
                    #savedNumber = len(savedFace_encodings) */*/*
                    print("eşleşme bulundu.")
                    matching = Data[results.index(True)]["encodings"]
                    print(f"Match Found : face{matching}")
                    face_distancePoint = face_distance(matching,face_encoding)
                    Data[results.index(True)]["frames"].append(count)
                    Data[results.index(True)]["matchPoints"].append(1 - face_distancePoint)
                    Data[results.index(True)]["ratioPoints"].append((((w * h) / img_area ) * 100))

                else:
                    #savedNumber = len(savedFace_encodings) */*/*
                    print("Person's encoding does not exists in list.")
                    #savedFace_encodings.append(face_encoding)

                    Data[savedNumber]={}
                    Data[savedNumber]["encodings"]=face_encoding

                    print(Data[savedNumber]["encodings"])
                    
                    Data[savedNumber]["frames"]=[]
                    Data[savedNumber]["frames"].append(count)
                    
                    Data[savedNumber]["matchPoints"]=[]
                    Data[savedNumber]["matchPoints"].append(1.0)
                    
                    Data[savedNumber]["ratioPoints"]=[]
                    Data[savedNumber]["ratioPoints"].append((((w * h) / img_area ) * 100))

                    print("Added frame : "+str(count))
                    


        count +=1
    
    print("**************ANALİZ SONUÇLARI**************")
    print(Data)
    print("********************************************")


if __name__=="__main__":
    deneme()
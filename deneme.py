import face_recognition
import os
import numpy as np
import cv2

KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
#VIDEO_URL =""
FONT_THICKNESS = 2

isRead =False

known_faces = []
known_names = []

#yazılıma önceden verilen fotolardaki yüzlerin encdo edilmesi ve isimlerinin atanması
for name in os.listdir(KNOWN_FACES_DIR):
    for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        image =cv2.imread(f"{KNOWN_FACES_DIR}/{name}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        print(encoding)
        known_faces.append(encoding)
        known_names.append(name)



# Load a test image and get encondings for it
image_to_test = face_recognition.load_image_file("known_faces/ali/ali.png")
image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]






def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))
    face_dist_value = np.linalg.norm(face_encodings - face_to_compare, axis=1)
    print('[Face Services | face_distance] Distance between two faces is {}'.format(face_dist_value))
    return face_dist_value 

print(len(face_distance(known_faces,image_to_test_encoding)))

for i,k in zip(face_distance(known_faces,image_to_test_encoding),range(0,len(face_distance(known_faces,image_to_test_encoding)))):
    if (i < 0.6):
        print("person matched by : %"+str((1 - i )* 100))
        print("Person : "+str(known_names[k]))
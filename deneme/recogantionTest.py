import cv2 
import os
import face_recognition

KNOWN_FACES_DIR ="known_faces"
UNKNOWN_FACES_DIR="data"
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2

print("Bilinen Yüzler yükleniyor...")

known_faces = []
known_names = []


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
for filename in os.listdir(UNKNOWN_FACES_DIR):
    print(filename)
    print("Dosya var mi :"+str(os.path.exists(f"unknown_faces/{filename}")))
    image =cv2.imread(f"unknown_faces/{filename}")
    locations = face_recognition.face_locations(image,2)
    encoding = face_recognition.face_encodings(image,locations)
    image =cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    for face_encoding, face_location in zip(encoding, locations):
        results = face_recognition.compare_faces(known_faces,face_encoding,TOLERANCE)
        match = None
        
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match Found : {match}")
            """
            top_left = (face_location[3],face_location[0])
            bottom_right = (face_location[1],face_location[2])
            color =[0,255,0]
            cv2.rectangle(image,top_left,bottom_right,color,FRAME_THICKNESS)

            top_left = (face_location[3],face_location[2])
            bottom_right = (face_location[1],face_location[2]+22)

            cv2.rectangle(image,top_left,bottom_right,color,cv2.FILLED)
            cv2.putText(image,match, (face_location[3]+10,face_location[2]+15),cv2.FONT_HERSHEY_COMPLEX,0.5,(200,200,200),FONT_THICKNESS)
            cv2.imshow(match,image)
            cv2.waitKey(10000)
            """

#cv2.destroyAllWindows(filename)

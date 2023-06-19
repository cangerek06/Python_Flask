from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import numpy as np
import json
import ast
import psycopg2
import db_operations
import autoDetect

from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)


@app.route('/listAnalyzes',methods=['GET','POST'])
def listAnalyzes():
    if request.method=='GET':
        try:
            db_operations.ListAllAnalyzes()

        except Exception as e:
            return e



#düzenlendi
@app.route('/GetVideoUrl',methods=['GET','POST'])
def getVideoUrl():
    if request.method=='GET':
        try:
            jsonData = request.get_json()
            video_token = jsonData["video_token"]
            video_url=db_operations.getVideoSource(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),video_token=video_token)
            return f"Video Source Link : {video_url}"
            
        except Exception as e:
            return str(e)
#düzenlendi
@app.route('/info', methods =['GET','POST'])
def Goruntule():

    if request.method=="GET":
        try:
            jsonData = request.get_json()
            video_token = jsonData['video_token']
            returnedData = db_operations.SelectAllAnalysis(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),video_token=video_token)
            return returnedData
        except Exception as e:
            return "Hata : "+str(e)
        


#düzenlendi.
@app.route('/commit',methods=['POST'])
def home():
    if(request.method=="POST"):
       try:
        data = request.get_json()
        video_token= str(data["video_token"])
        autoDetect.face_detect(videoToken=video_token)
        return "video başarıyla işlendi."
       except Exception as e:
            return "Bir hata oldu : "+str(e)


#düzenlendi
@app.route('/') 
def main():
    return 'Flask Opencv Face Recognation App'



if __name__ == '__main__':
    try:
        db_operations.DbInitiliazer(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"))
    except Exception:
        print("hata")
    
    app.run()

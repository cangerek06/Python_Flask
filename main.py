from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import cv2
import face_recognition
import os
import numpy as np
import json
import psycopg2

import db_operations
import functions as functions

from dotenv import load_dotenv, dotenv_values

load_dotenv()

app = Flask(__name__)

@app.route('/compare',methods = ['GET','POST'])
def CompareTime():
    if request.method =="GET":
        try :
            data =request.get_json()
            videoId = data["videoId"]
            person = data["person"]

            conn=psycopg2.connect(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"))
            cursor =conn.cursor()
            cursor.execute(f"SELECT * FROM analyzeperframe WHERE id={videoId} ORDER BY frame ASC")
            data = cursor.fetchall()            
            if(data ==[]):
                return "Seçilen Videonun veritabanında kaydı yok."
            else:
                firstFrame=data[0][1]  
                print("Data :"+str(data))
                onlyPersonFrameList = db_operations.faceComparisonbyFrames(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),person=person,videoId=videoId)
                ratio_list = db_operations.GiveFaceRatio(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),RecievedData=onlyPersonFrameList,videoId=videoId)
                returnedData = {"data":[]}
                for i in range(0,len(onlyPersonFrameList)):
                    dataDict ={}
                    dataDict["frames"]     = str(onlyPersonFrameList[i])
                    dataDict["person"]     = person
                    dataDict["videoId"]    = videoId
                    dataDict["ratio"]      = ratio_list[i]
                    dataDict["identifier"] = str(videoId) + str(i)
                    returnedData["data"].append(dataDict)
                return returnedData
                


        except Exception as e:
            return str(e) 
        
@app.route('/show',methods=['GET'])
def showFrame():
    if request.method =="GET":
        try:
            data =request.get_json()  
            videoId=data["videoId"]
            frame = data["frame"]
            dbData = db_operations.SelectPerSecondAnalysisWithFrame(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),videoId,frame)
            returnedData = {"data":[]}
            dataDict ={}
            dataDict["videoId"]   =   dbData[0][0]
            dataDict["frame"]     =   dbData[0][1]
            dataDict["people"]    =   dbData[0][2]
            dataDict["ratio"]     =   dbData[0][3]
            dataDict["identifier"]=   dbData[0][4]

            returnedData["data"].append(dataDict)
            return returnedData
        
        except Exception as e:
            return "2"
            

@app.route('/delete',methods=['POST'])
def deleteFrame():
    if(request.method=="POST"):
        data= request.get_json()
        try:
            id = data["videoId"]
            frame = data["frame"]
            db_operations.DeleteFrameWithIdentifier(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),id,frame)
            db_operations.DeleteDataFromFaceNumberTable(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),id,frame)
            return "Frame silindi"
        except:
            return "videoId veya frame eksik girilmiş"
        

@app.route('/info', methods =['GET','POST'])
def Goruntule():

    if request.method=="GET":
        jsonData = request.get_json()
        try:
            videoId = jsonData['videoId']
        except Exception:
            return "Video Id girmeyi unuttunuz."
        dbData =db_operations.SelectAllFaceTableData(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),videoId)
        #returnData is a Dictionary
        returnData ={"data":[]}
        try:
            for i in range(0,len(dbData)):
                data ={}
                data["frame"]=str(dbData[i][1])
                data["Number of Faces"]=str(dbData[i][2])
                returnData["data"].append(data)
            
        except Exception:
            print(Exception)

        if(returnData ==[]):
            return "Video İşleme Sokulmamış."
        else:
            return returnData

@app.route('/commit',methods=['POST'])
def home():
    if(request.method=="POST"):
       try:
        data = request.get_json()
        videoId= int(data["videoId"])
        functions.allCalculations(videoId=videoId)
        return "video başarıyla işlendi."
       except Exception as e:
            return "Bir hata oldu : "+str(e)


@app.route('/')
def main():
    return 'Flask Opencv Face Recognation App'


@app.route('/getFrameView',methods = ['GET','POST'])
def getFrameVİew():
    if request.method=='GET':
        try:
            data = request.get_json()
            frameNo = data["frameNo"]
            videoId = data["videoId"]
            functions.getFrameView(videoId=videoId,frameNo=frameNo)
            return "asdasd"
        except Exception as e:
            return "Hata oluştu :"+str(e)



if __name__ == '__main__':
    try:
        db_operations.DbInitiliazer(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"))
    except Exception:
        print("hata")
    
    app.run()



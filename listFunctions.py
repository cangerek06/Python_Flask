import matplotlib.pyplot as plt
import os
import numpy as np
import ast

import db_operations
import faceFunctions as faceFunctions

from dotenv import load_dotenv, dotenv_values

load_dotenv()


def showAll(videoId):
    
    data = db_operations.SelectAllFrameDatas(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),videoId=videoId)
    returnedData ={"data":[]}
    if(len(data)==0):
        return "Video bilgileri Veritabanında Bulunmuyor."
    for i in range (0,len(data)):
        dataDict={}
        dataDictPeople={"PersonInfo":[]}
        dataDict["videoId"] = data[i][0]
        dataDict["frame"] = data[i][1]
        dataDict["identifier"] = data[i][4]
        peopleList = ast.literal_eval(data[i][2])
        ratioList = ast.literal_eval(data[i][3])
        if(len(peopleList) > 1):
            for i,k in zip(peopleList, ratioList):
                DataPeopleDict ={}
                DataPeopleDict["person"] = i
                DataPeopleDict["ratio"] = k
                dataDictPeople["PersonInfo"].append(DataPeopleDict)
        dataDict["peopleInfo"] = dataDictPeople
        returnedData["data"].append(dataDict)
    return returnedData


def getInfo(videoId):
        dbData =db_operations.SelectAllFaceTableData(os.getenv("HOST"),os.getenv("DBNAME"),os.getenv("MYUSER"),os.getenv("PASSWORD"),os.getenv("PORT"),videoId)
        #returnData is a Dictionary
        returnData ={"data":[]}
        if(len(dbData)!=0):
            for i in range(0,len(dbData)):
                data ={}
                data["frame"]=str(dbData[i][1])
                data["Number of Faces"]=str(dbData[i][2])
                returnData["data"].append(data)
            return returnData
        else:
             return "Video işleme sokulmamış"

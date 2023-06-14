import psycopg2
import json
import numpy as np
import os
from dotenv import load_dotenv, dotenv_values
import ast

load_dotenv()

def DbInitiliazer(host,dbname,user,password,port):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()


    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analysis_of_videos(
    faceid INTEGER,
    video_token VARCHAR(50),
    encoding VARCHAR(5500),
    seen_frames VARCHAR(2550),
    ratio_points VARCHAR(2550),
    match_points VARCHAR(2550),
    person_name VARCHAR(255),
    identifier VARCHAR(255)UNIQUE
    );"""


    
    #executing db table
    cursor.execute(QueryString_AnalyzePerFrame)
    conn.commit()
    
    cursor.close()
    conn.close()



    



def SelectVideoTableDatasWithId(host,dbname,user,password,port,videoId):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    DataQuery =f"select * from videotable where frame = {videoId}" 
    cursor.execute(DataQuery)
    Data = cursor.fetchall()
    if(len(Data)==0):
        print(f"Database Does Not Have Any Information At Id ={videoId}")
    else:

        VİDEO_URL = Data[0][1]

    conn.commit()

    cursor.close()
    conn.close()

    return VİDEO_URL



def SelectAllFrameDatas(host,dbname,user,password,port,videoId):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    
    DataQuery =f"SELECT * FROM analyzeperframe WHERE faceid={videoId} ORDER BY frame ASC"
    cursor.execute(DataQuery)
    data = cursor.fetchall()
    print(data)
    return data


def SelectPerSecondAnalysisWithFrame(host,dbname,user,password,port,id,frame):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    
    DataQuery =f"select * from analyzeperframe where frame = {frame} AND id={id} ORDER BY frame ASC" 
    cursor.execute(DataQuery)
    Data = cursor.fetchall()
    if(len(Data)==0):
        print(f"Database Does Not Have Any Information At Frame ={frame}")
        conn.commit()
        cursor.close()
        conn.close()
        return []
    
    conn.commit()

    cursor.close()
    conn.close()
    return Data

def InsertDataToFaceNumberTable(host,dbname,user,password,port,RecievedData,videoId):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    for data in RecievedData:
        InsertQuery =f"""INSERT INTO analyzeforfacenumber (id, frame,facenumber, identifier) VALUES ({videoId},{int(data[0])},{int(data[1])},{str(str(videoId)+str(data[0]))}) ON CONFLICT (identifier) DO NOTHING ;"""
        cursor.execute(InsertQuery)
        conn.commit()
    cursor.close()
    conn.close()

def DeleteDataFromFaceNumberTable(host,dbname,user,password,port,videoId,frame):         
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    DeleteQuery=f"DELETE FROM analyzeforfacenumber WHERE id={int(videoId)} and frame={int(frame)}"
    cursor.execute(DeleteQuery)
    conn.commit()
    cursor.close()
    conn.close()



def InsertDataToAnalyzePerFrame(host,dbname,user,password,port,RecievedData1,RecievedData2,RecievedData3,videoId,frameNumber):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    print("**********")
    print("func : InsertDataToAnalyzePerFrame Çalışıyor.")
    print("type RecievedData1: "+str(RecievedData1))
    print("length RecievedData1"+str(len(RecievedData1)))

    print("type RecievedData2: "+str(RecievedData2))
    print("length RecievedData2: "+str(len(RecievedData2)))

    if(len(RecievedData1) > 0):

        cursor.execute("INSERT INTO analyzeperframe(id,frame,people,ratio,matchpoint,identifier)VALUES(%s,%s,%s,%s,%s,%s) ON CONFLICT (identifier) DO NOTHING",(videoId, frameNumber,str(RecievedData1),str(RecievedData2),str(RecievedData3),str(str(videoId)+str(frameNumber))))
    
    conn.commit()
    cursor.close()
    conn.close()


def DeleteFrameWithIdentifier(host,dbname,user,password,port,id,frame):
        conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
        cursor =conn.cursor()
        identifier = str(str(id)+str(frame))
        DeleteQuery =f"DELETE FROM analyzeperframe WHERE frame ={frame} AND id ={id}"  
        cursor.execute(DeleteQuery)
        
        conn.commit()
        cursor.close()
        conn.close()
        
def GiveMatchPoint(host,dbname,user,password,port,RecievedData,videoId):
    conn =psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor =conn.cursor()
    matchPointList = []
    for i in RecievedData:
        DataQuery = f"SELECT * FROM analyzeperframe WHERE frame ={i} AND id={videoId}"
        cursor.execute(DataQuery)
        data = cursor.fetchall()
        matchPointList.append(str(data[4]))
        conn.commit()
    cursor.close()
    conn.close()
    return matchPointList

def GiveFaceRatio(host,dbname,user,password,port,RecievedData,videoId):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    ratioList = []
    for i in RecievedData:
        DataQuery = f"SELECT * FROM analyzeperframe WHERE frame ={i} AND id ={videoId}"
        cursor.execute(DataQuery)
        data = cursor.fetchall()
        print("**********^^^^^^************")
        print(data[0][3])
        print("**********^^^^^^************")
        ratioList.append(str(data[0][3]))
    cursor.close()
    conn.close()
    return ratioList

def faceComparisonbyFrames(host,dbname,user,password,port,person,videoId):
    conn =psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    DataQuery = f"SELECT * FROM analyzeperframe WHERE id={videoId} ORDER BY frame ASC"
    cursor.execute(DataQuery)
    Data = (cursor.fetchall())
    print("Data : "+str(Data))
    print("*************")
    print("Data type : "+str(type(Data)))
    print("*************")
    onlyPersonFrameList=[]
    personFrameList =[]
    
    
    for i in range(len(Data)):
        liste =list(ast.literal_eval(Data[i][2]))
        print("type of liste: "+str(type(liste)))
        print("*************")
        print("liste :"+str(liste))
        print("*************")
       
        print("liste :"+str(len(liste)))
        print("*************")
        if(person in liste):
            print("person Frame de bulunuyor.")
            print("*************")
            personFrameList.append(Data[i][1])
            deletePersonFromListToCompare = liste.remove(str(person))
            if(len(liste)==0):
                onlyPersonFrameList.append(Data[i][1])
        else:
            pass
        
    
    print("************")
    print("Person Where He Stays Alone At Frames :"+str(onlyPersonFrameList))
    print("Total Time That Stays Alone At Video :"+str(len(onlyPersonFrameList)))
    return onlyPersonFrameList

def getVideoSource(host,dbname,user,password,port,videoToken):
    conn =psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursour = conn.cursor()

    QueryStirng = f"SELECT * FROM files_media WHERE friendly_token='{(videoToken)}'"

    cursour.execute(QueryStirng)
    data =cursour.fetchall()
    if len(data) !=0:
        mediaSource = data[0][16]
        return mediaSource
    else:
        return "Girilen Token'a ait Video yok."


    
def InsertToAnalyzeTable(host,dbname,user,password,port,faceId,encoding,seen_frames,match_points,ratio_points,videoToken,identifier):
    conn = psycopg2.connect(host = host,dbname = dbname,user=user,password=password,port=port)
    cursor = conn.cursor()

    QueryString = "INSERT INTO analysis_of_videos(faceid, encoding, seen_frames, ratio_points, match_points, video_token, identifier)VALUES(%s, %s, %s, %s, %s, %s, %s)ON CONFLICT (identifier) DO NOTHING"
    cursor.execute(QueryString,(faceId,encoding,seen_frames,ratio_points,match_points,videoToken,identifier))

    conn.commit()
    cursor.close()
    conn.close()

def SelectAllAnalysis(host,dbname,user,password,port, video_token):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    
    Query_string = f"SELECT * FROM analysis_of_videos WHERE video_token='{(video_token)}'"
    cursor.execute(Query_string)
    
    
    datas = cursor.fetchall()
    print("data : "+str(len(datas)))
    returnedData = {"Datas":[]}
    for data in datas:
        print("544545454545454")
        print(data[1])
        dataDict = {}
        dataDict["faceid"] = data[0]
        dataDict["video_token"] = data[1]
        dataDict["encoding"] = data[2] #bunu vermeye gerek yok
        """dataDict["seen_frames"] = data[3]
        dataDict["ratio_points"] = data[4]
        dataDict["match_points"] = data[5]"""
        dataDict["name"] = data[6]
        dataDict["identifier"] = data[7]
        
        print("Data type of seen_frames : "+str(type(data[3])))
        print("Data type of ratio_points : "+str(type(data[4])))
        print("Data type of match_points : "+str(type(data[5])))

        seen_frames_list = data[3][1:-1]
        ratio_points_list = data[4][1:-1]
        match_points_list = data[5][1:-1]

        seen_frames_list2 = list(seen_frames_list.split(","))
        ratio_points_list2= list(ratio_points_list.split(","))
        match_points_list2 = list(match_points_list.split(","))

        print("işelm yapıldı.")

        print("Data type of seen_frames : "+str(type(seen_frames_list2)))
        print("Data type of ratio_points : "+str(type(ratio_points_list2)))
        print("Data type of match_points : "+str(type(match_points_list2)))
        

        print("Data type of seen_frames : "+str((seen_frames_list2)))
        print("Data type of ratio_points : "+str((ratio_points_list2)))
        print("Data type of match_points : "+str((match_points_list2)))
        DataDictList={"ListDatas":[]}
        for k,l,m in zip(seen_frames_list2,ratio_points_list2,match_points_list2):
            DataDictList2={}
            DataDictList2["seen_frame"]=k
            DataDictList2["ratio_point"]=l
            DataDictList2["match_point"]=m

            DataDictList["ListDatas"].append(DataDictList2)
    

        dataDict["List"]=DataDictList
        returnedData["Datas"].append(dataDict)
    
    return returnedData




    cursor.close()
    conn.close()
    return data

if __name__=='__main__':

    """DbInitiliazer("localhost","cangerek","cangerek","3095",port=5432)
    Data = {1:{
        "encoding":"encoding_verisi",
        "seen_frames":[1, 2, 3, 4],
        "ratio_points":[1.22, 1.23, 1.22, 2.11],
        "match_points":[11.22, 23.11, 11.22, 23.11],
        "video_token":["K123CKOPS"],
        "identifier":["1K123CKOPS"]

        }}
    faceId=2
    encoding = Data[1]["encoding"]
    seen_frames = Data[1]["seen_frames"]
    ratio_points = Data[1]["ratio_points"]
    match_points = Data[1]["match_points"]
    videoToken =Data[1]["video_token"]
    identifier =Data[1]["identifier"]

    print(Data[1]['encoding'])

    InsertToAnalyzeTable("localhost","cangerek","cangerek","3095",5432,faceId,encoding,seen_frames,match_points,ratio_points,videoToken,identifier)


    QueryString_AnalyzePerFrame = CREATE TABLE IF NOT EXISTS analysis_of_videos(
    faceid INTEGER,
    videoToken VARCHAR(255)
    encoding VARCHAR(5500),
    seen_frames VARCHAR(255),
    ratio_points VARCHAR(255),
    match_points VARCHAR(255),
    person_name VARCHAR(255),
    identifier VARCHAR(255)UNIQUE
    );

    """

    SelectAllAnalysis(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),video_token="JlboqHKra")
    #InsertToAnalyzeTable(host=os.getenv("HOST"),dbname=os.getenv("DBNAME"),user=os.getenv("MYUSER"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),faceId=1212,videoToken="asd",encoding="1231",seen_frames="123123",ratio_points="123123",identifier="1231",match_points="1231")
import psycopg2
import json
import numpy as np
import ast


def DbInitiliazer(host,dbname,user,password,port):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()


    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analysis_of_videos(
    faceid INTEGER UNIQUE,
    encoding VARCHAR(255),
    seen_frames VARCHAR(255),
    ratio_points VARCHAR(255),
    match_points VARCHAR(255),
    person_name VARCHAR(255)
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

    
def InsertToAnalyzeTable(host,dbname,user,password,port,faceId,encoding,seen_frames,match_points,ratio_points):
    conn = psycopg2.connect(host = host,dbname = dbname,user=user,password=password,port=port)
    cursor = conn.cursor()

    QueryString = "INSERT INTO analysis_of_videos(faceid, encoding, seen_frames, ratio_points, match_points)VALUES(%s, %s, %s, %s, %s)ON CONFLICT (faceid) DO NOTHING"
    cursor.execute(QueryString,(faceId,encoding,seen_frames,match_points,ratio_points))

    conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':

    DbInitiliazer("localhost","cangerek","cangerek","3095",port=5432)
    Data = {1:{
        "encoding":"encoding_verisi",
        "seen_frames":[1, 2, 3, 4],
        "ratio_points":[1.22, 1.23, 1.22, 2.11],
        "match_points":[11.22, 23.11, 11.22, 23.11]

        }}
    faceId=2
    encoding = Data[1]["encoding"]
    seen_frames = Data[1]["seen_frames"]
    ratio_points = Data[1]["ratio_points"]
    match_points = Data[1]["match_points"]

    print(Data[1]['encoding'])

    InsertToAnalyzeTable("localhost","cangerek","cangerek","3095",5432,faceId,encoding,seen_frames,match_points,ratio_points)


    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analysis_of_videos(
    faceid INTEGER UNIQUE,
    encoding VARCHAR(5500),
    seen_frames VARCHAR(255),
    ratio_points VARCHAR(255),
    match_points VARCHAR(255),
    person_name VARCHAR(255)
    );"""


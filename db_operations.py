import psycopg2
import json
import numpy as np
import ast


def DbInitiliazer(host,dbname,user,password,port):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    QueryString_VideoTable = """CREATE TABLE IF NOT EXISTS videotable(
        id INTEGER,
        videolink VARCHAR(255)

    );"""
    
    QueryString_AnalyzeForFaceNumber = """CREATE TABLE IF NOT EXISTS analyzeforfacenumber(
        id INTEGER,
        frame INTEGER,
        facenumber INTEGER,
        identifier VARCHAR(255) UNIQUE    
    );"""

    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analyzeperframe(
    id INTEGER,
    frame INTEGER,
    people VARCHAR(255),
    ratio VARCHAR(255),
    identifier VARCHAR(255) UNIQUE
    );"""

    QueryString_AnalyzeForPerson= """CREATE TABLE IF NOT EXISTS analyzeforperson(
    id INTEGER,
    person VARCHAR(255),
    totaltime VARCHAR(255)
    );"""
    
    #executing db tables
    cursor.execute(QueryString_VideoTable)
    conn.commit()
    cursor.execute(QueryString_AnalyzePerFrame)
    conn.commit()
    cursor.execute(QueryString_AnalyzeForPerson)
    conn.commit()
    cursor.execute(QueryString_AnalyzeForFaceNumber)
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

def SelectAllFaceTableData(host,dbname,user,password,port,videoId):
    conn = psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    
    DataQuery =f"select * from analyzeforfacenumber WHERE id={int(videoId)} ORDER BY frame ASC ;"
    cursor.execute(DataQuery)

    data = cursor.fetchall()
    print("$$$$$$$$$$$$$$$$$$$")
    print("FaceTable Data : "+str(data))
    print("$$$$$$$$$$$$$$$$$$$")
    return data
#cas
def SelectPerSecondAnalysisWithFrame(host,dbname,user,password,port,frame):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    
    DataQuery =f"select * from analyzeperframe where frame = {frame}" 
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





def InsertDataToVideoTable(host,dbname,user,password,port,RecievedData):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    InsertQuery = f"""INSERT INTO videotable (id, videolink) VALUES ({RecievedData[0]}, {RecievedData[1]}) ;"""
    cursor.execute(InsertQuery)

    conn.commit()
    cursor.close()
    conn.close()


def InsertDataToAnalyzePerFrame(host,dbname,user,password,port,RecievedData1,RecievedData2,videoId,frameNumber):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    print("**********")
    print("func : InsertDataToAnalyzePerFrame Çalışıyor.")
    print("type RecievedData1: "+str(RecievedData1))
    print("length RecievedData1"+str(len(RecievedData1)))

    print("type RecievedData2: "+str(RecievedData2))
    print("length RecievedData2: "+str(len(RecievedData2)))

    if(len(RecievedData1) > 0):

        cursor.execute("INSERT INTO analyzeperframe(id,frame,people,ratio,identifier)VALUES(%s,%s,%s,%s,%s) ON CONFLICT (identifier) DO NOTHING",(videoId, frameNumber,str(RecievedData1),str(RecievedData2),str(str(videoId)+str(frameNumber))))
    
    conn.commit()
    cursor.close()
    conn.close()

def InsertDataToAnalyzeForPerson(host,dbname,user,password,port,RecievedData,person,videoId):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO analyzeforperson(id,person,totaltime)VALUES(%s,%s,%s)",(videoId, person, len(RecievedData)))
    print("kayit edildi")

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

def faceComparisonbyFrames(host,dbname,user,password,port,person):
    conn =psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    DataQuery = "SELECT * FROM analyzeperframe"
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


if __name__=='__main__':
    DbInitiliazer("localhost","flask_db","postgres","1",5432)
    #InsertDataToAnalyzeForPerson('localhost',"flask_db","postgres","1",5432,[1,2],"celal",1)
    #InsertDataToAnalyzePerFrame("localhost","flask_db","postgres","1",5432,[("mehmet"),("celal"),("besim")],1,23)
    #faceComparisonbyFrames("localhost","flask_db","postgres","1",5432,"CelalSengor")
    GiveFaceRatio("localhost","flask_db","postgres","1",5432,[86,87,88,89,90],1)

    print("***************")

    
import psycopg2
import json
import ast


def DbInitiliazer(host,dbname,user,password,port):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    QueryString_VideoTable = """CREATE TABLE IF NOT EXISTS videotable(
        id INTEGER,
        videolink VARCHAR(255)

    );"""
    
    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analyzeperframe(
    id INTEGER,
    frame INTEGER PRIMARY KEY ,
    people VARCHAR(255),
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

def InsertDataToVideoTable(host,dbname,user,password,port,RecievedData):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    InsertQuery = f"""INSERT INTO videotable (id, videolink) VALUES ({RecievedData[0]}, {RecievedData[1]}) ;"""
    cursor.execute(InsertQuery)

    conn.commit()
    cursor.close()
    conn.close()


def InsertDataToAnalyzePerFrame(host,dbname,user,password,port,RecievedData,videoId,frameNumber):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO analyzeperframe(id,frame,people,identifier)VALUES(%s,%s,%s,%s) ON CONFLICT (identifier) DO NOTHING",(videoId, frameNumber,str(RecievedData),str(str(videoId)+str(frameNumber))))

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

def faceComparisonbyFrames(host,dbname,user,password,port,person):
    conn =psycopg2.connect(host=host,dbname=dbname,user=user,password=password,port=port)
    cursor = conn.cursor()
    DataQuery = "SELECT * FROM analyzeperframe"
    cursor.execute(DataQuery)
    Data = (cursor.fetchall())
    print("Data : "+str(Data))
    min=Data[0][1]
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
            personFrameList.append(i+min)
            deletePersonFromListToCompare = liste.remove(str(person))
            if(len(liste)==0):
                onlyPersonFrameList.append(i+min)
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
    faceComparisonbyFrames("localhost","flask_db","postgres","1",5432,"Celal Şengör")

    print("***************")

    

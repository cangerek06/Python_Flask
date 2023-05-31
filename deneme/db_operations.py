import psycopg2


def DbInitiliazer(host,dbname,user,password,port):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    QueryString_VideoTable = """CREATE TABLE IF NOT EXISTS videotable(
        id INTEGER PRIMARY KEY,
        videolink VARCHAR(255)

    );"""
    
    QueryString_AnalyzePerFrame = """CREATE TABLE IF NOT EXISTS analyzeperframe(
    id INTEGER PRIMARY KEY,
    frame VARCHAR(255),
    people VARCHAR(255)
    );"""

    QueryString_AnalyzeForPerson= """CREATE TABLE IF NOT EXISTS analyzeforperson(
    id INTEGER PRIMARY KEY,
    person VARCHAR(255),
    secondsinvideo VARCHAR(255),
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

    InsertQuery = f"""INSERT INTO videotable (id, videolink) VALUES ({RecievedData[0]}, {RecievedData[1]});"""
    cursor.execute(InsertQuery)

    conn.commit()
    cursor.close()
    conn.close()


def InsertDataToAnalyzePerFrame(host,dbname,user,password,port,RecievedData):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    InsertQuery = f"""INSERT INTO analyzeperframe (id, frame, people) VALUES ({RecievedData[0]}, {RecievedData[1],RecievedData[2]});"""
    cursor.execute(InsertQuery)

    conn.commit()
    cursor.close()
    conn.close()

def InsertDataToAnalyzeForPerson(host,dbname,user,password,port,RecievedData):
    conn = psycopg2.connect(host = host,dbname=dbname,user =user,password=password,port=port)
    cursor = conn.cursor()

    InsertQuery = f"""INSERT INTO analyzeforperson (id, person, secondsinvideo, totaltime) VALUES ({RecievedData[0]}, {RecievedData[1],RecievedData[2]}, {RecievedData[3]});"""
    cursor.execute(InsertQuery)

    conn.commit()
    cursor.close()
    conn.close()




if __name__=='__main__':

    DbInitiliazer('localhost',"flask_db","postgres","1",5432)
    print("can")

    

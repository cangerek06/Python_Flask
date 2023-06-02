import psycopg2

conn = psycopg2.connect(host="localhost",dbname="flask_db",user="postgres",password="1",port=5432)



cur =conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS person(
    id INT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    gender CHAR
);""")

cur.execute("""INSERT INTO person(id, name, age, gender) VALUES
    (1, 'Can', 22, 'm'),
    (2, 'Sevval', 21, 'f'),
    (3, 'Fatih', 22, 'm')

""")

conn.commit()


cur.close()

conn.close()
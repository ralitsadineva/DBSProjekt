import psycopg2

db = "election"
username = "postgres"
passwort = "ENTER YOUR PASSWORD"
host_ = "localhost"
port_ = "5432"
conn = psycopg2.connect(database = db, user = username, password = passwort, host = host_, port = port_)
print("Opened database successfully")

cur = conn.cursor()

def get_data():
    cur.execute("SELECT t1.time FROM enthaelt h1 JOIN tweet t1 on h1.tid = t1.id")
    file = open("data_diagramm.txt", "w")
    data = cur.fetchall()
    for i in data:
        file.write(str(i[0]) + "\n")
    file.close()
 
get_data()

conn.commit()
cur.close()
conn.close()
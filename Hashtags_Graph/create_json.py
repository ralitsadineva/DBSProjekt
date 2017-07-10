import json
import psycopg2
import math

db = "election"
username = "postgres"
passwort = "ENTER YOUR PASSWORD"
host_ = "localhost"
port_ = "5432"
conn = psycopg2.connect(database = db, user = username, password = passwort, host = host_, port = port_)
print("Opened database successfully")

cur = conn.cursor()

def get_data_nodes():
    cur.execute("SELECT * FROM hashtag")
    nodes = []
    data = cur.fetchall()
    for i in data:
        nodes.append(i[0])
    return nodes

def get_data_edges():
    cur.execute("SELECT h1.hname, h2.hname FROM enthaelt h1 JOIN enthaelt h2 on h1.tid = h2.tid WHERE h1.hname != h2.hname")
    edges = []
    data = cur.fetchall()
    for i in data:
        edges.append(i)
    return edges

data_nodes = get_data_nodes()
data_edges = get_data_edges()

conn.commit()
cur.close()
conn.close()

data_n = []
n = 0
for i in data_nodes:
    data = {
        "id": "n" + str(n),
        "label": i,
        "x": math.cos(math.pi * 2 * n / len(data_nodes)),
        "y": math.sin(math.pi * 2 * n / len(data_nodes)),
        "size": 1
    }
    data_n.append(data)
    n += 1

data_e = []
e = 0
source_n = ""
target_n = ""
for i in data_edges:
    for item in data_n:
        if item["label"] == i[0]:
            source_n = item["id"]
        if item["label"] == i[1]:
            target_n = item["id"]
    data = {
        "id": "e" + str(e),
        "source": source_n,
        "target": target_n
    }
    data_e.append(data)
    e += 1

data = {
    "nodes": data_n,
    "edges": data_e
}

with open('data.json', 'w') as f:
     json.dump(data, f)


import json
import math
from clustering import *

clusters = clustering(hashtags)

data_n = []
n = 0
k = 0
l = 0
for cluster in clusters:
    k += 1
    l = 0
    for hashtag in cluster:
        data = {
            "id": "n" + str(n),
            "label": hashtag,
            "x": math.cos(math.pi * 2 * l / len(cluster)) + k * 5,
            "y": math.sin(math.pi * 2 * l / len(cluster)),
            "size": 1
        }
        data_n.append(data)
        n += 1
        l += 1

data_e = []
e = 0
source_n = ""
target_n = ""
for cluster in clusters:
    for i in range(len(cluster)):
        for item in data_n:
            if item["label"] == cluster[i]:
                source_n = item["id"]
            if i == len(cluster) - 1:
                if item["label"] == cluster[0]:
                    target_n = item["id"]
            else:
                if item["label"] == cluster[i+1]:
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

with open('data_sim.json', 'w') as f:
     json.dump(data, f)


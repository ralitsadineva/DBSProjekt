import psycopg2
import random

db = "election"
username = "postgres"
passwort = "ENTER YOUR PASSWORD"
host_ = "localhost"
port_ = "5432"
conn = psycopg2.connect(database = db, user = username, password = passwort, host = host_, port = port_)
print("Opened database successfully")

cur = conn.cursor()

def hashtags_list():
    cur.execute("SELECT * FROM hashtag")
    hashtags = []
    data = cur.fetchall()
    for i in data:
        hashtags.append(i[0])
    return hashtags

hashtags = hashtags_list()

conn.commit()
cur.close()
conn.close()

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

distance_table = [[0 for _ in range(len(hashtags))] for _ in range(len(hashtags))]
index_dict = dict()

def init_table():
    for i in range(len(hashtags)):
        index_dict[hashtags[i]] = i
        for j in range(len(hashtags)):
            distance_table[i][j] = levenshtein(hashtags[i], hashtags[j])

def initialize_centers(k):
    hashtags_copy = hashtags[:]
    random.shuffle(hashtags_copy)
    centers = hashtags_copy[0:k]
    return centers

def get_distance(h1, h2):
    index1 = index_dict[h1]
    index2 = index_dict[h2]
    return distance_table[index1][index2]
 
def find_closest_center(h_tag, centers):
    center = min(centers, key=lambda c: get_distance(h_tag, c))
    return centers.index(center)

def assign_hashtags_to_clusters(hashtags, centers):
    clusters = [[] for _ in range(len(centers))]
    for h_tag in hashtags:
        c = find_closest_center(h_tag, centers)
        clusters[c].append(h_tag)
    return clusters

def find_cost(clusters, centers):
    sum_total = 0
    for index, cluster in enumerate(clusters):
        sum_cluster = 0
        center = centers[index]
        for element in cluster:
            sum_cluster += get_distance(center, element)
        sum_total += sum_cluster
    return sum_total

def clustering(hashtags):
    init_table()
    k = int(input("Enter value for k: "))
    centers = initialize_centers(k)
    clusters = assign_hashtags_to_clusters(hashtags, centers)
    cost = find_cost(clusters, centers)
    center_index = 0
    centers_set = set(centers)
    while center_index < k:
        for hashtag in hashtags:
            cost_new = 0
            if hashtag not in centers_set:
                centers_new = centers[:]
                centers_new[center_index] = hashtag
                clusters_new = assign_hashtags_to_clusters(hashtags, centers_new)
                cost_new = find_cost(clusters_new, centers_new)
                if cost_new < cost:
                    centers = centers_new
                    clusters = clusters_new
                    cost = cost_new
                    centers_set = set(centers)
        center_index += 1
    return clusters

if __name__ == "__main__":
    clusters = clustering(hashtags)
    for i in range(len(clusters)):
        print("Cluster " + str(i) + ": " + str(clusters[i]))
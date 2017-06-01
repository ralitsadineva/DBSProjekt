import psycopg2
from read_and_correct import *

db = "election"
username = "postgres"
passwort = "ENTER YOUR PASSWORD"
host_ = "localhost"
port_ = "5432"
conn = psycopg2.connect(database = db, user = username, password = passwort, host = host_, port = port_)
print("Opened database successfully")

cur = conn.cursor()

def populate_tweets():
    print("Populating tweets...")
    for row in read_file:
        link = extract_links(row['text'])
        if link != []:
            url = link 
        else:
            url = row['source_url']
        cur.execute('INSERT INTO TWEET (Text, Time, Favourite, Retweet_count, Link) VALUES (%s, %s, %s, %s, %s)', (row['text'], format_timestamp(row['time']), row['favorite_count'], row['retweet_count'], url))
    print("Finished populating tweets!")
    
def populate_hashtags():
    print("Populating hashtags...")
    hashtags = get_all_hashtags(read_file)
    for hashtag in hashtags:
        if len(hashtag) > 0:
            cur.execute("INSERT INTO HASHTAG VALUES (%s)", (hashtag, ))
    print("Finished populating hashtags!")
            
            
def populate_autor():
    print("Populating autor...")
    authors = set()
    for row in read_file:
        authors.add(row['handle'])
    
    for author in authors:
        cur.execute("INSERT INTO AUTOR VALUES(%s)", (author, ))
    print("Finished populating autor!")
        
def populate_von():
    print("Populating von...")
    cur.execute("SELECT * FROM TWEET")
    rows = cur.fetchall()
    for row in rows:
        id = row[0]
        text = row[1]
        time = row[2]
        favourite = row[3]
        retweet_count = row[4]
        for row_file in read_file:
            if text == row_file['text'] and str(time) == row_file['time'].replace("T", " ") and favourite == int(row_file['favorite_count']) and retweet_count == int(row_file['retweet_count']):
                if row_file['is_retweet'] == 'True':
                    og =  row_file['original_author']
                else:
                    og = row_file['handle']
                cur.execute("INSERT INTO VON VALUES(%s, %s, %s)", (id, row_file['handle'], og))
                break
    print("Finished populating von!")
                
def populate_enthaelt():
    print("Populating enthaelt...")
    cur.execute("SELECT * FROM TWEET")
    rows_tweet = cur.fetchall()
    cur.execute("SELECT * FROM HASHTAG")
    rows_hashtag = cur.fetchall()
    for r_tweet in rows_tweet:
        id = r_tweet[0]
        text = r_tweet[1]
        for r_hash in rows_hashtag:
            if "#" + r_hash[0] in text.replace("# ", "#"):
                cur.execute("INSERT INTO ENTHAELT VALUES(%s, %s)", (id, r_hash))
    print("Finished populating enthaelt!")


populate_hashtags()
populate_autor()
populate_tweets()
populate_von()
populate_enthaelt()
conn.commit()
cur.close()
conn.close()
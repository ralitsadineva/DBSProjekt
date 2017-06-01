import csv
csvfile = open('american-election-tweets.csv')
creader = csv.DictReader(csvfile, delimiter=';')

read_file = [row for row in creader]
    
def extract_hash_tags(s):
    s = s.replace("# ", "#")
    return set(part[1:] for part in s.split() if part.startswith('#'))
    
def get_all_hashtags(creader):
    hashtags = set()
    for row in creader:
        hashtags.update(extract_hash_tags(row['text']))
    return hashtags
    
def format_timestamp(timestamp):
    return timestamp.replace("T", " ")
    
def extract_links(text):
    links = [part for part in text.split() if part.startswith('https')]
    if links == []:
        return []
    return links[len(links) - 1]
    
        


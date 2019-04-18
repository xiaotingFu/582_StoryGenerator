import json
import sys
from urllib.request import urlopen
from summa.summarizer import summarize
from google.cloud import storage
import hashlib
import six
from Helper.DBHelper import DBHelper
import re
from collections import defaultdict
# Google Cloud Setting
PROJECT_ID = 'mongodb-236418'
CLOUD_STORAGE_BUCKET = 'generated_fiction'


def parsename(s):
    return " ".join(re.findall("[a-zA-Z]+", s))


def _get_storage_client():
    return storage.Client(
        project=PROJECT_ID)


def upload_file(file_stream, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    client = _get_storage_client()
    bucket = client.bucket(CLOUD_STORAGE_BUCKET)
    blob = bucket.blob(filename)
    stats = storage.Blob(bucket=bucket, name=filename).exists(client)
    if not stats:
        print("Upload story to cloud.")
        blob.upload_from_string(
            file_stream,
            content_type=content_type)
    else:
        print("File already in cloud storage")
    url = blob.public_url
    print(url)
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')
    return url


# import spacy
# from spacy import displacy
# from collections import Counter
# nlp = spacy.load("en_core_web_sm")

def get_book_pairs():
    """
    select story from database make sure all combinition has more than three titles

    get the book combinition that has the most stories

    return a list of books    
    """
    import sqlite3
    conn = sqlite3.connect('../db/db.sqlite3')
    
    sql = "select book1, book2, count(*) from Story group by book1, book2 HAVING count(*)> 10 ORDER BY count(*);"
    cursor = conn.execute(sql)
    # build a graph for book pairs
    bookpairs = defaultdict(list)
    for row in cursor:
        bookpairs[row[0]].append(bookpairs[row[1]])
        bookpairs[row[1]].append(bookpairs[row[0]])
    print(bookpairs)
    # search in the graph and delete the pair that are not fully-connected


def readStory():
    with open('../db/tmp.json') as json_file:
        data = json.load(json_file)
        url_list = data['urls']
        book1 = data['book1']
        book2 = data['book2']
    return url_list, book1, book2


def generate_summary(url_list):
    story_content_list = []
    story_summary_list = []
    character_list = []
    for url in url_list:
        data = urlopen(url)
        story_content_list.append(data.read().decode('utf-8'))

    for story in story_content_list:
        summary = summarize(story, words=100)
        story_summary_list.append(summary)

    summary_string = ". ".join(story_summary_list)
    f = open('input.txt', 'w+')
    f.write(summary_string)
    f.close()


def clean_summary():
    out_file = '../db/output.txt'
    in_file = 'input.txt'
    completed_lines_hash = set()

    o_file = open(out_file, 'w')
    story_content = ""
    for line in open(in_file, 'r'):
        hash_value = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()

        if hash_value not in completed_lines_hash:
            o_file.write(line)
            story_content += line
            completed_lines_hash.add(hash_value)
    o_file.close()
    return story_content


def uploadDB(book1, book2, story_content):
    file_tile = parsename(book1) + "_" + parsename(book2)
    url = upload_file(story_content, file_tile, 'text/plain')
    db = DBHelper(parsename(book1), parsename(book2))
    db.url = url
    db.insertSummary()


def main():
    # 1. read story from nodejs output
    url_list, book1, book2 = readStory()
    # 2. generate summary
    generate_summary(url_list)
    # 3. clean summary
    story_content = clean_summary()
    print(story_content)
    # 4. upload file to google cloud and save record to sqlite db
    uploadDB(book1, book2, story_content)


if __name__ == "__main__":
    # main()
    get_book_pairs()

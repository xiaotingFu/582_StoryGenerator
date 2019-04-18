import json
import sys
from urllib.request import urlopen
from summa.summarizer import summarize
from google.cloud import storage
import hashlib
import six
from Helper.DBHelper import DBHelper
import re
import sqlite3
import time
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


def get_book_url(book1, book2):
    conn = sqlite3.connect('../db/db.sqlite3')

    sql = "select url from Story where book1 ='{b1}' AND book2 = '{b2}';".format(b1=book1, b2=book2)
    cursor = conn.execute(sql)
    urls = []
    for row in cursor:
        urls.append(row[0])
    return urls

def get_book_pairs():
    """
    select story from database make sure all combinition has more than three titles

    get the book combinition that has the most stories

    return a list of books    
    """
    import collections
    conn = sqlite3.connect('../db/db.sqlite3')
    sql = "select book1, book2, count(*) from Story group by book1, book2 HAVING count(*)> 10 ORDER BY count(*) DESC;"
    cursor = conn.execute(sql)
    # build a graph for book pairs
    # bookpairs = collections.defaultdict(list)
    print("Top 10 books")
    count = 100
    books= []
    for row in cursor:
        if count > 0:
            book1, book2, occ = row[0], row[1], str(row[2])
            # print(book1 + " : " + book2 + " appears " + occ + " times")
            pair = [book1, book2] 
            books.append(pair)
        count -= 1
    # print(books)
    # print(len(books))

    conn.close()
    return books


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
    print("=====================")
    print("Start generator")
    pairs = get_book_pairs()
    total_time = time.time()
    for book1, book2 in pairs:
        if book1 == "Harry Potter" and book2 == "Percy Jackson and the Olympians":
            continue
        if DBHelper(book1, book2).isRecordExistSummary():
            continue
        start_time = time.time()
        print("Generating for books " + book1 + " and " + book2)
        # 1. read book url
        url_list = get_book_url(book1, book2)
        # 2. generate summary
        generate_summary(url_list)
        # 3. clean summary
        story_content = clean_summary()
        print(story_content)
        # 4. upload file to google cloud and save record to sqlite db
        uploadDB(book1, book2, story_content)
        elapsed_time = time.time() - start_time
        print("Done in {s} ms.".format(s=elapsed_time))
    total_elasped = time.time() - total_time
    print("Finsh generation for " + len(pairs) + " book pairs;")
    print("Total done in {s} ms.".format(s=total_elasped))
if __name__ == "__main__":
    # main()
    main()

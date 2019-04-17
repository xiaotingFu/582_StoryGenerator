import json
from urllib.request import urlopen
from summa.summarizer import summarize
import hashlib

# import spacy
# from spacy import displacy
# from collections import Counter
# nlp = spacy.load("en_core_web_sm")

with open('../db/tmp.json') as json_file:
    data = json.load(json_file)
    url_list = data['urls']

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
# article = nlp(summary_string)

# for x in article.ents:
#     if x.label_ == "PERSON":
#         character_list.append(x)

# print(character_list)
# print(Counter(character_list).most_common(5))

f = open('input.txt', 'w+')
f.write(summary_string)
f.close()

out_file = '../db/output.txt'
in_file = 'input.txt'

completed_lines_hash = set()

o_file = open(out_file, 'w')

for line in open(in_file, 'r'):
    hash_value = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()

    if hash_value not in completed_lines_hash:
        o_file.write(line)
        completed_lines_hash.add(hash_value)

o_file.close()


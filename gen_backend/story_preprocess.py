import json
from urllib.request import urlopen
from summa.summarizer import summarize

with open('../db/tmp.json') as json_file:
    data = json.load(json_file)
    url_list = data['urls']

story_content_list = []
story_summary_list = []

for url in url_list:
    print(url)
    data = urlopen(url)
    story_content_list.append(data.read().decode('utf-8'))

for story in story_content_list:
    summary = summarize(story, words=50)
    story_summary_list.append(summary)

summary_string = ". ".join(story_summary_list)

f = open('input.txt', 'w+')
f.write(summary_string)
f.close()



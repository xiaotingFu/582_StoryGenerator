# import urllib.request
import json
import sys
# def generator(stories):
#     """
#     input: dictionary, book content
#     rtype: generated story
#     """
#     new_story = ""
#     count = 1
#     for title in stories:
#         new_story += str(count) + title + "\n"
#         count += 1
#     return new_story
#read json file
d = {}
with open('../db/tmp.json') as json_file:
    d = json.load(json_file)
print(d)
sys.stdout.flush()
    # stories = {}
    # # print(d)
    # for title in d:
    #     url = d[title]
    #     # print(title, url)
    #     story_content = ""
    #     for line in urllib.request.urlopen(url):
    #         story_content += str(line)
    #     stories[title] = story_content

    # # use machine learning to generate story
    # new_story= generator(stories)


import os
import codecs
import requests
from bs4 import BeautifulSoup
import json
from google.cloud import firestore


# Project ID is determined by the GCLOUD_PROJECT environment variable

# Inistalize firestore client
db = firestore.Client()

counter = 1
site_path = "https://www.fanfiction.net"
book_list_page = requests.get(site_path + "/crossovers/book/")
soup = BeautifulSoup(book_list_page.content, 'html.parser')


book_columns = soup.find_all('td', valign='TOP')
for first_book_column in book_columns:
    book_records = first_book_column.find_all('div')
    for first_book in book_records:
        first_book_path = site_path + str(first_book.find('a')['href'])

        second_book_list_page = requests.get(first_book_path)
        soup2 = BeautifulSoup(second_book_list_page.content, 'html.parser')

        second_book_columns = soup2.find_all('td', valign='TOP')
        for column in second_book_columns:
            second_book_records = column.find_all('div')
            for second_book in second_book_records:
                second_book_path = site_path + str(second_book.find('a')['href'])

                crossover_result_page = requests.get(second_book_path)
                soup3 = BeautifulSoup(crossover_result_page.content, 'html.parser')

                books_header = soup3.find('div', id='content_wrapper_inner')
                book_names = books_header.find_all('a')
                if book_names:
                    book1 = book_names[0].text.replace(' ', ' ')
                    book2 = book_names[1].text.replace(' ', ' ')
                    print(book1, book2)
                    crossover_category = book_names[0].text.replace(' ', '_') + "_and_" + book_names[1].text.replace(' ', '_')

                    # new_directory_path = '../data/' + crossover_category

                    # try:
                    #     os.mkdir(new_directory_path)
                    # except OSError:
                    #     print("Creation of the directory %s failed" % new_directory_path)
                    #
                    #     break
                    # else:
                    #     print("Successfully created the directory %s " % new_directory_path)
                    print("Crawling category%s " % crossover_category)
                    list_of_stories = soup3.find_all('div', class_='z-list')
                    for story in list_of_stories:

                        story_link = story.find('a', class_='stitle')['href']
                        story_url = site_path + story_link

                        story_page = requests.get(story_url)
                        soup4 = BeautifulSoup(story_page.content, 'html.parser')
                        story_title = story_url.split('/')[-1:][0]
                        if len(story_title) <= 100:
                            print("- Crawling story %s" % story_title)
                            story_text = ""
                            # story_path = new_directory_path + '/' + story_title + ".txt"

                            if soup4.find('select', id='chap_select'):
                                chapters = soup4.find('select', id='chap_select').find_all('option')
                                for chapter in chapters:
                                    chapter_index = chapter['value']
                                    story_link_broken = story_link.split('/')
                                    story_link_broken[-2] = chapter_index
                                    story_link = "/".join(story_link_broken)

                                    story_page = requests.get(site_path + story_link)
                                    soup4 = BeautifulSoup(story_page.content, 'html.parser')

                                    story_page = soup4.find('div', id='storytext')

                                    paragraph = story_page.find_all('p')
                                    story_page = ' '.join(item.text for item in paragraph)
                                    story_text += story_page
                                    # # json record
                                    # record = {
                                    #     story_title[0]:  str(story_text)
                                    # }
                                    # extracted_crossovers.append(record)
                            else:
                                story_page = soup4.find('div', id='storytext')
                                paragraph = story_page.find_all('p')
                                story_page = ' '.join(item.text for item in paragraph)
                                story_text += story_page

                            # insert a record into the firebase db
                            story_data = {
                                u"title":  u'{}'.format(story_title),
                                u"book1": u'{}'.format(book_names[0]),
                                u"book2": u'{}'.format(book_names[1]),
                                u"content": u'{}'.format(story_text)
                            }
                            c = db.collection(u'fictions')
                            d = c.document(u'crossovers')
                            d.collection(u'{}'.format(crossover_category)).document(u'{}'.format(story_title)).set(story_data)

                            # with open(story_path, 'a+', encoding='utf-8') as f:
                            #     f.write(story_text)



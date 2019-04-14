import requests
from bs4 import BeautifulSoup
from google.cloud import storage
from langdetect import detect
import six
from Helper.DBHelper import DBHelper


import re
def parsename(s):
    return " ".join(re.findall("[a-zA-Z]+", s))

PROJECT_ID = 'mongodb-236418'
CLOUD_STORAGE_BUCKET = 'fiction_db2'
def _get_storage_client():
    return storage.Client(
        project=PROJECT_ID)

# Inistalize google cloud client

# [START upload_file]
def upload_file(file_stream, foldername, filename, content_type):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """

    client = _get_storage_client()
    bucket = client.bucket(CLOUD_STORAGE_BUCKET)
    print('{}/'.format(foldername) + filename)
    blob = bucket.blob('{}/'.format(foldername) + filename)
    filepath = '{}/'.format(foldername)
    stats = storage.Blob(bucket=bucket, name=filepath).exists(client)
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
                    print("Crawling category %s " % crossover_category)
                    list_of_stories = soup3.find_all('div', class_='z-list')
                    for story in list_of_stories:

                        story_link = story.find('a', class_='stitle')['href']
                        story_url = site_path + story_link

                        story_page = requests.get(story_url)
                        soup4 = BeautifulSoup(story_page.content, 'html.parser')
                        story_title = story_url.split('/')[-1:][0]
                        title_type = ""
                        try:
                            title_type = detect(story_title)
                        except:
                            print("langdetect.lang_detect_exception.LangDetectException: No features in text.")
                            pass

                        if title_type == 'en' and len(story_title) <= 100:
                                db = DBHelper(parsename(book1), parsename(book2), parsename(story_title))
                                if not db.isRecordExist():
                                    print("- Crawling story %s" % story_title)
                                    story_text = ""
                                    # story_path = new_directory_path + '/' + story_title + ".txt"
                                    try:
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
                                                if paragraph:
                                                    story_page = ' '.join(item.text for item in paragraph)
                                                else:
                                                    story_page = str(story_page)
                                                story_text += story_page

                                        else:
                                            story_page = soup4.find('div', id='storytext')
                                            paragraph = story_page.find_all('p')
                                            if paragraph:
                                                story_page = ' '.join(item.text for item in paragraph)
                                            else:
                                                story_page = str(story_page)
                                            story_text += story_page

                                        if len(story_text) > 0:
                                            lang = detect(story_text)
                                        else:
                                            lang = 'null'

                                        if lang == 'en' and len(story_text) > 0:
                                            try:
                                                # upload file to google cloud and retrive its url
                                                url = upload_file(story_text,crossover_category, story_title,'text/plain')
                                                # update the url to database
                                                db.url = url
                                                db.insert()
                                            except:
                                                print("[ERROR] Upload to Google Cloud and Database")
                                                pass
                                    except:
                                        print("[ERROR] Unable to find chapter")
                                        pass
                        else:
                            print("[Error] Story not in english")


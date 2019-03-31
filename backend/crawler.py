import os
import requests
from bs4 import BeautifulSoup

counter = 1

site_path = "https://www.fanfiction.net"
book_list_page = requests.get(site_path + "/crossovers/book/")
soup = BeautifulSoup(book_list_page.content, 'html.parser')

book_columns = soup.find_all('td', valign='TOP')
for column in book_columns:
    book_records = column.find_all('div')
    for book in book_records:
        first_book_path = site_path + str(book.find('a')['href'])

        second_book_list_page = requests.get(first_book_path)
        soup2 = BeautifulSoup(second_book_list_page.content, 'html.parser')

        second_book_columns = soup2.find_all('td', valign='TOP')
        for column in second_book_columns:
            second_book_records = column.find_all('div')
            for book in second_book_records:
                second_book_path = site_path + str(book.find('a')['href'])

                crossover_result_page = requests.get(second_book_path)
                soup3 = BeautifulSoup(crossover_result_page.content, 'html.parser')

                books_header = soup3.find('div', id='content_wrapper_inner')
                book_names = books_header.find_all('a')

                new_directory_path = book_names[0].text.replace(' ', '_') + "_" + book_names[1].text.replace(' ', '_')

                try:
                    os.mkdir(new_directory_path)
                except OSError:
                    print("Creation of the directory %s failed" % new_directory_path)
                else:
                    print("Successfully created the directory %s " % new_directory_path)

                list_of_stories = soup3.find_all('div', class_='z-list')
                for story in list_of_stories:
                    story_link = story.find('a', class_='stitle')['href']
                    story_url = site_path + story_link


                    story_page = requests.get(story_url)
                    soup4 = BeautifulSoup(story_page.content, 'html.parser')

                    story_title = story_url.split('/')[-1:]
                    story_text = ""

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
                        
                        text_file = open(new_directory_path + '/' + story_title[0] + '.txt', 'w+', encoding='utf-8')
                        text_file.write(str(story_text))
                        text_file.close()

                    if counter == 1:
                        break

                if counter == 1:
                    break

            if counter == 1:
                break

        if counter == 1:
            break
    if counter == 1:
        break
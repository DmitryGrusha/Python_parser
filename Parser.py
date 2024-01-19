import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin, urlparse, parse_qs


def parse_page(url: str, page: int):
    response = requests.get(url)
    # status
    if response.status_code == 200:
        print("STATUS CODE == 200")
        soup = BeautifulSoup(response.text, 'html.parser')
        # properties
        author_links = soup.find('a', class_='styles_bookAuthor__MDwQE')
        book_title = soup.find('h1', class_='styles_bookTitle__g0OEg')

        file_path = author_links.getText() + " - " + book_title.get_text() + ".txt"

        book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Books')

        if not os.path.exists(book_folder_path):
            os.makedirs(book_folder_path)

        book_path = os.path.join(book_folder_path, file_path)

        if page == 1:
            # author_links = soup.find('a', class_='styles_bookAuthor__MDwQE')
            # book_title = soup.find('h1', class_='styles_bookTitle__g0OEg')
            # book_img = soup.find('img')
            # print('АВТОР:  ' + author_links.getText())
            # print('НАЗВАНИЕ:  ' + book_title.getText())
            # print('IMG:  ' + book_img.get('src'))
            # file_path = author_links.getText() + " - " + book_title.get_text() + ".txt"

            text = author_links.getText() + '\n' + book_title.get_text() + '\n'
            with open(book_path, "w", encoding="utf-8") as file:
                file.write(text)
            print("FILE CREATED")

        paragraphs = soup.find_all('p', class_='MsoNormal')
        for paragraph in paragraphs:
            text_between_tags = paragraph.get_text()
            with open(book_path, "a", encoding="utf-8") as file:
                file.write('\n' + text_between_tags)
                print("APPEND TEXT...")


        print("APPEND TEXT FINISHED")
        print("NEXT PAGE...")
        # if book_img:
        #     img_url = book_img.get('src')
        #     print(img_url)
        # img_response = requests.get(img_url)
        #
        # img_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Img')
        #
        # if not os.path.exists(img_folder_path):
        #     os.makedirs(img_folder_path)
        #
        # img_path = os.path.join(img_folder_path, '1.jpg')
        #
        # with open(img_path, 'wb') as f:
        #     f.write(response.content)
        # print('--------------------')
        # for paragraph in paragraphs:
        #     text_between_tags = paragraph.get_text()
        #     print(text_between_tags)
        return True
    else:
        return False


def run():
    print("START")
    base_url = 'https://foxbooks.ec/reader'
    ids = [126153]
    for id in ids:
        page = 1
        while True:
            print('PAGE ' + str(page) + ' - start parsing...')
            params = {'id': id, 'page': page}
            url_with_query = urljoin(base_url, '?' + urlencode(params))
            # parse
            result = parse_page(url=url_with_query, page=page)
            if result:
                page += 1
            else:
                break

    print("SUCCESS")


run()
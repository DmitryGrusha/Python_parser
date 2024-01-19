import requests
import os
import re
from bs4 import BeautifulSoup
from ID_Generator import generate_id


image_base_url = "https://readbookfreeonline.com/"
file_format = ".txt"
image_format = ".jpg"
files_directory = "English_Books"
images_directory = "Img"
page_path_component = "/page-"


def parse_by(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        book_id = generate_id()
        # author information
        author_result, author_name = get_author_name(soup)
        if author_result is False: return False
        # book title information
        book_title_result, book_title = get_book_name(soup)
        if book_title_result is False: return False
        # number of pages
        book_pages_count_result, book_pages_count = get_book_pages_count(soup)
        if book_pages_count_result is False: return False
        # load image
        load_image_result = get_and_load_image(soup, book_id)
        if load_image_result is False: return False
        # create txt file
        book_path = create_file(book_id=book_id, author_name=author_name, book_title=book_title)
        final_result = parse_all_pages(url=url, max_pages=book_pages_count, book_path=book_path)
        if final_result:
            return True
        else:
            return False
    else:
        print("INITIAL REQUEST ERROR")
        return False


# PARSE ALL PAGES
def parse_all_pages(url: str, max_pages: int, book_path):
    page_url = url + page_path_component
    current_page = 1
    while True:
        print("CURRENT PAGE - " + str(current_page) + "   |   " + "MAX PAGE - " + str(max_pages))
        result = get_text_from_page(url=page_url + str(current_page), book_path=book_path, page=current_page)
        if result:
            current_page += 1
        else:
            print("DONE")
            return True


# CREATE FILE FOR ALL DATA
def create_file(book_id: int, author_name: str, book_title: str):
    file_path = str(book_id) + file_format
    book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), files_directory)
    # create directory if not exist
    if not os.path.exists(book_folder_path):
        os.makedirs(book_folder_path)

    book_path = os.path.join(book_folder_path, file_path)
    author_and_book_title = author_name + '\n' + book_title + '\n'

    with open(book_path, "w", encoding="utf-8") as file:
        file.write(author_and_book_title)
        print("FILE CREATED - SUCCESS")
        return book_path


# LOAD IMAGE TO DIRECTORY
def get_and_load_image(soup, book_id: int) -> bool:
    img_tag = soup.find('div', class_='col-md-5').find('img')
    if img_tag:
        image_url = image_base_url + img_tag['src']
        get_book_image_request = requests.get(image_url)

        img_data = get_book_image_request.content
        image_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), images_directory)
        image_path = os.path.join(image_folder_path, str(book_id) + image_format)

        with open(image_path, 'wb') as file:
            file.write(img_data)
        print("LOAD IMAGE - SUCCESS")
        return True
    else:
        print("LOAD IMAGE - ERROR")
        return False



def get_genre(soup) -> (bool, str):
    genre_link = soup.find_all('div', class_='list-info')
    if genre_link:
        for div in genre_link:
            if 'Category:' in div.text:
                category_text = div.text.strip()
                print("GENRE - SUCCESS")
                return True, category_text
            # else:
            #     print("WRONG DIV")
            #     return False, ""
        return False, ""
    else:
        print("GENRE - ERROR")
        return False, ""

# GET STORYLINE
def get_storyline(soup) -> (bool, str):
    storyline_link = soup.find('div', class_='des-novel')
    if storyline_link:
        paragraphs = storyline_link.find_all('p')
        full_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        print("STORYLINE - SUCCESS")
        return True, full_text
    else:
        print("STORYLINE - ERROR")
        return False, ""



# GET AUTHOR NAME
def get_author_name(soup) -> (bool, str):
    author_link = soup.find('div', class_='list-info').find('a')
    if author_link:
        author_name = author_link.text.strip()
        print("AUTHOR NAME - SUCCESS")
        return True, author_name
    else:
        print("AUTHOR NAME - ERROR")
        return False, ""


# GET BOOK TITLE
def get_book_name(soup) -> (bool, str):
    book_title = soup.find('div', class_='col-sm-12').find('h1')
    if book_title:
        modified_book_title = re.sub(r'\([^)]*\)', '', book_title.get_text()).strip()
        print("BOOK NAME - SUCCESS")
        return True, modified_book_title
    else:
        print("BOOK NAME - ERROR")
        return False, ""


# GET BOOK PAGES COUNT
def get_book_pages_count(soup) -> (bool, int):
    total = soup.find('div', class_='title').find('h2')
    if total:
        total_pages = total.text.split('(')[-1].split(')')[0]
        print("NUMBER OF PAGES - SUCCESS")
        return True, total_pages
    else:
        print("NUMBER OF PAGES - ERROR")
        return False, 0


# PARSE ALL PARAGRAPHS ON 1 PAGE
def get_text_from_page(url: str, book_path, page: int):
    response = requests.get(url)
    if response.status_code == 200:
        print("REQUEST TO PAGE " + url + " - SUCCESS")
        soup = BeautifulSoup(response.text, 'lxml')
        paragraphs = soup.find_all('p')
        if paragraphs:
            for p in paragraphs:
                with open(book_path, 'a', encoding='utf-8') as file:
                    file.write("\n" + "\n" + p.getText())

            print("APPEND TEXT FINISHED - PAGE - " + str(page))
            return True
        else:
            print("PARAGRAPHS - ERROR")
            return False
    else:
        print("REQUEST TO PAGE " + url + " - ERROR")
        return False


# parse(url="https://readbookfreeonline.com/harry-potter-and-the-philosopher-s-stone-harry-potter-1")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-chamber-of-secrets-harry-potter-2")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-prisoner-of-azkaban-harry-potter-3")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-goblet-of-fire-harry-potter-4")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-order-of-the-phoenix-harry-potter-5")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-half-blood-prince-harry-potter-6")
# parse(url="https://readbookfreeonline.com/harry-potter-and-the-deathly-hallows-harry-potter-7")


# OLD!!!

# def parse(url: str):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'lxml')
#
#         book_id = generate_id()
#         max_pages = 0
#         current_page = 1
#         author_name = ''
#         # author
#         first_div_list_info = soup.find('div', class_='list-info')
#         if first_div_list_info:
#             author_link = first_div_list_info.find('a')
#             if author_link:
#                 author_name = author_link.text.strip()
#             else:
#                 print("Тег <a> внутри тега <div class='list-info'> не найден.")
#                 return
#         else:
#             print("Тег <div class='list-info'> не найден.")
#             return
#         # book title
#         book_title = soup.find('div', class_='col-sm-12').find('h1')
#         # total pages
#         total = soup.find('div', class_='title').find('h2')
#         if total:
#             total_pages = total.text.split('(')[-1].split(')')[0]
#             max_pages = total_pages
#         else:
#             print("Количество страниц неизвестно")
#             return
#
#         # book image
#         img_tag = soup.find('div', class_='col-md-5').find('img')
#         image_url = "https://readbookfreeonline.com/" + img_tag['src']
#         # load book image
#         get_book_image_request = requests.get(image_url)
#         img_data = get_book_image_request.content
#
#         image_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Img')
#         image_path = os.path.join(image_folder_path, str(book_id) + '.jpg')
#
#         with open(image_path, 'wb') as file:
#             file.write(img_data)
#
#         file_path = str(book_id) + ".txt"
#         book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'English_Books')
#         # create directory is not exist
#         if not os.path.exists(book_folder_path):
#             os.makedirs(book_folder_path)
#         book_path = os.path.join(book_folder_path, file_path)
#
#         # refactor book title
#         modified_book_title = re.sub(r'\([^)]*\)', '', book_title.get_text()).strip()
#         author_and_book_title = author_name + '\n' + modified_book_title + '\n'
#         with open(book_path, "w", encoding="utf-8") as file:
#             file.write(author_and_book_title)
#         print("FILE CREATED")
#         page_url = url + "/page-"
#         while True:
#             print("CURRENT PAGE - " + str(current_page))
#             print("MAX PAGE - " + str(max_pages))
#             print("START PARSING PAGE - " + str(current_page))
#             result = get_text_from_page(url=page_url + str(current_page), book_path=book_path, page=current_page)
#             if result:
#                 current_page += 1
#             else:
#                 print("DONE")
#                 return
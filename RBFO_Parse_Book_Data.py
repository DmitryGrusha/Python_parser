import requests
import os
import re
import json
from bs4 import BeautifulSoup
# from ID_Generator import *
import ID_Generator

from Genre import get_array_of_ids_by_name, Genre


image_base_url = "https://readbookfreeonline.com/"
file_format = ".txt"
json_file_format = ".json"
image_format = ".jpg"
# files_directory = "English_Books"
images_directory = "Img"
page_path_component = "/page-"
books_path = "Books/"


def parse_by(url: str, category: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        # book_id = generate_id()
        book_id = ID_Generator.create_new_id()
        print("Parse book info:")
        # author information
        author_result, author_name = get_author_name(soup)
        if author_result is False: return False
        # book title information
        book_title_result, book_title = get_book_name(soup)
        if book_title_result is False: return False
        # book storyline
        storyline_result, storyline = get_storyline(soup)
        if storyline_result is False: return False
        # genres
        genres_result, genres = get_genres(soup)
        if genres_result is False: return False
        # number of pages
        book_pages_count_result, book_pages_count = get_book_pages_count(soup)
        if book_pages_count_result is False: return False
        # load image
        load_image_result = get_and_load_image(soup, book_id)
        if load_image_result is False: return False
        # create txt file
        book_path = create_json_file(category=category, book_id=book_id, author_name=author_name, book_title=book_title, storyline=storyline, chapters_total_count=book_pages_count, genres=genres)
        # save new id to file
        ID_Generator.save_new_id(new_id=book_id)
        print("❕ Book parsing has started - " + book_title)
        # return parse_all_pages(url=url, max_pages=book_pages_count, book_path=book_path)
        parse_book_result = parse_all_pages(url=url, max_pages=book_pages_count, book_path=book_path)
        if parse_book_result:
            print("✅ - " + book_title)
            return True
    else:
        print("🔴 Book page request.")
        return False


# PARSE ALL PAGES
def parse_all_pages(url: str, max_pages: int, book_path):
    page_url = url + page_path_component
    current_page = 1
    while True:
        if current_page > max_pages:
            return True
        print("Progress - " + str(int(float(current_page * 100) / float(max_pages))) + "%" )
        result = get_text_from_page_and_save_to_json(url=page_url + str(current_page), book_path=book_path, page=current_page, max_pages=max_pages)
        if result is False:
            print("🔴 Get text from book page.")
            return False
        current_page += 1


def create_json_file(category: str, book_id: int, author_name: str, book_title: str,storyline: str, chapters_total_count: int, genres):
    file_path = str(book_id) + json_file_format
    book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), books_path + category)
    # create directory if not exist
    if not os.path.exists(book_folder_path):
        os.makedirs(book_folder_path)

    book_path = os.path.join(book_folder_path, file_path)
    # prepare json data
    data = { "author": author_name,
             "title": book_title,
             "storyline": storyline,
             "chapters_total_count": chapters_total_count,
             "genres": genres,
             "chapters": []
             }

    with open(book_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
        print("🟢 Json file.")
        return book_path


# CREATE FILE FOR ALL DATA
# def create_file(book_id: int, author_name: str, book_title: str,storyline: str, genres: [int]):
#     file_path = str(book_id) + file_format
#     book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), files_directory)
#     # create directory if not exist
#     if not os.path.exists(book_folder_path):
#         os.makedirs(book_folder_path)
#
#     book_path = os.path.join(book_folder_path, file_path)
#     author_and_book_title = author_name + '\n' + book_title + '\n'
#
#     with open(book_path, "w", encoding="utf-8") as file:
#         file.write(author_and_book_title)
#         print("FILE CREATED - SUCCESS")
#         return book_path


# LOAD IMAGE TO DIRECTORY
def get_and_load_image(soup, book_id: int) -> bool:
    img_tag = soup.find('div', class_='col-md-5').find('img')
    if img_tag:
        image_url = image_base_url + img_tag['src']
        get_book_image_request = requests.get(image_url)

        img_data = get_book_image_request.content
        image_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), books_path + images_directory)
        # Create dir if not exist
        if not os.path.exists(image_folder_path):
            os.makedirs(image_folder_path)

        image_path = os.path.join(image_folder_path, str(book_id) + image_format)

        with open(image_path, 'wb') as file:
            file.write(img_data)
        print("🟢 Image.")
        return True
    else:
        print("🔴 Image.")
        return False


# GET GENRES
def get_genres(soup) -> (bool, [Genre]):
    genre_link = soup.find_all('div', class_='list-info')
    if genre_link:
        for div in genre_link:
            if 'Category: ' in div.text:
                category_text = div.text.strip()
                # remove text 'Category: ' and ' ,'
                clear_text = category_text.replace('Category: ', '').rstrip(', ')
                # split to array str values
                str_array = clear_text.split(' ,')
                # remove spaces in genres
                modified_strings = [s.replace(" ", "") for s in str_array]
                print("🟢 Genres.")
                return True, get_array_of_ids_by_name(modified_strings)
        return False, ""
    else:
        print("🔴 Genres.")
        return False, ""

# GET STORYLINE
def get_storyline(soup) -> (bool, str):
    storyline_link = soup.find('div', class_='des-novel')
    if storyline_link:
        paragraphs = storyline_link.find_all('p')
        full_text = '\n\n'.join(paragraph.get_text(strip=True) for paragraph in paragraphs)
        # split and remove if 1 line contain #()
        lines = full_text.split('\n')
        filtered_lines = [line.strip() for line in lines if not ("#" in line and "(" in line and ")" in line)]
        result_text = '\n'.join(filtered_lines).strip()
        print("🟢 Storyline.")
        return True, result_text
    else:
        print("🔴 Storyline.")
        return False, ""



# GET AUTHOR NAME
def get_author_name(soup) -> (bool, str):
    author_link = soup.find('div', class_='list-info').find('a')
    if author_link:
        author_name = author_link.text.strip()
        print("🟢 Author.")
        return True, author_name
    else:
        print("🔴 Author.")
        return False, ""


# GET BOOK TITLE
def get_book_name(soup) -> (bool, str):
    book_title = soup.find('div', class_='col-sm-12').find('h1')
    if book_title:
        modified_book_title = re.sub(r'\([^)]*\)', '', book_title.get_text()).strip()
        print("🟢 Title.")
        return True, modified_book_title
    else:
        print("🔴 Title.")
        return False, ""


# GET BOOK PAGES COUNT
def get_book_pages_count(soup) -> (bool, int):
    total = soup.find('div', class_='title').find('h2')
    if total:
        total_pages = total.text.split('(')[-1].split(')')[0]
        print("🟢 Number of chapters.")
        return True, int(total_pages)
    else:
        print("🔴 Number of chapters.")
        return False, 0


# PARSE ALL PARAGRAPHS ON 1 PAGE
# def get_text_from_page(url: str, book_path, page: int):
#     response = requests.get(url)
#     if response.status_code == 200:
#         print("REQUEST TO PAGE " + url + " - SUCCESS")
#         soup = BeautifulSoup(response.text, 'lxml')
#         paragraphs = soup.find_all('p')
#         if paragraphs:
#             for p in paragraphs:
#                 with open(book_path, 'a', encoding='utf-8') as file:
#                     file.write("\n" + "\n" + p.getText())
#
#             print("APPEND TEXT FINISHED - PAGE - " + str(page))
#             return True
#         else:
#             print("PARAGRAPHS - ERROR")
#             return False
#     else:
#         print("REQUEST TO PAGE " + url + " - ERROR")
#         return False


def get_text_from_page_and_save_to_json(url: str, book_path, page: int, max_pages: int):
    response = requests.get(url)
    if response.status_code == 200:
        # print("REQUEST TO PAGE " + url + " - SUCCESS")
        soup = BeautifulSoup(response.text, 'lxml')
        paragraphs = soup.find_all('p')
        if paragraphs:
            full_chapter = ''
            for p in paragraphs:
                with open(book_path, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)

                data = "\n\n" + p.getText()
                full_chapter += data

            # print("FULL_CHAPTER - " + full_chapter)
            existing_data["chapters"].append(full_chapter)
            # existing_data["chapters"].append({"text": full_chapter})
            with open(book_path, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

            # print("APPEND TEXT FINISHED - PAGE - " + str(page))
            return True
        else:
            if page < max_pages:
                return True
            else:
                print("🔴 Cant parse page.")
                return False
    else:
        print("🔴 request - " + url)
        return False

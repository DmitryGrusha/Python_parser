import Parser_admin

already_parsed_file_path = "already_parsed" + ".txt"
split_char = "|"
books_path = "Books/"
import os

def save_url_to_already_parsed(url, category):
    book_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), books_path + category)
    # create directory if not exist
    if not os.path.exists(book_folder_path):
        os.makedirs(book_folder_path)

    file_path = os.path.join(str(book_folder_path), already_parsed_file_path)

    with open(file_path, 'a') as file:
        file.write(url + split_char)


def is_already_exists(url, category):
    folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), books_path + category)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        file_path = os.path.join(str(folder_path), already_parsed_file_path)
        with open(file_path, 'r') as file:
            content = file.read().split(split_char)
            return (url in content)
    else:
        return False


def how_much_is_already_exists(list, category):
    folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), books_path + category)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        file_path = os.path.join(str(folder_path), already_parsed_file_path)
        with open(file_path, 'r') as file:
            content = file.read().split(split_char)
            filtered_content = [item for item in content if item != '']

            filtered_list = [element for element in list if element not in filtered_content]
            percent = (len(filtered_content) * 100) / len(filtered_list)
            print("Already parsed in this category - " + str(percent) + "%")

# CATEGORIES
from RBFO_Parse_Category import *
from RBFO_Parse_Book_Data import *

stop = False

def lets_go(category):
    parse_links_result, data = parse_all_books_links_in(category=category)
    book_url_saved = 0
    if parse_links_result:
        print("✅Parse all books links")
        for link in data:
            if stop:
                print("Stop parse...")
                Parser_admin.stop = False
                break
            how_much_is_already_exists(data, category=category)
            url = "https://readbookfreeonline.com" + link
            if is_already_exists(url, category=category) is False:
                parse_book_result = parse_by(url, category=category)
                if parse_book_result:
                    save_url_to_already_parsed(url, category=category)
                    book_url_saved += 1
                    print("Book_saved - " + url)
                else:
                    print("🔴 - Parse book error.")
                    break
            else:
                print("☑️ Book already parsed")
        print("✅✅✅DONE")
    else:
        print("🔴 - Parse links error")

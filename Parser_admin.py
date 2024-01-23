already_parsed_file_path = "already_parsed" + ".txt"
split_char = "|"

def save_url_to_already_parsed(url):
    with open(already_parsed_file_path, 'a') as file:
        file.write(url + split_char)


def is_already_exists(url):
    with open(already_parsed_file_path, 'r') as file:
        content = file.read().split(split_char)
        return (url in content)


# def how_much_is_already_exists(array: [str]):
#     with

# CATEGORIES
from RBFO_Parse_Category import *
from RBFO_Parse_Book_Data import *

def lets_go(category):
    parse_links_result, data = parse_all_books_links_in(category=category)
    book_url_saved = 0
    if parse_links_result:
        print("✅Parse all books links")
        for link in data:
            url = "https://readbookfreeonline.com" + link
            if is_already_exists(url) is False:
                parse_book_result = parse_by(url)
                if parse_book_result:
                    save_url_to_already_parsed(url)
                    book_url_saved += 1
                    print("Book_saved - " + url)
                    break
                else:
                    print("🔴 - Parse book error.")
                    break
            else:
                print("☑️ Book already parsed")
    else:
        print("🔴 - Parse links error")

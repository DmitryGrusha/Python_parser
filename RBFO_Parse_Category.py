import Genre
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://readbookfreeonline.com/"
page_component = "/p/"
def parse_all_books_links_in(category: str):
    all_links = []
    # for category in categories_array:
    url = base_url + category.lower()
    # find max pages count in category
    max_pages_result, max_pages = find_category_pages_count(url)
    if max_pages_result is False: return False, []
    # print(url + " pages - " + str(max_pages))
    print("Category - " + category)
    print("Pages - " + str(max_pages))
    # parser all pages and take urls for book parsing
    parser_all_pages_result, data = parse_all_pages(url, int(max_pages))
    if parser_all_pages_result is False: return False, []
    all_links.extend(data)

    return True, all_links


def find_category_pages_count(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    a_element = soup.find('a', text='»')
    if a_element:
        href_value = a_element.get('href')
        if href_value is None: return True, 1
        match = re.search(r'/(\d+)$', href_value)

        if match:
            max_pages = match.group(1)
            print("Number of pages - " + str(max_pages))
            return True, max_pages
        else:
            print('🔴 Can not decode number of pages')
            return False, 0
    else:
        print("🔴 Can not find number of pages")
        return False, 0

def parse_all_pages(url, max_pages: int):
    page = 1
    all_books_in_category = []
    print("Start parsing all books links.")
    while True:
        print("Progress - " + str(int(float(page * 100) / float(max_pages))) + "%")
        page_url = url + page_component + str(page)
        if max_pages == 1: page_url = url
        result, all_links = get_all_links_on_page(page_url)
        if result:
            all_books_in_category.extend(all_links)
        else:
            print("🔴 GET_ALL_LINKS_ON_PAGE")
            return False, all_books_in_category
        if page < max_pages:
            page += 1
        else:
            return True, all_books_in_category


def get_all_links_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    div_elements = soup.find_all('div', class_='img-home-title thumbnail')

    links = []
    if div_elements:

        for div_element in div_elements:
            a_elements = div_element.find_all('a', href=True)
            href_values = [a.get('href') for a in a_elements]
            links.extend(href_values)

        return True, links
    else:
        return False, []
import requests
from bs4 import BeautifulSoup


from RBFO_Parse_Book_Data import get_storyline
from RBFO_Parse_Book_Data import get_genres

def parse_storyline(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        result, storyline = get_storyline(soup)
        if result:
            print("STORYLINE - SUCCESS")
            print(storyline)
        else:
            print("STORYLINE - ERROR")
    else:
        print("REQUEST - ERROR")


def parse_genres(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        result, genres = get_genres(soup)
        if result:
            print("GENRES - SUCCESS")
            print(genres)
        else:
            print("GENRES - ERROR")
    else:
        print("REQUEST - ERROR")
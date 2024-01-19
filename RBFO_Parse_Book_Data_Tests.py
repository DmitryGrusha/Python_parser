import requests
from bs4 import BeautifulSoup

from RBFO_Parse_Book_Data import get_genre

def parse_by(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        # result, storyline = get_storyline(soup)
        result, genre = get_genre(soup)
        if result:
            # print("STORYLINE - SUCCESS")
            print(genre)
        # else:
            # print("STORYLINE - ERROR")
    else:
        print("REQUEST - ERROR")
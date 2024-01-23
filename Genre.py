from enum import Enum

class Genre(Enum):
    Romance = 1, 'romance'
    Adventure = 2, 'adventure'
    Thriller = 3, 'thriller'
    Fantasy = 4, 'fantasy'
    YoungAdult = 5, 'young-adult'
    Mystery = 6, 'mystery'
    Historical = 7, 'historical'
    Horror = 8, 'horror'
    ScienceFiction = 9, 'science-fiction'
    Humorous = 10, 'humorous'
    Christian = 11, 'christian'
    Western = 12, 'western'



def get_array_of_ids_by_name(cases_ids: [str]) -> [int]:
    results = []
    for case_name in cases_ids:
        for genre_case in Genre.__members__:
            if case_name.lower() == genre_case.lower():
                results.append(Genre[genre_case].value[0])
    return results

def get_all_names() -> [str]:
    return [genre.value[1] for genre in Genre]
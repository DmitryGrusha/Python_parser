from enum import Enum

class Genre(Enum):
    Romance = 1
    Adventure = 2
    Thriller = 3
    Fantasy = 4
    YoungAdult = 5
    Mystery = 6
    Historical = 7
    Horror = 8
    ScienceFiction = 9
    Humorous = 10
    Christian = 11
    Western = 12


def get_case_by_name(case_str: str):
    for case in Genre.__members__:
        if case_str.lower() == case.lower():
            return Genre[case]
    return None


def get_case_by_id(case_int: int):
    for case in Genre:
        if case_int == case.value:
            return case
    return None


def get_cases_by_names(cases_str: [str]) -> [Genre]:
    results = []
    for case in cases_str:
        for genre_case in Genre.__members__:
            if case.lower() == genre_case.lower():
                results.append(Genre[genre_case])


    return results


def get_cases_by_ids(cases_int: [int]) -> [Genre]:
    results = []
    for case in cases_int:
        for genre_case in Genre:
            if case == genre_case.value:
                results.append(genre_case)
    return results

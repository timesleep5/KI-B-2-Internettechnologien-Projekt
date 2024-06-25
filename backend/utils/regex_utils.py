import re
from datetime import datetime


def find_summary_id(content: str) -> int:
    pattern = re.compile(r'\b\d+\b')
    matches = pattern.findall(content)

    for match in matches:
        number = int(match)
        if number < 100:
            return number
    raise ValueError('No id given')


def find_date(content: str) -> datetime:
    # format DD-MM-YYYY
    pattern = re.compile(r'\b\d{2}-\d{2}-\d{4}\b')
    matches = pattern.findall(content)

    for match in matches:
        try:
            date = datetime.strptime(match, '%d-%m-%Y')
            return date
        except ValueError:
            continue
    raise ValueError('No valid date found')


def find_number(content: str) -> int:
    pattern = re.compile(r'\b\d+\b')
    matches = pattern.findall(content)

    if matches:
        return int(matches[0])
    raise ValueError('No number given')

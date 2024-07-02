import json
import os
import random
import re
from typing import Any, Dict, List


class Paths:
    BOT_DATA_DIR = 'bot_data'
    BOT_QUESTIONS = f'{BOT_DATA_DIR}/questions.json'
    BOT_FALLBACKS = f'{BOT_DATA_DIR}/fallback.json'
    BOT_TRANSITIONS = f'{BOT_DATA_DIR}/transitions.json'
    BOT_GREETINGS = f'{BOT_DATA_DIR}/greetings.json'

    SUMMARY_DIR = 'summaries'
    SUMMARY_PATTERN = r'summary_(\d{2}).json'


def read_summary_with_id(id: int) -> Any:
    """
    Read a summary JSON file given its ID.

    :param id: The ID of the summary to read.
    :return: The content of the JSON file.
    :raises FileNotFoundError: If the summary file does not exist.
    """
    summary_name = summary_name_from_id(id)
    summary_path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    return read_json(summary_path)


def summary_name_from_id(id: int) -> str:
    """
    Generate the summary file name from its ID.

    :param id: The ID of the summary.
    :return: The generated summary file name.
    """
    return f'summary_{id:02}.json'


def read_json(path: str) -> Any:
    """
    Read and parse JSON data from a file.

    :param path: The path to the JSON file.
    :return: The parsed JSON data.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
    """
    with open(path, 'r') as file:
        return json.load(file)


def save_json(data: Dict) -> int:
    """
    Save data to a JSON file and return its assigned ID.

    :param: data: The data to save.
    :return: The ID assigned to the saved summary.

    """
    id = next_free_id()
    summary_name = summary_name_from_id(id)
    path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)
    return id


def next_free_id() -> int:
    """
    Find the next available ID for saving a summary.

    :return: The next available ID.
    """
    id_set = set(saved_summary_ids())
    smallest_id = 1

    while smallest_id in id_set:
        smallest_id += 1

    if smallest_id >= 100:
        return remove_random_summary()

    return smallest_id


def saved_summary_ids() -> List[int]:
    """
    Retrieve a list of IDs of saved summaries.

    :return: List of saved summary IDs.
    """
    summary_numbers = []
    pattern = re.compile(Paths.SUMMARY_PATTERN)

    for filename in os.listdir(Paths.SUMMARY_DIR):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            summary_numbers.append(number)
    return summary_numbers


def remove_random_summary() -> int:
    """
    Remove a randomly selected summary file and return its ID.

    :return: The ID of the removed summary.
    """
    id = random.randint(1, 99)
    summary_name = summary_name_from_id(id)
    path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    os.remove(path)
    return id

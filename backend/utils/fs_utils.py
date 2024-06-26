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
    summary_name = summary_name_from_id(id)
    summary_path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    return read_json(summary_path)


def summary_name_from_id(id: int) -> str:
    return f'summary_{id:02}.json'


def read_json(path: str) -> Any:
    with open(path, 'r') as file:
        return json.load(file)


def save_json(data: Dict) -> int:
    id = next_free_id()
    summary_name = summary_name_from_id(id)
    path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    with open(path, 'w') as file:
        json.dump(data, file, indent=2)
    return id


def next_free_id() -> int:
    id_set = set(saved_summary_ids())
    smallest_id = 1

    while smallest_id in id_set:
        smallest_id += 1

    if smallest_id >= 100:
        return remove_random_summary()

    return smallest_id


def saved_summary_ids() -> List[int]:
    summary_numbers = []
    pattern = re.compile(Paths.SUMMARY_PATTERN)

    for filename in os.listdir(Paths.SUMMARY_DIR):
        match = pattern.match(filename)
        if match:
            number = int(match.group(1))
            summary_numbers.append(number)
    return summary_numbers


def remove_random_summary() -> int:
    id = random.randint(1, 99)
    summary_name = summary_name_from_id(id)
    path = os.path.join(Paths.SUMMARY_DIR, summary_name)
    os.remove(path)
    return id

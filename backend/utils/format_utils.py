from datetime import datetime, timedelta
from typing import Any


def is_valid_startdate(start_datetime: datetime) -> bool:
    """
    Check if the start date is valid.

    A start date is considered valid if it lies at least one day in the past.

    :param start_datetime: The start date to validate.
    :return: True if the start date is valid, False otherwise.
    """
    now = datetime.now().date()
    threshold_date = now - timedelta(days=1)
    start_date = start_datetime.date()

    return start_date <= threshold_date


def is_positive_integer(integer: int) -> bool:
    """
    Checks if the given integer is a positive integer (including zero).

    A positive integer is defined as any integer that is zero or greater.

    :param integer: The integer to check.
    :return: True if the integer is positive (including zero), False otherwise.
    """
    return is_strictly_positive_integer(integer) or integer == 0


def is_strictly_positive_integer(integer: int) -> bool:
    """
    Checks if the given integer is strictly positive.

    A strictly positive integer is defined as any integer greater than zero.

    :param integer: The integer to check.
    :return: True if the integer is strictly positive, False otherwise.
    """
    return integer > 0


def round_to(value: Any, decimals=1):
    """
    Rounds a numerical value to one decimal place.

    :param value: The value to round.
    :param decimals: The number of decimal places to round to.
    :return: Rounded value.
    """
    return round(value, decimals)


def insert_spaces(term: str, number_of_chars=30) -> str:
    """
    Inserts spaces to align terms in the summary output.

    :param term: Term to align.
    :param number_of_chars: Number of characters in total.
    :return:str: Term with added spaces for alignment.
    """
    remaining_chars = number_of_chars - len(term)
    added_spaces = remaining_chars * ' '
    return term + added_spaces


def separator_of_length(length: int, separator='~') -> str:
    """
    Generates a separator line of specified length.

    :param length: Length of the separator.
    :param separator: Separator to use.
    :return: Separator line.
    """
    return length * separator

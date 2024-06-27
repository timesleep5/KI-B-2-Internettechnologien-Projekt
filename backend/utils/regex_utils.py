import re
from datetime import datetime


def find_summary_id(content: str) -> int:
    """
    Find the first valid summary ID in the given content.

    Args:
        content (str): The text to search for a summary ID.

    Returns:
        int: The found summary ID.

    Raises:
        ValueError: If no valid summary ID is found.
    """
    pattern = re.compile(r'\b\d+\b')  # Matches sequences of digits
    matches = pattern.findall(content)  # Find all matches in content

    for match in matches:
        number = int(match)
        if number < 100:  # Check if the number is a valid summary ID
            return number
    raise ValueError('No id given')  # Raise error if no valid ID is found


def find_date(content: str) -> datetime:
    """
    Find the first valid date in DD-MM-YYYY format in the given content.

    Args:
        content (str): The text to search for a date.

    Returns:
        datetime: The found date.

    Raises:
        ValueError: If no valid date is found.
    """
    pattern = re.compile(r'\b\d{2}-\d{2}-\d{4}\b')  # Matches dates in DD-MM-YYYY format
    matches = pattern.findall(content)  # Find all matches in content

    for match in matches:
        try:
            date = datetime.strptime(match, '%d-%m-%Y')  # Parse match into datetime object
            return date
        except ValueError:
            continue  # Continue to next match if parsing fails
    raise ValueError('No valid date found')  # Raise error if no valid date is found


def find_number(content: str) -> int:
    """
    Find the first valid integer number in the given content.

    Args:
        content (str): The text to search for a number.

    Returns:
        int: The found number.

    Raises:
        ValueError: If no valid number is found.
    """
    pattern = re.compile(r'\b\d+(?=\b|\D)')  # Matches sequences of digits
    matches = pattern.findall(content)  # Find all matches in content

    if matches:
        return int(matches[0])  # Convert first match to integer
    raise ValueError('No number given')  # Raise error if no valid number is found

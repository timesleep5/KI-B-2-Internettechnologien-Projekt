from datetime import datetime, timedelta


def is_valid_startdate(start_datetime: datetime) -> bool:
    """
    Check if the startdate is valid.

    A startdate is considered valid if it lies at least one day in the past.

    Args:
        start_datetime (datetime): The start date to validate.

    Returns:
        bool: True if the startdate is valid, False otherwise.
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


from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


def format_date(date: datetime) -> str:
  """
  Formats a datetime object into a string (DD.MM.YYYY).

  :param date: The datetime object to format.
  :return: Formatted date string.
  """
  return date.strftime("%d.%m.%Y")


def calculate_end_date(start_date: datetime, runtime_months: int) -> datetime:
  """
  Calculates the end date of the contract based on the start date and runtime in months.

  :param start_date: The start date of the leasing contract.
  :param runtime_months: The duration of the contract in months.
  :return:datetime: The calculated end date of the contract.
  """
  end_date = start_date + relativedelta(months=runtime_months)
  end_date -= timedelta(days=1)
  return end_date


def calculate_runtime_days(start_date: datetime, end_date: datetime) -> int:
  """
  Calculates the total number of days in the contract period.

  :param start_date: The start date of the leasing contract.
  :param end_date: The end date of the leasing contract.

  :return: Total number of days in the contract period.
  """
  return (end_date - start_date).days

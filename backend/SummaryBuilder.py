from datetime import datetime, timedelta
from typing import Dict, Any, Tuple

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from datastructures.ChatModels import LeasingContract


class SummaryBuilder:
    """
    Builds a summary report for a leasing contract based on provided parameters.

    Attributes:
        __contract (LeasingContract): The leasing contract details.
        __km_driven (float): Kilometers driven during the contract period.
        __summary_data (Dict[str, Any]): Summary data calculated based on the contract.
    """

    def __init__(self, start_date: datetime, runtime_months: int, km_limit: int, km_driven: float):
        """
        Initializes a SummaryBuilder instance with a LeasingContract and calculated summary data.

        Args:
            start_date (datetime): The start date of the leasing contract.
            runtime_months (int): The duration of the contract in months.
            km_limit (int): The kilometer limit for the contract.
            km_driven (float): The kilometers already driven during the contract period.
        """
        end_date = self.__calculate_end_date(start_date, runtime_months)
        runtime_days = self.__calculate_runtime_days(start_date, end_date)
        self.__contract = LeasingContract(
            start_date=start_date,
            end_date=end_date,
            km_limit=km_limit,
            runtime_days=runtime_days,
            runtime_months=runtime_months
        )
        self.__km_driven = km_driven
        self.__summary_data = self.__calculate_summary()

    def get_summary(self) -> str:
        """
        Generates a formatted summary string from the calculated summary data.

        Returns:
            str: Formatted summary string.
        """
        return self.get_summary_from_data(self.__summary_data)

    def get_summary_data(self) -> Dict[str, Any]:
        """
        Retrieves the calculated summary data.

        Returns:
            Dict[str, Any]: Calculated summary data.
        """
        return self.__summary_data

    def __calculate_end_date(self, start_date: datetime, runtime_months: int) -> datetime:
        """
        Calculates the end date of the contract based on the start date and runtime in months.

        Args:
            start_date (datetime): The start date of the leasing contract.
            runtime_months (int): The duration of the contract in months.

        Returns:
            datetime: The calculated end date of the contract.
        """
        end_date = start_date + relativedelta(months=runtime_months)
        end_date -= timedelta(days=1)
        return end_date

    def __calculate_runtime_days(self, start_date: datetime, end_date: datetime) -> int:
        """
        Calculates the total number of days in the contract period.

        Args:
            start_date (datetime): The start date of the leasing contract.
            end_date (datetime): The end date of the leasing contract.

        Returns:
            int: Total number of days in the contract period.
        """
        return (end_date - start_date).days

    def __calculate_summary(self) -> Dict[str, Any]:
        """
        Calculates various summary metrics based on the leasing contract.

        Returns:
            Dict[str, Any]: Calculated summary metrics.
        """
        return {
            'contract': self.__contract_overview(),
            'start date': self.__format_date(self.__contract.start_date),
            'end date': self.__format_date(self.__contract.end_date),
            'daily average': self.__calculate_daily_average(),
            'monthly average': self.__calculate_monthly_average(),
            'day': self.__day_number_in_contract(),
            'of': self.__contract.runtime_days,
            'allowed kms so far': self.__calculate_allowed_kms(),
            'driven': self.__km_driven,
            'difference': self.__calculate_allowed_km_difference(),
            'daily average so far': self.__calculate_daily_average_so_far(),
            'daily average from now': self.__calculate_daily_average_from_now()
        }

    def __contract_overview(self) -> str:
        """
        Generates a textual overview of the leasing contract.

        Returns:
            str: Textual overview of the leasing contract.
        """
        return f'{self.__contract.km_limit} km over {self.__contract.runtime_months} months'

    def __format_date(self, date: datetime) -> str:
        """
        Formats a datetime object into a string (DD.MM.YYYY).

        Args:
            date (datetime): The datetime object to format.

        Returns:
            str: Formatted date string.
        """
        return date.strftime("%d.%m.%Y")

    def __calculate_daily_average(self) -> float:
        """
        Calculates the daily average kilometers allowed for the contract.

        Returns:
            float: Daily average kilometers allowed.
        """
        km_limit = self.__contract.km_limit
        runtime_days = self.__contract.runtime_days
        daily_average = km_limit / runtime_days
        return self.__round(daily_average)

    def __calculate_monthly_average(self) -> float:
        """
        Calculates the monthly average kilometers allowed for the contract.

        Returns:
            float: Monthly average kilometers allowed.
        """
        days_per_month = 30
        daily_average = self.__calculate_daily_average()
        monthly_average = days_per_month * daily_average
        return self.__round(monthly_average)

    def __day_number_in_contract(self) -> int:
        """
        Calculates the current day number within the contract.

        Returns:
            int: Current day number within the contract.
        """
        today_date = datetime.now()
        start_date = self.__contract.start_date
        day_number = (today_date - start_date).days
        return day_number

    def __calculate_allowed_kms(self) -> float:
        """
        Calculates the allowed kilometers driven so far in the contract.

        Returns:
            float: Allowed kilometers driven so far.
        """
        day_number = self.__day_number_in_contract()
        daily_average = self.__calculate_daily_average()
        allowed_kms_so_far = day_number * daily_average
        return self.__round(allowed_kms_so_far)

    def __calculate_allowed_km_difference(self) -> float:
        """
        Calculates the difference between allowed kilometers and kilometers driven.

        Returns:
            float: Difference between allowed kilometers and kilometers driven.
        """
        allowed_km_difference = self.__calculate_allowed_kms() - self.__km_driven
        return self.__round(allowed_km_difference)

    def __calculate_daily_average_so_far(self) -> float:
        """
        Calculates the average kilometers driven per day so far in the contract.

        Returns:
            float: Average kilometers driven per day so far.
        """
        km_driven = self.__km_driven
        day_number = self.__day_number_in_contract()
        daily_average_so_far = km_driven / day_number
        return self.__round(daily_average_so_far)

    def __calculate_daily_average_from_now(self) -> float:
        """
        Calculates the estimated daily average kilometers needed to meet the contract limit from now.

        Returns:
            float: Estimated daily average kilometers needed.
        """
        remaining_km = self.__contract.km_limit - self.__km_driven
        remaining_days = self.__contract.runtime_days - self.__day_number_in_contract()
        daily_average_from_now = remaining_km / remaining_days
        return self.__round(daily_average_from_now)

    @staticmethod
    def get_summary_from_data(data: Dict[str, Any]) -> str:
        """
        Generates a formatted summary string from provided summary data.

        Args:
            data (Dict[str, Any]): Summary data to include in the summary.

        Returns:
            str: Formatted summary string.
        """
        header, footer = SummaryBuilder.__header_and_footer()
        summary = header + '\n'

        for key in data.keys():
            key_name = SummaryBuilder.__insert_spaces(key + ':')
            entry = f'{key_name}{data[key]}\n'
            summary += entry

        summary += footer
        return summary

    @staticmethod
    def __round(value: Any):
        """
        Rounds a numerical value to one decimal place.

        Args:
            value (Any): The value to round.

        Returns:
            Any: Rounded value.
        """
        decimals = 1
        return round(value, decimals)

    @staticmethod
    def __header_and_footer() -> Tuple[str, str]:
        """
        Generates header and footer lines for the summary report.

        Returns:
            Tuple[str, str]: Header and footer lines.
        """
        separator = SummaryBuilder.__separator_of_length(18)
        header = separator + ' SUMMARY ' + separator
        footer = SummaryBuilder.__separator_of_length(len(header))
        return header, footer

    @staticmethod
    def __separator_of_length(length: int) -> str:
        """
        Generates a separator line of specified length.

        Args:
            length (int): Length of the separator.

        Returns:
            str: Separator line.
        """
        return length * '~'

    @staticmethod
    def __insert_spaces(term: str) -> str:
        """
        Inserts spaces to align terms in the summary output.

        Args:
            term (str): Term to align.

        Returns:
            str: Term with added spaces for alignment.
        """
        number_of_chars = 30
        remaining_chars = number_of_chars - len(term)
        added_spaces = remaining_chars * ' '
        return term + added_spaces

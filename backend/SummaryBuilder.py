from datetime import datetime
from typing import Dict, Any, Tuple

from backend.utils.date_utils import format_date, calculate_end_date, calculate_runtime_days
from backend.utils.format_utils import round_to, insert_spaces, separator_of_length
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

        :param start_date: The start date of the leasing contract.
        :param runtime_months: The duration of the contract in months.
        :param km_limit: The kilometer limit for the contract.
        :param km_driven: The kilometers already driven during the contract period.
        """
        end_date = calculate_end_date(start_date, runtime_months)
        runtime_days = calculate_runtime_days(start_date, end_date)
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

        :return: Formatted summary string.
        """
        return self.get_summary_from_data(self.__summary_data)

    def get_summary_data(self) -> Dict[str, Any]:
        """
        Retrieves the calculated summary data.

        :return: Calculated summary data.
        """
        return self.__summary_data

    def __calculate_summary(self) -> Dict[str, str]:
        """
        Calculates various summary metrics based on the leasing contract.

        :return: Calculated summary metrics.
        """
        return {
            'contract': self.__contract_overview(),
            'start date': format_date(self.__contract.start_date),
            'end date': format_date(self.__contract.end_date),
            'daily average': f'{self.__calculate_daily_average()} km/day',
            'monthly average': f'{self.__calculate_monthly_average()} km/month',
            'day': f'{self.__day_number_in_contract()} of {self.__contract.runtime_days} days',
            'allowed kms so far': f'{self.__calculate_allowed_kms()} km',
            'driven': f'{self.__km_driven} km',
            'difference': f'{self.__calculate_allowed_km_difference()} km',
            'daily average so far': f'{self.__calculate_daily_average_so_far()} km/day',
            'daily average from now': f'{self.__calculate_daily_average_from_now()} km/day',
        }

    def __contract_overview(self) -> str:
        """
        Generates a textual overview of the leasing contract.

        :return: Textual overview of the leasing contract.
        """
        return f'{self.__contract.km_limit} km over {self.__contract.runtime_months} months'

    def __calculate_daily_average(self) -> float:
        """
        Calculates the daily average kilometers allowed for the contract.

        :return: Daily average kilometers allowed.
        """
        km_limit = self.__contract.km_limit
        runtime_days = self.__contract.runtime_days
        daily_average = km_limit / runtime_days
        return round_to(daily_average)

    def __calculate_monthly_average(self) -> float:
        """
        Calculates the monthly average kilometers allowed for the contract.

        :return: Monthly average kilometers allowed.
        """
        days_per_month = 30
        daily_average = self.__calculate_daily_average()
        monthly_average = days_per_month * daily_average
        return round_to(monthly_average)

    def __day_number_in_contract(self) -> int:
        """
        Calculates the current day number within the contract.

        :return: Current day number within the contract.
        """
        today_date = datetime.now()
        start_date = self.__contract.start_date
        day_number = (today_date - start_date).days
        return day_number

    def __calculate_allowed_kms(self) -> float:
        """
        Calculates the allowed kilometers driven so far in the contract.

        :return: Allowed kilometers driven so far.
        """
        day_number = self.__day_number_in_contract()
        daily_average = self.__calculate_daily_average()
        allowed_kms_so_far = day_number * daily_average
        return round_to(allowed_kms_so_far)

    def __calculate_allowed_km_difference(self) -> float:
        """
        Calculates the difference between allowed kilometers and kilometers driven.

        :return: Difference between allowed kilometers and kilometers driven.
        """
        allowed_km_difference = self.__calculate_allowed_kms() - self.__km_driven
        return round_to(allowed_km_difference)

    def __calculate_daily_average_so_far(self) -> float:
        """
        Calculates the average kilometers driven per day so far in the contract.

        :return: Average kilometers driven per day so far.
        """
        km_driven = self.__km_driven
        day_number = self.__day_number_in_contract()
        daily_average_so_far = km_driven / day_number
        return round_to(daily_average_so_far)

    def __calculate_daily_average_from_now(self) -> float:
        """
        Calculates the estimated daily average kilometers needed to meet the contract limit from now.

        :return: Estimated daily average kilometers needed.
        """
        remaining_km = self.__contract.km_limit - self.__km_driven
        remaining_days = self.__contract.runtime_days - self.__day_number_in_contract()
        daily_average_from_now = remaining_km / remaining_days
        return round_to(daily_average_from_now)

    @staticmethod
    def get_summary_from_data(data: Dict[str, Any]) -> str:
        """
        Generates a formatted summary string from provided summary data.

        :param data: Summary data to include in the summary.
        :return: Formatted summary string.
        """
        header, footer = SummaryBuilder.__header_and_footer()
        summary = header + '\n'

        for key in data.keys():
            key_name = insert_spaces(key + ':')
            entry = f'{key_name}{data[key]}\n'
            summary += entry

        summary += footer
        return summary

    @staticmethod
    def __header_and_footer() -> Tuple[str, str]:
        """
        Generates header and footer lines for the summary report.

        :return: Header and footer lines.
        """
        separator = separator_of_length(18)
        header = separator + ' SUMMARY ' + separator
        footer = separator_of_length(len(header))
        return header, footer

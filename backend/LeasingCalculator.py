import calendar
from datetime import datetime
from typing import Dict, Any, Tuple

from Models import LeasingContract


class LeasingCalculator:
    def __init__(self, start_date: datetime, runtime_months: int, km_limit: int, km_driven: float):
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
        self.__summary_values = self.__calculate_summary()

    def get_summary(self) -> str:
        header, footer = self.__header_and_footer()
        summary = header + '\n'

        for key in self.__summary_values.keys():
            key_name = self.__insert_spaces(key + ':')
            entry = f'{key_name}{self.__summary_values[key]}\n'
            summary += entry

        summary += footer
        return summary

    def __calculate_end_date(self, start_date: datetime, runtime_months: int) -> datetime:
        future_month = start_date.month + runtime_months
        future_year = start_date.year + future_month // 12
        future_month %= 12

        if future_month == 0:
            future_month = 12
            future_year -= 1

        last_day_of_future_month = calendar.monthrange(future_year, future_month)[1]
        future_day = min(start_date.day, last_day_of_future_month)

        return datetime(future_year, future_month, future_day)

    def __calculate_runtime_days(self, start_date: datetime, end_date: datetime) -> int:
        return (end_date - start_date).days

    def __calculate_summary(self) -> Dict[str, Any]:
        return {
            'contract': self.__contract_overview(),
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
        return f'{self.__contract.km_limit} km over {self.__contract.runtime_months} months'

    def __calculate_daily_average(self) -> float:
        km_limit = self.__contract.km_limit
        runtime_days = self.__contract.runtime_days
        daily_average = km_limit / runtime_days
        return self.__round(daily_average)

    def __calculate_monthly_average(self) -> float:
        days_per_month = 30
        daily_average = self.__calculate_daily_average()
        monthly_average = days_per_month * daily_average
        return self.__round(monthly_average)

    def __day_number_in_contract(self) -> int:
        today_date = datetime.now()
        start_date = self.__contract.start_date
        day_number = (today_date - start_date).days
        return day_number

    def __calculate_allowed_kms(self) -> float:
        day_number = self.__day_number_in_contract()
        daily_average = self.__calculate_daily_average()
        allowed_kms_so_far = day_number * daily_average
        return self.__round(allowed_kms_so_far)

    def __calculate_allowed_km_difference(self) -> float:
        allowed_km_difference = self.__calculate_allowed_kms() - self.__km_driven
        return self.__round(allowed_km_difference)

    def __calculate_daily_average_so_far(self) -> float:
        km_driven = self.__km_driven
        day_number = self.__day_number_in_contract()
        daily_average_so_far = km_driven / day_number
        return self.__round(daily_average_so_far)

    def __calculate_daily_average_from_now(self) -> float:
        remaining_km = self.__contract.km_limit - self.__km_driven
        remaining_days = self.__contract.runtime_days - self.__day_number_in_contract()
        daily_average_from_now = remaining_km / remaining_days
        return self.__round(daily_average_from_now)

    def __round(self, value):
        decimals = 1
        return round(value, decimals)

    def __header_and_footer(self) -> Tuple[str, str]:
        separator = self.__separator_of_length(18)
        header = separator + ' SUMMARY ' + separator
        footer = self.__separator_of_length(len(header))
        return header, footer

    def __separator_of_length(self, length: int) -> str:
        return length * '~'

    def __insert_spaces(self, term: str):
        number_of_chars = 30
        remaining_chars = number_of_chars - len(term)
        added_spaces = remaining_chars * ' '
        return term + added_spaces


lc = LeasingCalculator(datetime(2024, 3, 1), 9, 8000, 2714)
print(lc.get_summary())

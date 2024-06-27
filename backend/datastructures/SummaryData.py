from datetime import datetime


class SummaryData:
    """
    Represents summary data including start date, months, kilometer limit, and kilometers driven.

    Attributes:
        __data (dict): Dictionary holding summary data with default values:
            - 'start_date': Initial date set to January 1, 1970.
            - 'months': Initial value set to 0.
            - 'km_limit': Initial value set to 0.
            - 'km_driven': Initial value set to 0.
    """

    def __init__(self):
        """
        Initializes a SummaryData object with default values.
        """
        self.__data = {
            'start_date': datetime(1970, 1, 1),
            'months': 0,
            'km_limit': 0,
            'km_driven': 0
        }

    def is_complete(self) -> bool:
        """
        Checks if all essential data attributes have been set.

        Returns:
            bool: True if all attributes are set, False otherwise.
        """
        for value in self.__data.values():
            if value == 0 or value == datetime(1970, 1, 1):
                return False
        return True

    def get_start_date(self) -> datetime:
        """
        Retrieves the start date.

        Returns:
            datetime: The start date.
        """
        return self.__data['start_date']

    def set_start_date(self, date: datetime):
        """
        Sets the start date.

        Args:
            date (datetime): The start date to set.
        """
        self.__data['start_date'] = date

    def get_months(self) -> int:
        """
        Retrieves the number of months.

        Returns:
            int: The number of months.
        """
        return self.__data['months']

    def set_months(self, months: int):
        """
        Sets the number of months.

        Args:
            months (int): The number of months to set.
        """
        self.__data['months'] = months

    def get_km_limit(self) -> int:
        """
        Retrieves the kilometer limit.

        Returns:
            int: The kilometer limit.
        """
        return self.__data['km_limit']

    def set_km_limit(self, km_limit: int):
        """
        Sets the kilometer limit.

        Args:
            km_limit (int): The kilometer limit to set.
        """
        self.__data['km_limit'] = km_limit

    def get_km_driven(self) -> int:
        """
        Retrieves the kilometers driven.

        Returns:
            int: The kilometers driven.
        """
        return self.__data['km_driven']

    def set_km_driven(self, km_driven: int):
        """
        Sets the kilometers driven.

        Args:
            km_driven (int): The kilometers driven to set.
        """
        self.__data['km_driven'] = km_driven

    def __repr__(self) -> str:
        """
        Returns a string representation of the SummaryData object.

        Returns:
            str: String representation including start date, months, kilometer limit, and kilometers driven.
        """
        start_date_str = self.__data['start_date'].strftime("%d.%m.%Y") if self.__data['start_date'] else 'None'
        return (
            f"  start date: {start_date_str},\n"
            f"  months: {self.__data['months']},\n"
            f"  km limit: {self.__data['km_limit']},\n"
            f"  km driven: {self.__data['km_driven']}\n"
        )

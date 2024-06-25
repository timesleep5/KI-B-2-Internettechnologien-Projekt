from datetime import datetime


class SummaryData:
    def __init__(self):
        self.__data = {
            'start_date': datetime(1970, 1, 1),
            'months': 0,
            'km_limit': 0,
            'km_driven': 0
        }

    def is_complete(self):
        for value in self.__data.values():
            if value == 0 or value == datetime(1970, 1, 1):
                return False
        return True

    def get_start_date(self) -> datetime:
        return self.__data['start_date']

    def set_start_date(self, date: datetime):
        self.__data['start_date'] = date

    def get_months(self) -> int:
        return self.__data['months']

    def set_months(self, months: int):
        self.__data['months'] = months

    def get_km_limit(self) -> int:
        return self.__data['km_limit']

    def set_km_limit(self, km_limit: int):
        self.__data['km_limit'] = km_limit

    def get_km_driven(self) -> int:
        return self.__data['km_driven']

    def set_km_driven(self, km_driven: int):
        self.__data['km_driven'] = km_driven

    def __repr__(self):
        start_date_str = self.__data['start_date'].strftime("%d.%m.%Y") if self.__data['start_date'] else 'None'
        return (
            f"  start_date: {start_date_str},\n"
            f"  months: {self.__data['months']},\n"
            f"  km_limit: {self.__data['km_limit']},\n"
            f"  km_driven: {self.__data['km_driven']}\n"
        )

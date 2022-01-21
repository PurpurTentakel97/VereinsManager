# Purpur Tentakel
# 21.01.2022
# VereinsManager / Performance Schedule

from datetime import date

performance_days: list = list()


class Performance:
    def __init__(self)->None:
        self.performance_time: str = str()
        self.performance_type: str = str()
        self.location: str = str()
        self.location_link: str = str()

        self.comment_text: str = str()


class PerformanceDay:
    def __init__(self)->None:
        self.performance_date: date | None = None
        self.weekday: str = str()
        self.departure_time: str = str()
        self.uniform: str = str()

        self.comment_text: str = str()

        self.performance: list[Performance] = list()

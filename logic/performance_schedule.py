# Purpur Tentakel
# 21.01.2022
# VereinsManager / Performance Schedule

from datetime import date
import enum_sheet

performance_days: list = list()


class Performance:
    def __init__(self, name: str, id_: int) -> None:
        self.id_: int = id_
        self.name: str = name
        self.performance_time: str = str()
        self.performance_type: str = str()
        self.location_name: str = str()
        self.location_link: str = str()

        self.comment_text: str = str()

    def set_name(self, name: str) -> None:
        self.name: str = name

    def set_performance_time(self, time: str) -> None:
        self.performance_time: str = time

    def set_performance_type(self, type_: str) -> None:
        self.performance_type: str = type_

    def set_location_name(self, location: str) -> None:
        self.location_name: str = location

    def set_location_link(self, link: str) -> None:
        self.location_link: str = link

    def set_comment_text(self, text: str) -> None:
        self.comment_text: str = text


class PerformanceDay:
    def __init__(self) -> None:
        self.performance_date: date | None = None
        self.weekday: str = str()
        self.departure_time: str = str()
        self.uniform: str = str()

        self.comment_text: str = str()

        self.performances: list[Performance] = list()

    def set_performance_date(self, date_: dict[str, int]) -> None:
        self.performance_date: date = date(date_["year"], date_["month"], date_["day"])
        self.weekday: str = enum_sheet.weekDaysMapping[self.performance_date.weekday()]

    def set_departure_time(self, time_: str) -> None:
        self.departure_time: str = time_

    def set_uniform(self, uniform: str) -> None:
        self.uniform: str = uniform

    def set_comment_text(self, text: str) -> None:
        self.comment_text: str = text

    def add_performance(self, name: str) -> None:
        self.performances.append(Performance(name=name, id_=len(self.performances)))

    def remove_performance(self, id_: int) -> None:
        self.performances.remove(self._get_performance_from_id(id_=id_))
        self._update_performance_ids()

    def _update_performance_ids(self) -> None:
        counter: int = 0
        for performance in self.performances:
            performance.id_ = counter
            counter += 1

    def _get_performance_from_id(self, id_: int) -> Performance:
        for performance in self.performances:
            if performance.id_ == id_:
                return performance

# Purpur Tentakel
# 13.02.2022
# VereinsManager / Anniversary Handler
import datetime

from sqlite import select_handler as s_h
from config import config_sheet as c

import debug

debug_str = "Anniversary Handler"


def get_anniversary_member_data(type_: str, active: bool, year: int = 0) -> dict | str:
    b_day_data: list = list()
    entry_day_data: list = list()
    member_data = s_h.select_handler.get_name_and_dates_from_member(active=active)
    if isinstance(member_data, str):
        return member_data
    for _, firstname, lastname, b_day, entry_day in member_data:
        if b_day:
            inner: dict = {
                "firstname": firstname,
                "lastname": lastname,
                "b_day": _transform_timestamp_to_datetime(b_day),
            }
            b_day_data.append(inner)
        if entry_day:
            inner: dict = {
                "firstname": firstname,
                "lastname": lastname,
                "entry_day": _transform_timestamp_to_datetime(entry_day),
            }
            entry_day_data.append(inner)

    match type_:
        case "current":
            return _transform_current_data(b_day=b_day_data, entry_day=entry_day_data)

        case "other":
            return _transform_other_data(b_day=b_day_data, entry_day=entry_day_data, year=year)


def _transform_current_data(b_day: list, entry_day: list) -> dict:
    break_day: int = 15
    current_date: datetime.datetime = datetime.datetime.now()

    current_b_day: list = list()
    for entry in b_day:
        if current_date.day <= break_day:
            if entry["b_day"].month == current_date.month:
                current_b_day.append(entry)
        else:
            if entry["b_day"].month == current_date.month and entry["b_day"].day > break_day:
                current_b_day.append(entry)
            elif entry["b_day"].month == current_date.month + 1 and entry["b_day"].day < break_day:
                current_b_day.append(entry)

    final_b_day_data: list = list()
    for entry in current_b_day:
        entry["age"] = _get_years_from_date(entry["b_day"])
        if entry["age"] % 10 == 0 or entry["age"] == 18:
            entry["b_day"] = entry["b_day"].strftime(c.config.date_format["short"])[:-4]
            final_b_day_data.append(entry)

    current_entry_day: list = list()
    for entry in entry_day:
        if current_date.day <= break_day:
            if entry["entry_day"].month == current_date.month:
                current_entry_day.append(entry)
        else:
            if entry["entry_day"].month == current_date.month and entry["entry_day"].day > break_day:
                current_entry_day.append(entry)
            elif entry["entry_day"].month == current_date.month + 1 and entry["entry_day"].day < break_day:
                current_entry_day.append(entry)

    final_entry_date_data: list = list()
    for entry in current_entry_day:
        entry["membership_years"] = _get_years_from_date(entry["entry_day"])
        if entry["membership_years"] % 5 == 0:
            entry["entry_day"] = entry["entry_day"].strftime(c.config.date_format["short"])[:-4]
            final_entry_date_data.append(entry)

    data: dict = {
        "b_day": final_b_day_data,
        "entry_day": final_entry_date_data,
    }

    return data


def _transform_other_data(b_day: list, entry_day: list, year: int) -> dict:
    debug.info(item=debug_str, keyword="_transform_other_data", message=f"data = {b_day} // {entry_day}")


def _transform_timestamp_to_datetime(timestamp: int) -> datetime:
    if timestamp:
        if timestamp > 0:
            return datetime.datetime.fromtimestamp(timestamp)
        else:
            return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)


def _get_years_from_date(date: datetime.datetime) -> int:
    current_date = datetime.datetime.now()
    age = current_date.year - date.year  # TODO date in January False?
    return age

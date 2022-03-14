# Purpur Tentakel
# 13.02.2022
# VereinsManager / Anniversary Handler

import datetime

from sqlite import select_handler as s_h
from config import config_sheet as c, error_code as e
from logic import validation as v

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
                "date": _transform_timestamp_to_datetime(b_day),
            }
            b_day_data.append(inner)
        if entry_day:
            inner: dict = {
                "firstname": firstname,
                "lastname": lastname,
                "date": _transform_timestamp_to_datetime(entry_day),
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
            if entry["date"].month == current_date.month:
                current_b_day.append(entry)
        else:
            if entry["date"].month == current_date.month and entry["date"].day > break_day:
                current_b_day.append(entry)
            elif entry["date"].month == current_date.month + 1 and entry["date"].day < break_day:
                current_b_day.append(entry)

    final_b_day_data: list = list()
    for entry in current_b_day:
        entry["year"] = _get_years_from_date(entry["date"])
        if entry["year"] % 10 == 0 or entry["year"] == 18:
            entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
            final_b_day_data.append(entry)

    current_entry_day: list = list()
    for entry in entry_day:
        if current_date.day <= break_day:
            if entry["date"].month == current_date.month:
                current_entry_day.append(entry)
        else:
            if entry["date"].month == current_date.month and entry["date"].day > break_day:
                current_entry_day.append(entry)
            elif entry["date"].month == current_date.month + 1 and entry["date"].day < break_day:
                current_entry_day.append(entry)

    final_entry_date_data: list = list()
    for entry in current_entry_day:
        entry["year"] = _get_years_from_date(entry["date"])
        if entry["year"] % 5 == 0:
            entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
            final_entry_date_data.append(entry)

    final_b_day_data = sorted(final_b_day_data, key=lambda x: x["date"])
    final_entry_date_data = sorted(final_entry_date_data, key=lambda x: x["date"])

    data: dict = {
        "b_day": final_b_day_data,
        "entry_day": final_entry_date_data,
    }
    return data


def _transform_other_data(b_day: list, entry_day: list, year: int) -> dict:
    try:
        v.validation.must_positive_int(year, max_length=4)
    except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="_transform_other_data", message=f"Error = {error.message}")
        return error.message

    final_b_day_data: list = list()
    for entry in b_day:
        if (year - entry["date"].year) % 10 == 0 or year - entry["date"].year == 18:
            entry["year"] = year - entry["date"].year
            if entry["year"] >= 0:
                entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
                final_b_day_data.append(entry)

    final_entry_day_data: list = list()
    for entry in entry_day:
        if (year - entry["date"].year) % 5 == 0:
            entry["year"] = year - entry["date"].year
            if entry["year"] >= 0:
                entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
                final_entry_day_data.append(entry)

    final_b_day_data = sorted(final_b_day_data, key=lambda x: x["date"])
    final_entry_day_data = sorted(final_entry_day_data, key=lambda x: x["date"])

    data: dict = {
        "b_day": final_b_day_data,
        "entry_day": final_entry_day_data,
    }

    return data


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

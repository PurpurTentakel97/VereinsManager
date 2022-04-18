# Purpur Tentakel
# 13.02.2022
# VereinsManager / Member Data Anniversary Handler

import sys
import datetime
from datetime import timedelta

from helpers import validation, helper
from logic.sqlite import select_handler as s_h
from config import config_sheet as c, exception_sheet as e

import debug

debug_str = "Member Data Anniversary Handler"


def get_anniversary_member_data(type_: str, active: bool, year: int = 0) -> tuple[str | dict, bool]:
    # validation
    try:
        b_day_data: list = list()
        entry_day_data: list = list()
        member_data: tuple = s_h.select_handler.get_name_and_dates_from_member(active=active)

        for _, firstname, lastname, b_day, entry_day in member_data:
            firstname: str
            lastname: str
            b_day: int
            entry_day: int

            inner: dict = {
                "firstname": firstname,
                "lastname": lastname,
                "date": None,  # assigned later
            }

            if b_day:
                inner_b_day: dict = inner.copy()
                inner_b_day["date"]: datetime.datetime = helper.transform_timestamp_to_datetime(b_day)
                b_day_data.append(inner_b_day)
            if entry_day:
                inner_entry_day: dict = inner.copy()
                inner_entry_day["date"]: datetime.datetime = helper.transform_timestamp_to_datetime(entry_day)
                entry_day_data.append(inner_entry_day)

        match type_:
            case "current":
                return _transform_current_data(b_day=b_day_data, entry_day=entry_day_data), True

            case "other":
                return _transform_other_data(b_day=b_day_data, entry_day=entry_day_data, year=year), True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_anniversary_member_data", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_anniversary_member_data", error_=sys.exc_info())
        return error.message, False


def _transform_current_data(b_day: list, entry_day: list) -> dict:
    reference_date_1: datetime.datetime = datetime.datetime.today() - timedelta(days=5)
    reference_date_2: datetime.datetime = datetime.datetime.today() + timedelta(days=31)

    current_b_day: list = list()
    for entry in b_day:
        if reference_date_1.month == entry['date'].month and reference_date_1.day <= entry['date'].day \
                or reference_date_2.month == entry['date'].month and reference_date_2.day >= entry['date'].day:
            current_b_day.append(entry)

    final_b_day_data: list = list()
    for entry in current_b_day:
        entry["year"] = helper.get_years_from_date_to_now(entry["date"])
        if entry["year"] % 10 == 0 or entry["year"] == 18:
            entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
            final_b_day_data.append(entry)

    current_entry_day: list = list()
    for entry in entry_day:
        if reference_date_1.month == entry['date'].month and reference_date_1.day < entry['date'].day \
                or reference_date_2.month == entry['date'].month and reference_date_2.day > entry['date'].day:
            current_entry_day.append(entry)

    final_entry_date_data: list = list()
    for entry in current_entry_day:
        entry["year"] = helper.get_years_from_date_to_now(entry["date"])
        if entry["year"] % 5 == 0:
            entry["date"] = entry["date"].strftime(c.config.date_format["short"])[:-4]
            final_entry_date_data.append(entry)

    final_b_day_data: list = sorted(final_b_day_data, key=lambda x: [x["date"][-3:-1], x["date"][:2]])
    final_entry_date_data: list = sorted(final_entry_date_data, key=lambda x: [x["date"][-3:-1], x["date"][:2]])

    data: dict = {
        "b_day": final_b_day_data,
        "entry_day": final_entry_date_data,
    }
    return data


def _transform_other_data(b_day: list, entry_day: list, year: int) -> dict:
    validation.must_positive_int(year, max_length=4)

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

    final_b_day_data = sorted(final_b_day_data, key=lambda x: [x["year"], x["date"][-3:-1], x["date"][:2]])
    final_entry_day_data = sorted(final_entry_day_data, key=lambda x: [x["year"], x["date"][-3:-1], x["date"][:2]])

    data: dict = {
        "b_day": final_b_day_data,
        "entry_day": final_entry_day_data,
    }

    return data

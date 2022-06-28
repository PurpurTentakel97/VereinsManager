# Purpur Tentakel
# 09.05.2022
# VereinsManager / Schedule Day Handler

import sys
import locale
from datetime import datetime, timedelta

from logic.sqlite import add_handler as a_h, select_handler as s_h, update_handler as u_h, delete_handler as d_h
from logic.main_handler import schedule_entry_handler
from helpers import validation, helper
from config import exception_sheet as e, config_sheet as c
import debug

locale.setlocale(locale.LC_ALL, '')

debug_str: str = "Schedule Day Handler"

last_ID: int = 0


def _add_schedule_day(data: dict) -> int:
    return a_h.add_handler.add_schedule_day(data=data)


def get_schedule_day_dates(active: bool = True) -> tuple[str | list, bool]:
    try:
        validation.must_bool(bool_=active)

        ret_data: list = list()
        data = s_h.select_handler.get_all_schedule_day_dates(active=active)
        today: int = int(datetime.timestamp(datetime.today() - timedelta(days=5)))
        for ID, timestamp in data:
            if today > timestamp:
                continue
            date = helper.transform_timestamp_to_datetime(timestamp=timestamp)
            day = f"{datetime.strftime(date, '%A')}, {datetime.strftime(date, c.config.date_format.short)}"
            ret_data.append((ID, day, None))
        return ret_data, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_schedule_day_dates", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_schedule_day_dates", error_=sys.exc_info())
        return error.message, False


def get_schedule_day_by_ID(ID: int, active: bool = True) -> tuple[str | dict, bool]:
    try:
        validation.must_bool(bool_=active)
        validation.must_positive_int(int_=ID, max_length=None)

        data = s_h.select_handler.get_schedule_day_by_ID(ID=ID, active=active)
        ret_data = transform_schedule_day_data_to_dict(data=data)
        global last_ID
        last_ID = ID
        return ret_data, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_schedule_day_by_ID", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_schedule_day_by_ID", error_=sys.exc_info())
        return error.message, False


def update_schedule_day_activity(ID: int, active: bool) -> tuple[None | str, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)
        validation.must_bool(bool_=active)

        u_h.update_handler.update_schedule_day_activity(ID=ID, active=active)
        return None, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"update_schedule_day_activity", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"update_schedule_day_activity", error_=sys.exc_info())
        return error.message, False


def _update_schedule_day(data: dict) -> None:
    return u_h.update_handler.update_schedule_day(data=data)


def save_schedule_day(data: dict) -> tuple[str | int | None, bool]:
    try:
        validation.check_save_schedule_day(data=data)

        if data['ID']:
            result = _update_schedule_day(data=data)
        else:
            result = _add_schedule_day(data=data)

        return result, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"save_schedule_day", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"save_schedule_day", error_=sys.exc_info())
        return error.message, False


def delete_schedule_day(ID: int) -> tuple[None | str, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)

        entries, valid = schedule_entry_handler.get_schedule_entry_IDs_by_day_id(day_id=ID)
        if not valid:
            return entries, valid

        for entry_id in entries:
            d_h.delete_handler.delete_schedule_entry(ID=entry_id[0])

        d_h.delete_handler.delete_schedule_day(ID=ID)

        return None, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"delete_schedule_day", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"delete_schedule_day", error_=sys.exc_info())
        return error.message, False


def transform_schedule_day_data_to_dict(data: tuple) -> dict:
    return {
        "ID": data[0],
        "date": data[1],
        "hour": data[2],
        "minute": data[3],
        "location": data[4],
        "uniform": data[5],
        "comment": data[6],
    }

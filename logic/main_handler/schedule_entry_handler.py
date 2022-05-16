# Purpur Tentakel
# 15.05.2022
# VereinsManager / Schedule Entry Handler

import sys

from helpers import validation
from logic.main_handler import schedule_day_handler
from logic.sqlite import add_handler as a_h, select_handler as s_h, update_handler as u_h
from config import exception_sheet as e
import debug

debug_str: str = "Schedule Entry Handler"


def get_all_schedule_day_names(active: bool) -> tuple[str | list, bool]:
    try:
        validation.must_bool(bool_=active)

        return s_h.select_handler.get_all_schedule_entry_names(active=active, day_id=schedule_day_handler.last_ID), True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_al_schedule_day_names", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_al_schedule_day_names", error_=sys.exc_info())
        return error.message, False


def get_schedule_day_by_ID(ID: int, active: bool) -> tuple[str | dict, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)
        validation.must_bool(bool_=active)

        data = s_h.select_handler.get_schedule_entry_by_ID(ID=ID, active=active)
        data = _transform_for_load_schedule_entry(data=data)
        return data, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_schedule_day_by_ID", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_schedule_day_by_ID", error_=sys.exc_info())
        return error.message, False


def _add_schedule_day(data: dict) -> int:
    return a_h.add_handler.add_schedule_entry(data=data, day_id=schedule_day_handler.last_ID)


def update_schedule_day_activity(ID: int, active: bool) -> tuple[str | None, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)
        validation.must_bool(bool_=active)

        u_h.update_handler.update_schedule_entry_activity(ID=ID, active=active)
        return None, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"update_schedule_day_activity", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"update_schedule_day_activity", error_=sys.exc_info())
        return error.message, False


def _update_schedule_day(data: dict) -> None:
    u_h.update_handler.update_schedule_entry(data=data)


def save_schedule_day(data: dict) -> tuple[int | str, bool]:
    try:
        validation.check_save_schedule_entry(data=data)

        if data['ID']:
            result = _update_schedule_day(data=data)
        else:
            result = _add_schedule_day(data=data)

        return result, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"save_schedule_day", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"Schedule Entry Handler", error_=sys.exc_info())
        return error.message, False


def _transform_for_load_schedule_entry(data: tuple) -> dict:
    return {
        "ID": data[0],
        "day": data[1],
        "title": data[2],
        "hour": data[3],
        "minute": data[4],
        "entry_type": data[5],
        "location": data[6],
        "comment": data[7],
    }

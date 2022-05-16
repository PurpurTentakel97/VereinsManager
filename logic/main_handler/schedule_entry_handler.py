# Purpur Tentakel
# 15.05.2022
# VereinsManager / Schedule Entry Handler

import sys

from helpers import validation
from logic.main_handler import schedule_day_handler
from logic.sqlite import add_handler as a_h
from config import exception_sheet as e
import debug

debug_str: str = "Schedule Entry Handler"


def _add_schedule_day(data: dict) -> int:
    return a_h.add_handler.add_schedule_entry(data=data, day_id=schedule_day_handler.last_ID)


def _update_schedule_day(data: dict) -> None:
    pass


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

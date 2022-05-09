# Purpur Tentakel
# 09.05.2022
# VereinsManager / Schedule Day Handler

import sys

from logic.sqlite import add_handler as a_h
from helpers import validation
from config import exception_sheet as e
import debug

debug_str: str = "Schedule Day Handler"


def _add_schedule_day(data: dict) -> int:
    return a_h.add_handler.add_schedule_day(data=data)


def _update_schedule_day(data: dict) -> None:
    pass


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
    return "pass", False

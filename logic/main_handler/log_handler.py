# Purpur Tentakel
# 13.04.2022
# VereinsManager / Log Handler

import sys

from logic.data_handler import member_log_data_handler
from helper import validation as v
from config import exception_sheet as e
import debug

debug_str: str = "Log Handler"


def get_single_member_log(target_id: int) -> tuple[list | str, bool]:
    try:
        v.must_positive_int(int_=target_id, max_length=None)
        return member_log_data_handler.get_log_member_data(target_id=target_id), True
    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_single_member_log", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_single_member_log", error_=sys.exc_info())
        return error.message, False

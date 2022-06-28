# Purpur Tentakel
# 21.03.2022
# VereinsManager / Global Handler

import datetime

from helpers import helper
from config import config_sheet as c
from logic.main_handler import user_handler, member_handler
import debug

debug_str: str = "Global Handler"


def get_is_delete_bool(updated: int) -> bool:
    now: datetime.datetime = datetime.datetime.now()

    updated: datetime.datetime = helper.transform_timestamp_to_datetime(timestamp=updated)
    days: int = (now - updated).days
    if days > (c.config.date_format.delete_years * 365):
        return True

    return False


def is_delete_inactive_data() -> bool:
    is_delete: bool = False

    functions: tuple = (
        member_handler.get_all_member_IDs_and_updated,
        user_handler.get_all_user_IDs_and_updated
    )
    for function_ in functions:
        data, valid = function_(active=False)
        for ID, updated in data:
            if get_is_delete_bool(updated=updated):
                is_delete = True
                break

        if is_delete:
            break

    return is_delete

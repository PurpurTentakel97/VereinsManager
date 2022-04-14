# Purpur Tentakel
# 13.04.2022
# VereinsManager / Log Handler

import sys
import datetime

from helper import validation
from config import exception_sheet as e
from logic.sqlite import select_handler as s_h
from logic.data_handler import member_log_data_handler
from logic.main_handler import type_handler
import debug

debug_str: str = "Log Handler"


def get_single_member_log(target_id: int) -> tuple[list | str, bool]:
    try:
        validation.must_positive_int(int_=target_id, max_length=None)
        return member_log_data_handler.get_log_member_data(target_id=target_id), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_single_member_log", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_single_member_log", error_=sys.exc_info())
        return error.message, False


def get_log_by_ID(ID: int) -> tuple[dict | str, bool]:
    try:
        data = s_h.select_handler.get_log_by_ID(ID=ID)
        data = _transform_single_entry(data=data)
        return data, True

    except e.OperationalError as error:
        debug.info(item=debug_str, keyword=f"get_log_by_ID", error_=sys.exc_info())
        return error.message, False


# helper
def _transform_single_entry(data: tuple) -> dict:
    data = _transform_to_dict(data=data)
    match data['target_column']:
        case 'active':
            data['old_data'] = _transform_bool(entry=data['old_data'])
            data['new_data'] = _transform_bool(entry=data['new_data'])
        case 'membership_type':
            data['old_data'] = _transform_membership_type(entry=data['old_data'])
            data['new_data'] = _transform_membership_type(entry=data['new_data'])
    data['log_date'] = _transform_timestamp(timestamp=data['log_date'])
    return data


def _transform_to_dict(data: tuple) -> dict:
    return {
        'ID': data[0],
        'target_table': data[3],
        'target_id': data[4],
        'target_column': data[5],
        'old_data': data[6],
        'new_data': data[7],
        'log_date': data[8],
        'display_name': None,  # Allocation in other transform funktion
    }


def _transform_bool(entry: int) -> bool:
    return entry == 1


def _transform_membership_type(entry: int) -> str:
    type_, _ = type_handler.get_type_name_by_ID(ID=entry)
    return type_[0]


def _transform_timestamp(timestamp: int) -> datetime.datetime:
    if timestamp:
        return datetime.datetime(1970, 1, 1, 1, 0, 0) + datetime.timedelta(seconds=timestamp)

# Purpur Tentakel
# 02.05.2022
# VereinsManager / Location Handler

import sys

from helpers import validation
from config import exception_sheet as e, config_sheet as c
from logic.sqlite import add_handler as a_h, select_handler as s_h, update_handler as u_h
import debug

debug_str: str = "Location Handler"


def _add_location(data: dict) -> int:
    return a_h.add_handler.add_location(data=data)


def get_all_location_names(active: bool = True) -> tuple[list | str, bool]:
    try:
        validation.must_bool(bool_=active)

        data = s_h.select_handler.get_all_location_names(active=active)

        new_data: list = list()
        for ID, name in data:
            new_data.append((
                ID,
                name,
                None,
            ))

        return new_data, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_all_location_names", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_all_location_names", error_=sys.exc_info())
        return error.message, False


def _update_location(data: dict) -> None:
    return u_h.update_handler.update_location(data=data)


def save_location(data: dict) -> tuple[str | int | None, bool]:
    try:
        validation.check_save_location(data=data)

        data['country'] = _transform_country_to_ID(country=data['country'])

        if data['ID'] is None:
            return _add_location(data=data), True

        return _update_location(data=data), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"save_location", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"save_location", error_=sys.exc_info())
        return error.message, False


def _transform_country_to_ID(country: str) -> int:
    return s_h.select_handler.get_id_by_type_name(raw_id=c.config.raw_type_id['country'], name=country)[0]

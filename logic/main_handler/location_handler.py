# Purpur Tentakel
# 02.05.2022
# VereinsManager / Location Handler

import sys

from helpers import validation
from config import exception_sheet as e, config_sheet as c
from logic.sqlite import add_handler as a_h, select_handler as s_h, update_handler as u_h, delete_handler as d_h
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


def get_single_location_by_ID(ID: int, active: bool = True) -> tuple[list or str, bool]:
    try:
        data = s_h.select_handler.get_location_by_ID(ID=ID, active=active)
        data = _transform_to_dict(data=data)
        data['country'] = _transform_ID_to_country(ID=data['country'])

        return data, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_single_location_by_ID", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_single_location_by_ID", error_=sys.exc_info())
        return error.message, False


def update_location_activity(ID: int, active: bool) -> tuple[None | str, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)
        validation.must_bool(bool_=active)

        u_h.update_handler.update_location_activity(ID=ID, active=active)
        return None, True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"update_location_activity", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"update_location_activity", error_=sys.exc_info())
        return error.message, False


def _update_location(data: dict) -> None:
    return u_h.update_handler.update_location(data=data)


def delete_location(ID: int) -> tuple[None or str, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)

        d_h.delete_handler.delete_location(ID=ID)
        return None,True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="delete_location", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword="delete_location", error_=sys.exc_info())
        return error.message, False


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
    return s_h.select_handler.get_id_by_type_name(raw_id=c.config.raw_type_id.country, name=country)[0]


def _transform_ID_to_country(ID: int) -> str:
    return s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=ID)[0]


def _transform_to_dict(data: tuple) -> dict:
    return {
        "owner": data[0],
        "name": data[1],
        "street": data[2],
        "number": data[3],
        "zip_code": data[4],
        "city": data[5],
        "country": data[6],
        "maps_link": data[7],
        "comment": data[8],
    }

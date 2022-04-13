# Purpur Tentakel
# 08.04.2022
# VereinsManager / Organisation Handler

import sys

from helper import validation
from config import config_sheet as c, exception_sheet as e
from logic.sqlite import select_handler as s_h, update_handler as u_h, add_handler as a_h
import debug

debug_str: str = "Organisation Handler"


# get
def get_organisation_data() -> tuple[dict | str, bool]:
    try:
        data = s_h.select_handler.get_organisation_data()
        if not data:
            return "Keine Daten vorhanden", False
        data = _transform_data_for_load(data=data)
        return data, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"get_organisation_data", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_organisation_data", error_=sys.exc_info())
        return error.message, False


# add
def _add_organisation(data: dict, log_date: int) -> int:
    return a_h.add_handler.add_organisation(data=data, log_date=log_date)


# add / update
def add_update_organisation(data: dict, log_date: int = None) -> tuple[int | str, bool]:
    try:
        validation.check_add_update_organisation(data=data)
        validation.must_default_user(c.config.user['ID'], False)

        if data['ID'] is None:
            data['ID'] = _add_organisation(data=data, log_date=log_date)
        else:
            _update_organisation(data=data)

        return data['ID'], True

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"add_update_organisation", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"add_update_organisation", error_=sys.exc_info())
        return error.message, False


# update
def _update_organisation(data: dict) -> None:
    u_h.update_handler.update_organisation(data=data)


# helper
def _transform_data_for_load(data: tuple) -> dict:
    data_dict: dict = {
        'ID': data[0],
        'name': data[1],
        'street': data[2],
        'number': data[3],
        'zip_code': data[4],
        'city': data[5],
        'country': data[6],
        'bank_name': data[7],
        'bank_owner': data[8],
        'bank_IBAN': data[9],
        'bank_BIC': data[10],
        'contact_person': data[11],
        'web_link': data[12],
        'extra_text': data[13],
    }
    data_dict['contact_person'] = s_h.select_handler.get_name_of_user_by_ID(ID=data_dict['contact_person'])
    return data_dict

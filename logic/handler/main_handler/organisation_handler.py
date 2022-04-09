# Purpur Tentakel
# 08.04.2022
# VereinsManager / Organisation Handler

import sys

from sqlite import add_handler as a_h, select_handler as s_h
from config import config_sheet as c, exception_sheet as e
from helper import validation as v
import debug

debug_str: str = "Organisation Handler"


# get
def get_organisation_data() -> [tuple | str, bool]:
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


# update
def add_update_organisation(data: dict, log_date: int = None) -> [int | str, bool]:
    try:
        v.must_dict(dict_=data)
        v.must_organisation(data=data)
        v.must_default_user(c.config.user['ID'], False)

        if data['ID'] is None:
            data['ID'] = _add_organisation(data=data, log_date=log_date)
        else:
            pass

        return data['ID'], True

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"add_update_organisation", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"add_update_organisation", error_=sys.exc_info())
        return error.message, False


# helper
def _transform_data_for_load(data: tuple) -> dict:
    debug.debug(item=debug_str, keyword="_transform_data_for_load", message=f"data = {data}")
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
    data = s_h.select_handler.get_name_of_user_by_ID(ID=data_dict['contact_person'])
    debug.debug(item=debug_str, keyword="_transform_data_for_load", message=f"data = {data}")
    data_dict['contact_person'] = data
    return data_dict

# Purpur Tentakel
# 08.04.2022
# VereinsManager / Organisation Handler

import sys

from sqlite import add_handler as a_h
from config import config_sheet as c, exception_sheet as e
from helper import validation as v
import debug

debug_str: str = "Organisation Handler"


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

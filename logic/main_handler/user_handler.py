# Purpur Tentakel
# 21.03.2022
# VereinsManager / User Handler
import sys

from helper import hasher, validation
from config import exception_sheet as e, config_sheet as c
from logic.sqlite import select_handler as s_h, delete_handler as d_h, update_handler as u_h, add_handler as a_h
import debug

debug_str: str = "User Handler"


# get
def get_names_of_user(active: bool = True) -> [str | tuple, bool]:
    try:
        validation.must_bool(bool_=active)
        return s_h.select_handler.get_names_of_user(active=active), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_names_of_user", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_names_of_user", error_=sys.exc_info())
        return error.message, False


def get_names_of_user_without_default(active: bool = True) -> [str | tuple, bool]:
    data, valid = get_names_of_user(active=active)
    if not valid:
        return data, valid

    index = None
    for entry in data:
        ID, *_ = entry
        if ID == c.config.user['default_user_id']:
            index = data.index(entry)
            break

    if index is not None:
        del data[index]

    return data, True


def get_data_of_user_by_ID(ID: int, active: bool) -> [str | dict, bool]:
    try:
        validation.must_positive_int(int_=ID)
        validation.must_bool(bool_=active)

        data = s_h.select_handler.get_data_of_user_by_ID(ID=ID, active=active)
        data_: dict = {
            "ID": data[0],
            "firstname": data[1],
            "lastname": data[2],
            "street": data[3],
            "number": data[4],
            "zip_code": data[5],
            "city": data[6],
            "country": data[7],
            "phone": data[8],
            "mail": data[9],
            "position": data[10],
        }
        return data_, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_data_of_user_by_ID", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_data_of_user_by_ID", error_=sys.exc_info())
        return error.message, False


def get_hashed_password_by_ID(ID: int) -> bytes:
    try:
        validation.must_positive_int(int_=ID)

        hashed = s_h.select_handler.get_hashed_password_by_ID(ID=ID)

        return hashed
    except e.OperationalError:
        debug.error(item=debug_str, keyword="get_hashed_password_by_ID", error_=sys.exc_info())


# add / update
def add_update_user(data: dict) -> [str | int | None, bool]:
    try:
        validation.check_add_update_user(data=data)

        if not data["ID"]:
            data["password_hashed"] = hasher.hash_password(data["password_1"])
            return a_h.add_handler.add_user(data=data), True

        u_h.update_handler.update_user(ID=data["ID"], data=data)
        c.config.set_user(ID=c.config.user['ID'])

        if data["password_1"]:
            data["password_hashed"] = hasher.hash_password(data["password_1"])
            u_h.update_handler.update_user_password(ID=data["ID"], password=data["password_hashed"])
        return None, True

    except (e.InputError, e.UserError, e.PasswordError) as error:
        debug.info(item=debug_str, keyword="add_update_user", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="add_update_user", error_=sys.exc_info())
        return error.message, False


# update
def update_user_activity(ID: int, active: bool) -> [str, bool]:
    try:
        validation.must_positive_int(int_=ID)
        validation.must_bool(bool_=active)
        validation.must_current_user(ID=ID, same=not active)
        validation.must_default_user(ID=ID, same=False)
        u_h.update_handler.update_user_activity(ID=ID, active=active)
        return None, True

    except (e.InputError, e.UserError) as error:
        debug.info(item=debug_str, keyword="update_user_activity", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_user_activity", error_=sys.exc_info())
        return error.message, False


# delete
def delete_inactive_user() -> None:
    try:
        reference_data, _ = get_names_of_user(active=False)
        for ID, *_ in reference_data:
            d_h.delete_handler.delete_user(ID=ID)
    except e.OperationalError:
        debug.error(item=debug_str, keyword="delete_inactive_user", error_=sys.exc_info())

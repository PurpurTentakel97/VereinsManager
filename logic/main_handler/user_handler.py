# Purpur Tentakel
# 21.03.2022
# VereinsManager / User Handler

import sys

from helpers import hasher, validation
from config import exception_sheet as e, config_sheet as c
from logic.main_handler import global_handler
from logic.sqlite import select_handler as s_h, delete_handler as d_h, update_handler as u_h, add_handler as a_h
import debug

debug_str: str = "User Handler"


# get
def get_names_of_user(active: bool = True) -> [str | tuple, bool]:
    try:
        validation.must_bool(bool_=active)
        data = s_h.select_handler.get_names_of_user(active=active)
        if not active:
            data = _get_old_bool(data=data)
        return data, True

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


def get_all_user_IDs_and_updated(active: bool) -> tuple[tuple | str, bool]:
    try:
        return s_h.select_handler.get_all_IDs_and_updated_from_user(active=active), True
    except e.OperationalError as error:
        debug.error(item=debug_str, keyword=f"get_all_user_IDs_and_updated", error_=sys.exc_info())
        return error.message, False


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
        validation.check_delete_user(ID=ID, active=active)
        u_h.update_handler.update_user_activity(ID=ID, active=active)
        return None, True

    except (e.InputError, e.UserError) as error:
        debug.info(item=debug_str, keyword="update_user_activity", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_user_activity", error_=sys.exc_info())
        return error.message, False


# delete
def delete_user(ID: int) -> tuple[str, bool]:
    try:
        validation.must_positive_int(int_=ID)

        d_h.delete_handler.delete_user(ID=ID)
        return "", True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="delete_inactive_user", error_=sys.exc_info())
        return error.message, False

    except e.InputError as error:
        debug.info(item=debug_str, keyword=f"delete_user", error_=sys.exc_info())
        return error.message, False


# helper
def _get_old_bool(data: list) -> list:
    reference_data = s_h.select_handler.get_all_IDs_and_updated_from_user(active=False)
    new_data: list = list()

    for ID, firstname, lastname in data:
        for ref_ID, updated in reference_data:

            if not ref_ID == ID:
                continue

            entry: tuple = (
                ID,
                firstname,
                lastname,
                global_handler.get_is_delete_bool(updated=updated)
            )

            new_data.append(entry)
            break

    return new_data

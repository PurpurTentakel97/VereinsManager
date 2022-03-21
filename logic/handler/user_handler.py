# Purpur Tentakel
# 21.03.2022
# VereinsManager / User Handler

from helper import hasher
from logic import validation as v
from config import error_code as e
from sqlite import add_handler as a_h, update_handler as u_h, select_handler as s_h
import debug

debug_str: str = "User Handler"


# get
def get_names_of_user(active: bool = True) -> [tuple | str, bool]:
    try:
        v.validation.must_bool(bool_=active)
    except e.NoBool as error:
        debug.debug(item=debug_str, keyword="get_names_of_user", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_names_of_user(active=active)


def get_data_of_user_by_ID(ID: int, active: bool) -> [dict | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID)
        v.validation.must_bool(bool_=active)
    except (e.NoInt, e.NoPositiveInt, e.NoBool) as error:
        debug.error(item=debug_str, keyword="get_data_of_user", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_data_of_user_by_ID(ID=ID, active=active)


# add / update
def add_update_user(data: dict) -> [int | str | None, bool]:
    try:
        v.validation.save_update_user(data=data)
    except (e.NoDict, e.NoStr, e.NoInt, e.NoPositiveInt, e.DifferentPassword, e.PasswordToShort,
            e.PasswordHasSpace, e.LowPassword, e.VeryLowPassword, e.ToLong, e.DefaultUserException,
            e.CurrentUserException) as error:
        debug.error(item=debug_str, keyword="save_update_user", message=f"Error = {error.message}")
        return error.message, False

    if not data["ID"]:
        data["password_hashed"] = hasher.hash_password(data["password_1"])
        return a_h.add_handler.add_user(data=data)

    result, valid = u_h.update_handler.update_user(ID=data["ID"], data=data)
    if not valid:
        return result, False

    if data["password_1"]:
        data["password_hashed"] = hasher.hash_password(data["password_1"])
        return u_h.update_handler.update_user_password(ID=data["ID"], password=data["password_hashed"])

    return None, True


# update
def update_user_activity(ID: int, active: bool) -> [str, bool]:
    try:
        v.validation.must_positive_int(int_=ID)
        v.validation.must_bool(bool_=active)
        v.validation.must_current_user(ID=ID, same=False)
        v.validation.must_default_user(ID=ID, same=False)
    except (e.NoInt, e.NoPositiveInt, e.NoBool, e.CurrentUserException, e.DefaultUserException) as error:
        debug.error(item=debug_str, keyword="update_user_activity", message=f"Error = {error.message}")
        return error.message, False

    return u_h.update_handler.update_user_activity(ID=ID, active=active)

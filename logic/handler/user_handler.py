# Purpur Tentakel
# 21.03.2022
# VereinsManager / User Handler

from helper import hasher
from logic import validation as v
from config import exception_sheet as e
from sqlite import add_handler as a_h, update_handler as u_h, select_handler as s_h
import debug

debug_str: str = "User Handler"


# get
def get_names_of_user(active: bool = True) -> tuple:
    v.validation.must_bool(bool_=active)

    return s_h.select_handler.get_names_of_user(active=active)


def get_data_of_user_by_ID(ID: int, active: bool) -> dict:
    v.validation.must_positive_int(int_=ID)
    v.validation.must_bool(bool_=active)

    return s_h.select_handler.get_data_of_user_by_ID(ID=ID, active=active)


# add / update
def add_update_user(data: dict) -> int | None:
    v.validation.save_update_user(data=data)

    if not data["ID"]:
        data["password_hashed"] = hasher.hash_password(data["password_1"])
        return a_h.add_handler.add_user(data=data)

    u_h.update_handler.update_user(ID=data["ID"], data=data)

    if data["password_1"]:
        data["password_hashed"] = hasher.hash_password(data["password_1"])
        u_h.update_handler.update_user_password(ID=data["ID"], password=data["password_hashed"])


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

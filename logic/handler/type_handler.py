# Purpur Tentakel
# 21.03.2022
# VereinsManager / Type Handler

from logic import validation as v
from config import exception_sheet as e, config_sheet as c
from sqlite import add_handler as a_h, delete_handler as d_h, select_handler as s_h, update_handler as u_h, \
    log_handler as l_h
import debug

debug_str: str = "Type Handler"


# add
def add_type(type_name: str, raw_type_id: int) -> [str | int, bool]:
    try:
        v.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
        v.validation.must_default_user(c.config.user_id, False)
        type_name = type_name.strip().title()
    except (e.NoStr, e.NoInt, e.NoPositiveInt, e.ToLong, e.AlreadyExists, e.DefaultUserException) as error:
        debug.error(item=debug_str, keyword="add_type", message=f"Error = {error.message}")
        return error.message, False

    return a_h.add_handler.add_type(type_name=type_name, raw_type_id=raw_type_id)


# get
def get_raw_types() -> [tuple | str, bool]:
    return s_h.select_handler.get_raw_types()


def get_all_single_type() -> [tuple | str, bool]:
    s_h.select_handler.get_all_single_type()


def get_single_raw_type_types(raw_type_id: int, active: bool = True) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=raw_type_id)
        v.validation.must_bool(bool_=active)
    except (e.NoBool, e.NoPositiveInt) as error:
        debug.error(item=debug_str, keyword="get_single_raw_type_types", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active)


def get_active_member_type() -> [tuple | str, bool]:
    return s_h.select_handler.get_active_member_type()


def get_type_name_by_ID(ID: int) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_type_name_by_ID(ID=ID)


def get_type_active_by_id(ID: int) -> [tuple or str, bool]:
    try:
        v.validation.must_positive_int(int_=ID, max_length=None)
    except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_type_active_by_id(ID=ID)


def get_id_by_type_name(raw_id: int, name: str) -> [tuple | str, bool]:
    try:
        v.validation.must_positive_int(int_=raw_id, max_length=None)
        v.validation.must_str(str_=name)
    except (e.NoInt, e.NoPositiveInt, e.NoStr, e.ToLong) as error:
        debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"Error = {error.message}")
        return error.message, False

    return s_h.select_handler.get_id_by_type_name(raw_id=raw_id, name=name)


# update
def update_type(ID: int, name: str) -> [str | None, bool]:
    try:
        v.validation.update_type(ID=ID, new_name=name)
        v.validation.must_default_user(c.config.user_id, False)
        name = name.strip().title()
    except (e.NoStr, e.NoInt, e.NoPositiveInt, e.NoChance, e.NotFound, e.ToLong, e.DefaultUserException) as error:
        debug.error(item=debug_str, keyword="update_type", message=f"Error = {error.message}")
        return error.message, False

    reference_data, valid = s_h.select_handler.get_type_name_by_ID(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_type(ID=ID, name=name)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0],
                                             new_data=name)
    if not valid:
        return result, False

    return None, True


def update_type_activity(ID: int, active: bool = True) -> [str | None, bool]:
    try:
        v.validation.update_type_activity(ID=ID, active=active)
        v.validation.must_default_user(c.config.user_id, False)
    except (e.NoStr, e.NoPositiveInt, e.NoChance, e.NotFound, e.ToLong, e.DefaultUserException) as error:
        debug.error(item=debug_str, keyword="update_type_activity", message=f"Error = {error.message}")
        return error.message, False

    reference_data, valid = s_h.select_handler.get_type_active_by_id(ID=ID)
    if not valid:
        return reference_data, False

    result, valid = u_h.update_handler.update_type_activity(ID=ID, active=active)
    if not valid:
        return result, False

    result, valid = l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0],
                                             new_data=active)
    if not valid:
        return result, False

    return None, True


# delete
def delete_type(ID: int) -> [str | None, bool]:
    try:
        v.validation.must_positive_int(ID, max_length=None)
        v.validation.must_default_user(c.config.user_id, False)
    except (e.NoInt, e.NoPositiveInt, e.ToLong, e.DefaultUserException) as error:
        debug.error(item=debug_str, keyword="delete_type", message=f"Error = {error.message}")
        return error.message, False

    return d_h.delete_handler.delete_type(ID=ID)

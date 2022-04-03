# Purpur Tentakel
# 21.03.2022
# VereinsManager / Type Handler

from logic import validation as v
from config import config_sheet as c, exception_sheet as e
from sqlite import add_handler as a_h, delete_handler as d_h, select_handler as s_h, update_handler as u_h, \
    log_handler as l_h
import debug

debug_str: str = "Type Handler"


# add
def add_type(type_name: str, raw_type_id: int) -> [str | int, bool]:
    try:
        v.add_type(type_name=type_name, raw_type_id=raw_type_id)
        v.must_default_user(c.config.user['ID'], False)

        return a_h.add_handler.add_type(type_name=type_name.strip().title(), raw_type_id=raw_type_id), True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="add_type", message=f"Error = {error}")
        return error.message, False


# get
def get_raw_types() -> [str | tuple, bool]:
    try:
        return s_h.select_handler.get_raw_types(), True
    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_raw_types", message=f"Error = {error.message}")
        return error.message, False


def get_single_raw_type_types(raw_type_id: int, active: bool = True) -> [str | tuple, bool]:
    try:
        v.must_positive_int(int_=raw_type_id)
        v.must_bool(bool_=active)

        return s_h.select_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active), True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="get_single_raw_type_types", message=f"Error = {error.message}")
        return error.message, False


def get_active_member_type() -> [str | tuple, bool]:
    try:
        return s_h.select_handler.get_active_member_type(), True
    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_active_member_type", message=f"Error = {error.message}")
        return error.message, False


def get_type_name_by_ID(ID: int) -> [str | tuple, bool]:
    try:
        v.must_positive_int(int_=ID, max_length=None)

        return s_h.select_handler.get_type_name_by_ID(ID=ID), True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="get_type_name_by_ID", message=f"Error = {error.message}")
        return error.message, False


# update
def update_type(ID: int, name: str) -> [str | None, bool]:
    try:
        v.update_type(ID=ID, new_name=name)
        v.must_default_user(c.config.user['ID'], False)

        name = name.strip().title()

        reference_data = s_h.select_handler.get_type_name_by_ID(ID=ID)
        u_h.update_handler.update_type(ID=ID, name=name)
        l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0], new_data=name)
        return None, True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="update_type", message=f"Error = {error.message}")
        return error.message, False


def update_type_activity(ID: int, active: bool = True) -> [str | None, bool]:
    try:
        v.update_type_activity(ID=ID, active=active)
        v.must_default_user(c.config.user['ID'], False)

        reference_data = s_h.select_handler.get_type_active_by_id(ID=ID)
        u_h.update_handler.update_type_activity(ID=ID, active=active)
        l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0], new_data=active)
        return None, True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="update_type_activity", message=f"Error = {error.message}")
        return error.message, False


# delete
def delete_type(ID: int) -> [str | None, bool]:
    try:
        v.must_positive_int(ID, max_length=None)
        v.must_default_user(c.config.user['ID'], False)

        d_h.delete_handler.delete_type(ID=ID)
        return None, True
    except (e.OperationalError, e.InputError) as error:
        debug.error(item=debug_str, keyword="delete_type", message=f"Error = {error.message}")
        return error.message, False

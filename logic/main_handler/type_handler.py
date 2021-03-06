# Purpur Tentakel
# 21.03.2022
# VereinsManager / Type Handler
import sys

from helpers import validation
from config import config_sheet as c, exception_sheet as e
from logic.sqlite import select_handler as s_h, delete_handler as d_h, log_handler as l_h, update_handler as u_h, \
    add_handler as a_h
import debug

debug_str: str = "Type Handler"


# add
def add_type(type_name: str, raw_type_id: int, extra_value: str) -> tuple[str | int, bool]:
    try:
        validation.check_add_type(type_name=type_name, raw_type_id=raw_type_id, extra_value=extra_value)
        validation.must_default_user(c.config.user.ID, False)

        return a_h.add_handler.add_type(type_name=type_name.strip().title(), raw_type_id=raw_type_id,
                                        extra_value=extra_value), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="add_type", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="add_type", error_=sys.exc_info())
        return error.message, False


# get
def get_raw_types() -> tuple[str | tuple, bool]:
    try:
        return s_h.select_handler.get_raw_types(), True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_raw_types", error_=sys.exc_info())
        return error.message, False


def get_single_raw_type_types(raw_type_id: int, active: bool = True) -> tuple[str | tuple, bool]:
    try:
        validation.must_positive_int(int_=raw_type_id)
        validation.must_bool(bool_=active)

        return s_h.select_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_single_raw_type_types", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_single_raw_type_types", error_=sys.exc_info())
        return error.message, False


def get_active_member_type() -> tuple[str | tuple, bool]:
    try:
        return s_h.select_handler.get_active_member_type(), True

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_active_member_type", error_=sys.exc_info())
        return error.message, False


def get_type_name_by_ID(ID: int) -> tuple[str | tuple, bool]:
    try:
        validation.must_positive_int(int_=ID, max_length=None)

        return s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=ID), True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="get_type_name_by_ID", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="get_type_name_by_ID", error_=sys.exc_info())
        return error.message, False


# update
def update_type(ID: int, name: str, extra_value: str) -> tuple[str | None, bool]:
    try:
        validation.check_update_type(ID=ID, new_name=name, new_extra_value=extra_value)
        validation.must_default_user(c.config.user.ID, False)

        name = name.strip().title()

        reference_data = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=ID)
        u_h.update_handler.update_type(ID=ID, name=name, extra_value=extra_value)
        l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0], new_data=name)
        l_h.log_handler.log_type(target_id=ID, target_column="extra_value", old_data=reference_data[1],
                                 new_data=extra_value)
        return None, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="update_type", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_type", error_=sys.exc_info())
        return error.message, False


def update_type_activity(ID: int, active: bool = True) -> tuple[str | None, bool]:
    try:
        validation.check_update_type_activity(ID=ID, active=active)
        validation.must_default_user(c.config.user.ID, False)

        reference_data = s_h.select_handler.get_type_active_by_id(ID=ID)
        u_h.update_handler.update_type_activity(ID=ID, active=active)
        l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0], new_data=active)
        return None, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="update_type_activity", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="update_type_activity", error_=sys.exc_info())
        return error.message, False


# delete
def delete_type(ID: int) -> tuple[str | None, bool]:
    try:
        validation.must_positive_int(ID, max_length=None)
        validation.must_default_user(c.config.user.ID, False)

        d_h.delete_handler.delete_type(ID=ID)
        return None, True

    except e.InputError as error:
        debug.info(item=debug_str, keyword="delete_type", error_=sys.exc_info())
        return error.message, False

    except e.OperationalError as error:
        debug.error(item=debug_str, keyword="delete_type", error_=sys.exc_info())
        return error.message, False

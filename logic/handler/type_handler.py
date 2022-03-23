# Purpur Tentakel
# 21.03.2022
# VereinsManager / Type Handler

from logic import validation as v
from config import config_sheet as c
from sqlite import add_handler as a_h, delete_handler as d_h, select_handler as s_h, update_handler as u_h, \
    log_handler as l_h
import debug

debug_str: str = "Type Handler"


# add
def add_type(type_name: str, raw_type_id: int) -> int:
    v.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
    v.validation.must_default_user(c.config.user_id, False)

    return a_h.add_handler.add_type(type_name=type_name.strip().title(), raw_type_id=raw_type_id)


# get
def get_raw_types() -> tuple:
    return s_h.select_handler.get_raw_types()


def get_all_single_type() -> tuple:
    return s_h.select_handler.get_all_single_type()


def get_single_raw_type_types(raw_type_id: int, active: bool = True) -> tuple:
    v.validation.must_positive_int(int_=raw_type_id)
    v.validation.must_bool(bool_=active)

    return s_h.select_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active)


def get_active_member_type() -> tuple:
    return s_h.select_handler.get_active_member_type()


def get_type_name_by_ID(ID: int) -> tuple:
    v.validation.must_positive_int(int_=ID, max_length=None)

    return s_h.select_handler.get_type_name_by_ID(ID=ID)


def get_type_active_by_id(ID: int) -> tuple:
    v.validation.must_positive_int(int_=ID, max_length=None)

    return s_h.select_handler.get_type_active_by_id(ID=ID)


def get_id_by_type_name(raw_id: int, name: str) -> tuple:
    v.validation.must_positive_int(int_=raw_id, max_length=None)
    v.validation.must_str(str_=name)

    return s_h.select_handler.get_id_by_type_name(raw_id=raw_id, name=name)


# update
def update_type(ID: int, name: str) -> None:
    v.validation.update_type(ID=ID, new_name=name)
    v.validation.must_default_user(c.config.user_id, False)

    name = name.strip().title()

    reference_data = s_h.select_handler.get_type_name_by_ID(ID=ID)
    u_h.update_handler.update_type(ID=ID, name=name)
    l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0], new_data=name)


def update_type_activity(ID: int, active: bool = True) -> None:
    v.validation.update_type_activity(ID=ID, active=active)
    v.validation.must_default_user(c.config.user_id, False)

    reference_data = s_h.select_handler.get_type_active_by_id(ID=ID)
    u_h.update_handler.update_type_activity(ID=ID, active=active)
    l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0], new_data=active)


# delete
def delete_type(ID: int) -> None:
    v.validation.must_positive_int(ID, max_length=None)
    v.validation.must_default_user(c.config.user_id, False)

    d_h.delete_handler.delete_type(ID=ID)

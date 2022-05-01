# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

import sys

from helpers import password_validation
from config import exception_sheet as e
from logic.data_handler import member_table_data_handler, member_anniversary_data_handler
from logic.main_handler import user_handler, type_handler, path_handler, member_handler, \
    organisation_handler, log_handler
from logic.pdf_handler import global_pdf_handler, member_table_pdf as m_t_p, member_card_pdf as m_c_p, \
    member_anniversary_pdf as m_a_p, member_log_pdf as m_l_p, member_entry_letter_pfd as m_e_l_p

import debug

debug_str: str = "Transition"


# global
def create_default_dir(type_) -> None:
    try:
        path_handler.create_default_path(type_)
    except:
        handle_error()


def compare_password(ID: int, password: str) -> [str | bool, bool]:
    try:
        return password_validation.check_user_password(ID=ID, password=password)
    except:
        handle_error()


# type
def get_raw_types() -> [tuple | str, bool]:
    try:
        return type_handler.get_raw_types()
    except:
        handle_error()


def get_single_type(raw_type_id: int, active: bool) -> [tuple | str, bool]:
    try:
        return type_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active)
    except:
        handle_error()


def get_active_member_type() -> [tuple | str, bool]:
    try:
        return type_handler.get_active_member_type()
    except:
        handle_error()


def get_type_name_by_ID(ID: int) -> [tuple | str, bool]:
    try:
        return type_handler.get_type_name_by_ID(ID=ID)
    except:
        handle_error()


def add_type(type_name: str, raw_type_id: int, extra_value) -> [str | None, bool]:
    try:
        return type_handler.add_type(type_name=type_name, raw_type_id=raw_type_id, extra_value=extra_value)
    except:
        handle_error()


def update_type(id_: int, name: str, extra_value: str) -> [str | None, bool]:
    try:
        return type_handler.update_type(ID=id_, name=name, extra_value=extra_value)
    except:
        handle_error()


def update_type_activity(id_: int, active: bool) -> [str | None, bool]:
    try:
        return type_handler.update_type_activity(ID=id_, active=active)
    except:
        handle_error()


def delete_type(id_: int) -> [str | None, bool]:
    try:
        return type_handler.delete_type(ID=id_)
    except:
        handle_error()


# member
def get_all_member_name(active: bool = True) -> [tuple | str, bool]:
    try:
        return member_handler.get_names_of_member(active=active)
    except:
        handle_error()


def get_anniversary_member_data(type_: str | int, active: bool = True, year: int = 0) -> [dict | str, bool]:
    try:
        return member_anniversary_data_handler.get_anniversary_member_data(active=active, type_=type_, year=year)
    except:
        handle_error()


def get_member_data_by_id(id_: int, active: bool = True) -> [dict | str, bool]:
    try:
        return member_handler.get_member_data(ID=id_, active=active)
    except:
        handle_error()


def get_member_data_for_table(active: bool = True) -> [dict | str, bool]:
    try:
        return member_table_data_handler.get_member_table_data(active=active)
    except:
        handle_error()


def update_member_data(id_: int, data: dict, log_date: int | None = None) -> [str | dict, bool]:
    try:
        return member_handler.add_update_member_data(ID=id_, data=data, log_date=log_date)
    except:
        handle_error()


def update_member_activity(ID: int, active: bool, log_date: int | None = None) -> [str | None, bool]:
    try:
        return member_handler.update_member_activity(ID=ID, active=active, log_date=log_date)
    except:
        handle_error()


def delete_member(ID: int) -> tuple[str, bool]:
    try:
        return member_handler.delete_member(ID=ID)
    except:
        handle_error()


# user
def save_update_user(data: dict) -> [str | int | None, bool]:
    try:
        return user_handler.add_update_user(data=data)
    except:
        handle_error()


def update_user_activity(ID: int, active: bool) -> [str | None, bool]:
    try:
        return user_handler.update_user_activity(ID=ID, active=active)
    except:
        handle_error()


def get_all_user_name(active: bool = True) -> [str | dict, bool]:
    try:
        return user_handler.get_names_of_user(active=active)
    except:
        handle_error()


def get_all_user_name_without_default(active: bool = True) -> [str | dict, bool]:
    try:
        return user_handler.get_names_of_user_without_default(active=active)
    except:
        handle_error()


def get_user_data_by_id(ID: int, active: bool) -> [str | dict, bool]:
    try:
        return user_handler.get_data_of_user_by_ID(ID=ID, active=active)
    except:
        handle_error()


def delete_user(ID: int) -> tuple[str, bool]:
    try:
        return user_handler.delete_user(ID=ID)
    except:
        handle_error()


# pdf_handler
def get_member_table_pdf(path: str, active: bool = True) -> [None | str, bool]:
    try:
        return m_t_p.member_table_pdf.create_pdf(path=path, active=active)
    except:
        handle_error()


def get_member_anniversary_pdf(path: str, year: int or None = None, active: bool = True) -> [None | str, bool]:
    try:
        return m_a_p.member_anniversary_pdf.create_pdf(path=path, year=year, active=active)
    except:
        handle_error()


def get_member_card_pdf(ID: int, path: str, active: bool = True) -> [None | str, bool]:
    try:
        return m_c_p.member_card_pdf.create_pdf(ID=ID, active=active, path=path)
    except:
        handle_error()


def get_member_log_pdf(ID: int, path: str, active: bool) -> tuple[str | None, bool]:
    try:
        return m_l_p.member_log_pdf.create_pdf(path=path, ID=ID, active=active)
    except:
        handle_error()


def get_member_entry_letter_pdf(ID: int, path: str, active: bool, log_id: int) -> tuple[str | None, bool]:
    try:
        return m_e_l_p.member_entry_letter_pdf.create_pdf(ID=ID, path=path, active=active, log_id=log_id)
    except:
        handle_error()


def open_latest_export() -> None:
    try:
        global_pdf_handler.open_last_export()
    except:
        handle_error()


# organisation
def get_organisation_data() -> [tuple | str, bool]:
    try:
        return organisation_handler.get_organisation_data()
    except:
        handle_error()


def add_update_organisation(data: dict) -> [int | str, bool]:
    try:
        return organisation_handler.add_update_organisation(data=data)
    except:
        handle_error()


# log
def get_log_member_data(target_id: int) -> [tuple | str, bool]:
    try:
        return log_handler.get_single_member_log(target_id=target_id)
    except:
        handle_error()


# debug
def handle_error():
    debug.error(item=debug_str, keyword=f"handle_error", error_=sys.exc_info())
    debug.export_error()
    raise e.QuitException()

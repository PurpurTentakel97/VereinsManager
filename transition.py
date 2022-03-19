# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h, \
    global_handler as g_h
from logic import member_table_data_handler, path_handler, member_anniversary_data_handler
from pdf_handler import member_table_pdf as m_t_p, member_anniversary_pdf as m_a_p


# global
def create_default_dir(type_) -> None:
    path_handler.create_default_path(type_)


# type
def get_raw_types() -> tuple | str:
    return s_h.select_handler.get_raw_types()


def get_single_type(raw_type_id: int, active: bool = True) -> tuple | str:
    return s_h.select_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active)


def get_active_member_type() -> tuple | str:
    return s_h.select_handler.get_active_member_type()


def get_type_name_by_ID(ID: int) -> tuple | str:
    return s_h.select_handler.get_type_name_by_ID(ID=ID)


def add_type(type_name: str, raw_type_id: int) -> str | None:
    return a_h.add_handler.add_type(type_name=type_name, raw_type_id=raw_type_id)


def update_type(id_: int, name: str) -> str | None:
    return u_h.update_handler.update_type(ID=id_, name=name)


def update_type_activity(id_: int, active: bool) -> str | None:
    return u_h.update_handler.update_type_activity(ID=id_, active=active)


def delete_type(id_: int) -> str | None:
    return d_h.delete_handler.delete_type(ID=id_)


# member
def get_all_member_name(active: bool = True) -> tuple | str:
    return s_h.select_handler.get_names_of_member(active=active)


def get_anniversary_member_data(type_: str | int, active: bool = True, year: int = 0) -> dict | str:
    return member_anniversary_data_handler.get_anniversary_member_data(active=active, type_=type_, year=year)


def get_member_data_by_id(id_: int, active: bool = True) -> dict | str:
    return g_h.global_handler.get_member_data(ID=id_, active=active)


def get_member_data_for_table(active: bool = True) -> dict | str:
    return member_table_data_handler.get_member_table_data(active=active)


def update_member_data(id_: int, data: dict, log_date: int | None = None) -> str | dict:
    return g_h.global_handler.update_member_data(ID=id_, data=data, log_date=log_date)


def update_member_activity(id_: int, active: bool, log_date: int | None = None) -> str | None:
    return u_h.update_handler.update_member_activity(ID=id_, active=active, log_date=log_date)


# user
def save_update_user(data: dict) -> str | int | None:
    return g_h.global_handler.save_update_user(data=data)


def get_all_user_name(active: bool = True) -> str | dict:
    return s_h.select_handler.get_names_of_user(active=active)


def get_user_data_by_id(ID: int, active: bool = True) -> str | dict:
    return s_h.select_handler.get_data_of_user_by_ID(ID=ID, active=active)


# pdf_handler
def get_member_table_pdf(path: str, active: bool = True) -> None | str:
    return m_t_p.member_table_pdf.create_pdf(path=path, active=active)


def get_member_anniversary_pdf(path: str, year: int or None = None, active: bool = True) -> None or str:
    return m_a_p.member_anniversary_pdf.create_pdf(path=path, year=year, active=active)

# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from logic import password_validation
from logic.handler import path_handler, user_handler, \
    type_handler, member_handler
from logic.handler.data_handler import member_anniversary_data_handler, member_table_data_handler
from logic.handler.pdf_handler import member_table_pdf as m_t_p, global_pdf_handler, member_anniversary_pdf as m_a_p, \
    member_card_pdf as m_c_p


# global
def create_default_dir(type_) -> None:
    path_handler.create_default_path(type_)


def compare_password(ID: int, password: str) -> [str | bool, bool]:
    return password_validation.check_password(ID=ID, password=password)


# type
def get_raw_types() -> [tuple | str, bool]:
    return type_handler.get_raw_types()


def get_single_type(raw_type_id: int, active: bool) -> [tuple | str, bool]:
    return type_handler.get_single_raw_type_types(raw_type_id=raw_type_id, active=active)


def get_active_member_type() -> [tuple | str, bool]:
    return type_handler.get_active_member_type()


def get_type_name_by_ID(ID: int) -> [tuple | str, bool]:
    return type_handler.get_type_name_by_ID(ID=ID)


def add_type(type_name: str, raw_type_id: int) -> [str | None, bool]:
    return type_handler.add_type(type_name=type_name, raw_type_id=raw_type_id)


def update_type(id_: int, name: str) -> [str | None, bool]:
    return type_handler.update_type(ID=id_, name=name)


def update_type_activity(id_: int, active: bool) -> [str | None, bool]:
    return type_handler.update_type_activity(ID=id_, active=active)


def delete_type(id_: int) -> [str | None, bool]:
    return type_handler.delete_type(ID=id_)


# member
def get_all_member_name(active: bool = True) -> [tuple | str, bool]:
    return member_handler.get_names_of_member(active=active)


def get_anniversary_member_data(type_: str | int, active: bool = True, year: int = 0) -> [dict | str, bool]:
    return member_anniversary_data_handler.get_anniversary_member_data(active=active, type_=type_, year=year)


def get_member_data_by_id(id_: int, active: bool = True) -> [dict | str, bool]:
    return member_handler.get_member_data(ID=id_, active=active)


def get_member_data_for_table(active: bool = True) -> [dict | str, bool]:
    return member_table_data_handler.get_member_table_data(active=active)


def update_member_data(id_: int, data: dict, log_date: int | None = None) -> [str | dict, bool]:
    return member_handler.update_member_data(ID=id_, data=data, log_date=log_date)


def update_member_activity(ID: int, active: bool, log_date: int | None = None) -> [str | None, bool]:
    return member_handler.update_member_activity(ID=ID, active=active, log_date=log_date)


# user
def save_update_user(data: dict) -> [str | int | None, bool]:
    return user_handler.add_update_user(data=data)


def update_user_activity(ID: int, active: bool) -> [str | None, bool]:
    return user_handler.update_user_activity(ID=ID, active=active)


def get_all_user_name(active: bool = True) -> [str | dict, bool]:
    return user_handler.get_names_of_user(active=active)


def get_user_data_by_id(ID: int, active: bool) -> [str | dict, bool]:
    return user_handler.get_data_of_user_by_ID(ID=ID, active=active)


# pdf_handler
def get_member_table_pdf(path: str, active: bool = True) -> [None | str, bool]:
    return m_t_p.member_table_pdf.create_pdf(path=path, active=active)


def get_member_anniversary_pdf(path: str, year: int or None = None, active: bool = True) -> [None or str, bool]:
    return m_a_p.member_anniversary_pdf.create_pdf(path=path, year=year, active=active)


def get_member_card_pdf(ID: int, path: str, active: bool = True) -> None:
    m_c_p.member_card_pdf.create_pdf(ID=ID, active=active, path=path)


def open_latest_export() -> None:
    global_pdf_handler.open_last_export()

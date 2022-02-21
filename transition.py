# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h, \
    global_handler as g_h


# type
def get_raw_types() -> tuple | str:
    return s_h.select_handler.get_raw_types()


def get_single_type(raw_type_id: int, active: bool = True) -> tuple | str:
    return s_h.select_handler.get_single_type(raw_type_id=raw_type_id, active=active)


def get_active_member_type() -> tuple | str:
    return s_h.select_handler.get_active_member_type()


def add_type(type_name: str, raw_type_id: int) -> str | None:
    return a_h.add_handler.add_type(type_name=type_name, raw_type_id=raw_type_id)


def update_type(id_: int, name: str) -> str | None:
    return u_h.update_handler.update_type(id_=id_, name=name)


def update_type_activity(id_: int, active: bool) -> str | None:
    return u_h.update_handler.update_type_activity(id_=id_, active=active)


def delete_type(id_: int) -> str | None:
    return d_h.delete_handler.delete_type(id_=id_)


# member
def load_all_member_name(active: bool = True) -> tuple | str:
    return s_h.select_handler.get_names_of_member(active=active)


def get_member_data_by_id(id_: int, active: bool = True) -> dict | str:
    return g_h.global_handler.get_member_data(id_=id_, active=active)


def update_member_data(id_: int, data: dict) -> str | None:
    return g_h.global_handler.update_member_data(id_=id_, data=data)

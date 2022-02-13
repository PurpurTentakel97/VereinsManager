# Purpur Tentakel
# 08.02.2022
# VereinsManager / Transition

from sqlite import types_handler, global_handler, member_handler, member_nexus_handler


# config
def get_display_types(type_) -> list:
    return types_handler.get_display_types(type_type=type_)


def get_type_list(display_name: str) -> list:
    return types_handler.get_type_list(display_name=display_name)


def add_type(display_name: str, type_: str) -> None:
    types_handler.add_type(display_name=display_name, type_=type_)


def edit_type(display_name: str, new_type_: str, type_id: int) -> None:
    types_handler.edit_type(display_name=display_name, new_type_=new_type_, type_id=type_id)


def remove_type(display_name: str, type_id: int) -> None:
    types_handler.remove_type(display_name=display_name, type_id=type_id)


# member
def save_update_member(output: dict, time_stamp) -> dict:
    return global_handler.save_update_member(output=output, time_stamp=time_stamp)


def load_all_member_names(active: bool) -> list:
    return member_handler.load_all_member_names(active=active)


def load_data_single_member(id_: int) -> list:
    return member_handler.load_data_from_single_member(id_=id_)


# member nexus
def load_member_nexus(member_id, table_type) -> list:
    return member_nexus_handler.load_member_nexus(member_id=member_id, table_type=table_type)

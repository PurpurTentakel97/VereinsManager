# Purpur Tentakel
# 07.02.2022
# VereinsManager / Handler Types

import enum_sheet
from enum_sheet import TypeType

from sqlite import sql_database


# add
def add_type(display_name: str, type_: str) -> None:
    sql_database.database.types.add_type(table_name=get_type_from_display_name(display_name=display_name), type_=type_)


# edit
def edit_type(display_name: str, new_type_: str, type_id: int) -> None:
    sql_database.database.types.edit_type(table_name=get_type_from_display_name(display_name=display_name),
                                          new_type=new_type_,
                                          type_id=type_id)


# remove
def remove_type(display_name: str, type_id: int) -> None:
    sql_database.database.types.remove_type(table_name=get_type_from_display_name(display_name=display_name),
                                            type_id=type_id)


# get
def get_all_types() -> list:
    all_types: list = list()
    for type_ in enum_sheet.all_types.items():
        all_types.append(type_[1])
    return all_types


def get_type_from_display_name(display_name: str) -> str:
    for type_ in get_all_types():
        if display_name in type_:
            return type_[0]


def get_display_types(type_type: TypeType) -> list[str]:
    display_types: list = list()
    dummy_list: list = list()

    match type_type:
        case TypeType.ALL:
            dummy_list = get_all_types()
        case TypeType.MEMBER:
            dummy_list = enum_sheet.member_types

    for type_ in dummy_list:
        display_types.append(type_[1])
    return display_types


def get_type_list(display_name: str) -> list:
    return sql_database.database.types.get_type_list(table_name=get_type_from_display_name(display_name=display_name))

# Purpur Tentakel
# 07.02.2022
# VereinsManager / Handler

from sqlite import sql_database

import main
import enum_sheet
from enum_sheet import TableTypes, TypeType


def create_database_classes() -> None:
    sql_database.database = sql_database.Database()


def create_all_tables() -> None:
    for type_ in enum_sheet.get_all_types():
        sql_database.database.types.create_type_table(table_name=type_[0])
    sql_database.database.member.create_member_table()
    sql_database.database.member_nexus.create_member_nexus_tables()
    sql_database.database.log.create_log_tables()


def get_display_types(type_type: TypeType) -> list[str]:
    display_types: list = list()
    dummy_list: list = list()

    match type_type:
        case TypeType.ALL:
            dummy_list = enum_sheet.get_all_types()
        case TypeType.MEMBER:
            dummy_list = enum_sheet.member_types

    for type_ in dummy_list:
        display_types.append(type_[1])
    return display_types


def get_type_from_display_name(display_name: str) -> str:
    for type_ in enum_sheet.get_all_types():
        if display_name in type_:
            return type_[0]


def save_member_nexus(member_id: int, table_type, output: tuple) -> dict:
    ids: dict = dict()
    for member_table_id, value_id, value_type, value in output:
        if member_table_id is None and len(value) == 0:  # no entry
            continue

        elif member_table_id is None and len(value) > 0:  # save entry
            id_ = sql_database.database.member_nexus.save_member_nexus(table_type=table_type, member_id=member_id, value_id=value_id,
                                                          value=value)
            ids[value_type] = id_
            main.log_initial_member_nexus(member_id=member_id, log_type=value_type, new_data=value)

        elif member_table_id is not None and len(value) > 0:  # update entry
            reference_data = sql_database.database.member_nexus.load_nexus_item_from_id(table_type=table_type, id_=member_table_id)
            sql_database.database.member_nexus.update_member_nexus(table_type=table_type, member_table_id=member_table_id, value=value)
            main.log_update_member_nexus(reverence_data=reference_data, log_type=value_type, new_data=value)

        elif member_table_id is not None and len(value) == 0:  # delete entry
            reference_data = sql_database.database.member_nexus.load_nexus_item_from_id(table_type=table_type, id_=member_table_id)
            sql_database.database.member_nexus.delete_member_nexus(table_type=table_type, id_=member_table_id)
            main.log_update_member_nexus(reverence_data=reference_data, log_type=value_type, new_data=value)
        else:
            print("Error save member nexus")
    return ids


def load_member_nexus(member_id, table_type: TableTypes):
    value_type: str = str()
    match table_type:
        case TableTypes.MEMBER_PHONE:
            value_type: str = enum_sheet.get_single_type(table_type=table_type)
            table_type: str = TableTypes.MEMBER_PHONE.value
        case TableTypes.MEMBER_MAIL:
            value_type: str = enum_sheet.get_single_type(table_type=table_type)
            table_type: str = TableTypes.MEMBER_MAIL.value
        case TableTypes.MEMBER_POSITION:
            value_type: str = enum_sheet.get_single_type(table_type=table_type)
            table_type: str = TableTypes.MEMBER_POSITION.value

    data = sql_database.database.member_nexus.load_member_nexus(member_id=member_id, table_type=table_type)
    data_ = list()
    for i in data:
        i = list(i)
        type_id = i[2]
        type_ = sql_database.database.types.get_type_from_id(id_=type_id, table_type=value_type)
        i[2] = type_
        data_.append(i)
    return data_

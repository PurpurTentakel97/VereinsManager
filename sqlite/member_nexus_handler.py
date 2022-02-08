# Purpur Tentakel
# 07.02.2022
# VereinsManager / Handler Member Nexus

from datetime import date

from sqlite import sql_database, log_handler
import enum_sheet
from enum_sheet import TableTypes
from sqlite3 import OperationalError


def safe_update_member_nexus(member_id: int, table_type, output: tuple, time_stamp: date) -> dict:
    new_ids: dict = dict()
    for data in output:
        member_value_id, value_id, type_, value = data
        if member_value_id is None and len(value) == 0:  # no data
            continue

        elif member_value_id is None and len(value) > 0:  # new entry
            new_id: int = sql_database.database.member_nexus.save_member_nexus(table_type=table_type,
                                                                               member_id=member_id, value_id=value_id,
                                                                               value=value)
            log_handler.log_initial_data(new_data=value, type_=type_, member_id=member_id, time_stamp=time_stamp)
            new_ids[type_] = new_id
            continue

        elif member_value_id is not None and len(value) > 0:  # update entry
            reverence_data: tuple = sql_database.database.member_nexus.load_nexus_item_from_id(table_type=table_type,
                                                                                               id_=member_value_id)
            sql_database.database.member_nexus.update_member_nexus(table_type=table_type,
                                                                   member_table_id=member_value_id, value=value)
            log_handler.log_data(reference_data=reverence_data, output=data, time_stamp=time_stamp,
                                 table_type=table_type)
            continue
        elif member_value_id is not None and len(value) == 0:  # delete entry
            reverence_data: tuple = sql_database.database.member_nexus.load_nexus_item_from_id(table_type=table_type,
                                                                                               id_=member_value_id)
            sql_database.database.member_nexus.delete_member_nexus(table_type=table_type, id_=member_value_id)
            log_handler.log_data(reference_data=reverence_data, output=data, time_stamp=time_stamp,
                                 table_type=table_type)
    return new_ids


def safe_update_member_position(member_id: int, output: tuple, time_stamp: date) -> dict:
    new_ids: dict = dict()
    for data in output:
        member_position_id, value_id, value, active = data
        if member_position_id is None and value_id is None:  # no data
            continue

        elif member_position_id is None and active:  # new entry
            new_id: int = sql_database.database.member_nexus.save_member_nexus_position(member_id=member_id,
                                                                                        value_id=value_id)
            log_handler.log_initial_data(new_data=value, type_=value, member_id=member_id, time_stamp=time_stamp)
            new_ids[value] = new_id
            continue
        elif member_position_id is not None and active:  # update entry
            reference_data = sql_database.database.member_nexus.load_nexus_item_from_id(
                table_type=TableTypes.MEMBER_POSITION,
                id_=member_position_id)
            sql_database.database.member_nexus.update_member_nexus(table_type=TableTypes.MEMBER_POSITION,
                                                                   member_table_id=member_position_id, value=value_id)
            log_handler.log_data(reference_data=reference_data, output=data, time_stamp=time_stamp,
                                 table_type=TableTypes.MEMBER_POSITION)
            continue
        elif member_position_id is not None and not active:  # delete entry
            try:
                reference_data = sql_database.database.member_nexus.load_nexus_item_from_id(
                    table_type=TableTypes.MEMBER_POSITION,
                    id_=member_position_id)
                sql_database.database.member_nexus.delete_member_nexus(table_type=TableTypes.MEMBER_POSITION,
                                                                       id_=member_position_id)
                log_handler.log_data(reference_data=reference_data, output=data, time_stamp=time_stamp,
                                     table_type=TableTypes.MEMBER_POSITION)
            except OperationalError:
                pass

    return new_ids


def load_member_nexus(member_id, table_type: TableTypes) -> list:
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

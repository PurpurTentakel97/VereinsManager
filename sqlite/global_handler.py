# Purpur Tentakel
# 07.02.2022
# VereinsManager / Global Handler

from datetime import date

import main
import enum_sheet
from enum_sheet import TableTypes
from sqlite import sql_database
from sqlite import types_handler, member_handler, member_nexus_handler


def create_database_classes() -> None:
    sql_database.create_database()


def create_all_tables() -> None:
    for type_ in types_handler.get_all_types():
        sql_database.database.types.create_type_table(table_name=type_[0])
    sql_database.database.member.create_member_table()
    sql_database.database.member_nexus.create_member_nexus_tables()
    sql_database.database.log.create_log_tables()


def save_update_member(output: dict, time_stamp: date) -> dict:
    try:
        member_output: dict = output["member"]
        member_phone_output: tuple = output["member_phone"]
        member_mail_output: tuple = output["member_mail"]
        member_position_output: tuple = output["member_position"]

    except KeyError:
        print("ERROR-LOG // GLOBAL HANDLER // key error save/update member")
        return dict()

    member_id: int = member_handler.save_update_member(output=member_output, time_stamp=time_stamp)
    if not member_id:
        member_id = member_output["ID"]
    member_phone_ids: dict = member_nexus_handler.safe_update_member_nexus(member_id=member_id,
                                                                           table_type=TableTypes.MEMBER_PHONE,
                                                                           output=member_phone_output,
                                                                           time_stamp=time_stamp)
    member_mail_ids: dict = member_nexus_handler.safe_update_member_nexus(member_id=member_id,
                                                                          table_type=TableTypes.MEMBER_MAIL,
                                                                          output=member_mail_output,
                                                                          time_stamp=time_stamp)
    member_position_ids: dict = member_nexus_handler.safe_update_member_position(member_id=member_id,
                                                                                 output=member_position_output,
                                                                                 time_stamp=time_stamp)

    all_ids: dict = {
        "member": member_id,
        "member_phone": member_phone_ids,
        "member_mail": member_mail_ids,
        "member_position": member_position_ids
    }

    return all_ids


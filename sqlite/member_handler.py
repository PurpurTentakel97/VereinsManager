# Purpur Tentakel
# 08.02.2022
# VereinsManager / Handler member

from sqlite import sql_database, log_handler
from enum_sheet import TableTypes


def save_update_member(output: dict, time_stamp) -> int:
    if output["ID"]:
        _update_member(output=output, time_stamp=time_stamp)
    else:
        return _save_member(output=output, time_stamp=time_stamp)


def _save_member(output: dict, time_stamp) -> int:
    member_id = sql_database.database.member.save_member(output=output)
    for type_, item in output.items():
        log_handler.log_initial_data(new_data=item, type_=type_, member_id=member_id, time_stamp=time_stamp)
    return member_id


def _update_member(output: dict, time_stamp) -> None:
    reference_data = sql_database.database.member.load_all_data_from_member(output["ID"])
    sql_database.database.member.update_member(output=output)
    log_handler.log_data(reference_data=reference_data, output=output, time_stamp=time_stamp,
                         table_type=TableTypes.MEMBER)


def load_all_member_names(active: bool) -> list:
    return sql_database.database.member.load_all_member_names(active=active)


def load_data_from_single_member(id_: int) -> list:
    return sql_database.database.member.load_data_from_single_member(id_=id_)

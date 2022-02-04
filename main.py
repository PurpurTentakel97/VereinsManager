# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
import datetime
from sqlite3 import OperationalError

from logic import sqlite

from ui import base_window, main_window

from enum_sheet import MemberTypes


# types
def get_types(type_) -> list:
    return sqlite.handler.get_display_types(type_type=type_)


def get_type_list(display_name: str) -> list:
    return sqlite.database.get_type_list(
        table_name=sqlite.handler.get_type_from_display_name(display_name=display_name))


def add_type(display_name: str, type_: str) -> None:
    sqlite.database.add_type(table_name=sqlite.handler.get_type_from_display_name(display_name=display_name),
                             type_=type_)


def edit_type(display_name: str, new_type_: str, type_id: int) -> None:
    sqlite.database.edit_type(table_name=sqlite.handler.get_type_from_display_name(display_name=display_name),
                              new_type=new_type_, type_id=type_id)


def remove_type(display_name: str, type_id: int) -> None:
    commit_: bool = sqlite.database.remove_type(
        table_name=sqlite.handler.get_type_from_display_name(display_name=display_name),
        type_id=type_id)

    if not commit_:
        main_window.main_window_.set_status_bar("Type konnte nichtgelöscht werden.")


# member
def save_member(output: dict) -> int:
    id_ = sqlite.database.save_member(output=output)

    _log_initial_member_data(output=output, member_id=id_)

    return id_


def update_member(output: dict) -> None:
    reference_data: list = sqlite.database.load_all_data_from_member(id_=output[MemberTypes.ID.value])
    _log_update_member_data(output=output, reference_data=reference_data)
    sqlite.database.update_member(output=output)


def delete_recover_member(output: list) -> None:
    member_id, active = output
    reverence_data = sqlite.database.load_all_data_from_member(id_=member_id)
    reverence_data = [reverence_data[0], reverence_data[-1]]
    sqlite.database.delete_recover_member(member_id=member_id, active=active)
    _log_update_member_active(output=output, reverence_data=reverence_data)


def load_all_member_names(active: bool) -> list:
    return sqlite.database.load_all_member_names(active=active)


def load_data_from_single_member(id_: int) -> list:
    try:
        return sqlite.database.load_data_from_single_member(id_=id_)
    except OperationalError:
        return list()


# member nexus
def save_member_nexus(member_id: int, table_type, output: tuple) -> None:
    if len(output) > 0:
        sqlite.handler.save_member_nexus(member_id=member_id, table_type=table_type, output=output)


# log data
def _log_initial_member_data(output: dict, member_id: int) -> None:
    for log_type, value in output.items():
        match value:
            case None:
                continue
            case "":
                continue

        sqlite.database.log_data(member_id=member_id, log_type=log_type,
                                 log_date=datetime.date.today(), old_data=None, new_data=value)


def _log_update_member_data(output: dict, reference_data: list) -> None:
    reference_data = reference_data[:-1]
    reference_data.pop(0)
    output_list = list(output.items())

    for index, old_value in enumerate(reference_data):
        log_type, value = output_list[index]

        if value == "":
            value = None

        if old_value != value:
            sqlite.database.log_data(member_id=output[MemberTypes.ID.value], log_type=log_type,
                                     log_date=datetime.date.today(), old_data=old_value, new_data=value)


def _log_update_member_active(output: list, reverence_data: list) -> None:
    output_id, output_value = output
    reverence_data_id, reverence_data_value = reverence_data
    if output_value != reverence_data_value:
        sqlite.database.log_data(member_id=reverence_data_id, log_type=MemberTypes.ACTIVE_MEMBER.value,
                                 log_date=datetime.date.today(), old_data=reverence_data_value, new_data=output_value)


# main
if __name__ == "__main__":
    sqlite.database = sqlite.Database()
    sqlite.handler = sqlite.Handler()
    sqlite.handler.create_all_tables()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()

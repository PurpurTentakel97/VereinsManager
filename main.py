# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

from os import path, mkdir
import json

from logic import sqlite

import transition
from logic.enum_sheet import SQLite_Table, MemberEntries


def _get_ui_types() -> dict:
    if not path.exists("types"):
        mkdir("types")
    with open("types/type.json", "r", encoding="utf=8") as f:
        data = json.load(f)
        return data


def _get_ui_non_types() -> dict:
    if not path.exists("types"):
        mkdir("types")
    with open("types/non_type.json", "r", encoding="utf=8") as f:
        data = json.load(f)
        return data


def set_path(path_: str) -> None:
    sqlite.path_ = path_
    sqlite.create_connection()


def save_data(data: list[dict], table: SQLite_Table) -> None:
    create_data: list = list()
    edit_data: list = list()
    for single_data in data:
        if single_data[MemberEntries.ID] is None:
            create_data.append(single_data)
        else:
            edit_data.append(single_data)
    if create_data:
        sqlite.write_data(table=table, data=create_data)
    if edit_data:
        sqlite.edit_data(table=table, data=edit_data)


def load_data(table: SQLite_Table) -> list:
    return sqlite.read_data(table=table)


if __name__ == "__main__":
    transition.put_types_in_ui(types=_get_ui_types())
    transition.put_non_types_in_ui(non_types=_get_ui_non_types())
    transition.create_application()
    set_path("saves/test.vm")
    transition.create_main_window()
    transition.run_application()

# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main
import enum_sheet

from logic import sqlite

from ui import base_window, main_window


def add_type(table_name: str, type_: str) -> None:
    sqlite.database.add_type(table_name=table_name, type_=type_)


def get_types() -> list:
    return enum_sheet.types


def get_type_list(table_name: str) -> list:
    return sqlite.database.get_type_list(table_name=table_name)


if __name__ == "__main__":
    sqlite.database = sqlite.Database()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()

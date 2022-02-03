# Purpur Tentakel
# 21.01.2022
# VereinsManager / Main

from logic import sqlite

from ui import base_window, main_window


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
    return sqlite.database.save_member(output=output)


def update_member(output: dict) -> None:
    print("updating member")


# member nexus
def save_member_nexus(member_id: int, table_type, output: tuple) -> None:
    if len(output) > 0:
        sqlite.handler.save_member_nexus(member_id=member_id, table_type=table_type, output=output)


# main
if __name__ == "__main__":
    sqlite.database = sqlite.Database()
    sqlite.handler = sqlite.Handler()
    sqlite.handler.create_all_tables()
    base_window.create_application()
    main_window.main_window_ = main_window.MainWindow()
    base_window.run_application()

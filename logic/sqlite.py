# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3

import enum_sheet


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("saves/test.vm")
        self.cursor = self.connection.cursor()

    def create_type_table(self, table_name: str) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{table_name}" (
        "ID" INTEGER NOT NULL UNIQUE,
        "{table_name}" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("ID" AUTOINCREMENT));"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_type_list(self, table_name: str) -> list:
        sql_command: str = f"""SELECT * FROM {table_name} ORDER BY {table_name}"""
        self.cursor.execute(sql_command)
        types_list: list = self.cursor.fetchall()
        return types_list

    def add_type(self, table_name: str, type_: str) -> None:
        sql_command: str = f"""INSERT INTO "{table_name}"
        ("{table_name}")
        VALUES('{type_}');"""
        self.cursor.execute(sql_command)
        self.connection.commit()

    def edit_type(self, table_name: str, new_type: str, type_id: int):
        sql_command: str = f"""UPDATE {table_name} SET {table_name} = '{new_type}' WHERE ID = {type_id};"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def remove_type(self, table_name: str, type_id: int) -> bool:
        sql_command: str = f"""DELETE FROM {table_name} WHERE ID ='{type_id}';"""

        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            return True
        except:
            return False


class Handler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_all_tables() -> None:
        for type_ in enum_sheet.types:
            database.create_type_table(table_name=type_[0])

    @staticmethod
    def get_display_types() -> list[str]:
        display_types: list = list()
        for type_ in enum_sheet.types:
            display_types.append(type_[1])
        return display_types

    @staticmethod
    def get_type_from_display_name(display_name: str) -> str:
        for type_ in enum_sheet.types:
            if display_name in type_:
                return type_[0]


database: Database | None = None
handler: Handler | None = None

# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3

import enum_sheet
from enum_sheet import TypeType


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

    def remove_type(self, table_name: str, type_: str) -> None:
        sql_command: str = f"""DELETE FROM {table_name} WHERE {table_name} ='{type_}';"""

        self.cursor.execute(sql_command)
        self.connection.commit()


class Handler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_all_tables() -> None:
        for type_ in enum_sheet.get_all_types():
            database.create_type_table(table_name=type_[0])

    @staticmethod
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

    @staticmethod
    def get_type_from_display_name(display_name: str) -> str:
        for type_ in enum_sheet.get_all_types():
            if display_name in type_:
                return type_[0]


database: Database | None = None
handler: Handler | None = None

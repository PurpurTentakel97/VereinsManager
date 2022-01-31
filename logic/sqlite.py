# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3

import enum_sheet

database: "Database" or None = None
handler: "Handler" or None = None


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("saves/test.vm")
        self.cursor = self.connection.cursor()

    def get_type_list(self, table_name: str) -> list:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{table_name}" (
        "ID" INTEGER NOT NULL UNIQUE,
        "{table_name}" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("ID" AUTOINCREMENT));"""

        self.cursor.execute(sql_command)
        self.connection.commit()

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


class Handler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get_display_types() -> list[str]:
        display_types: list = list()
        for types in enum_sheet.types:
            display_types.append(types[1])
        return display_types

    @staticmethod
    def get_type_from_display_name(display_name: str) -> str:
        for types in enum_sheet.types:
            if display_name in types:
                return types[0]



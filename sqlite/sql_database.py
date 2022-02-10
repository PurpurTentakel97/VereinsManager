# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3
from sqlite3 import OperationalError

from sqlite.sql_log import DatabaseLog
from sqlite.sql_member import DatabaseMember
from sqlite.sql_member_nexus import DatabaseMemberNexus
from sqlite.sql_types import DatabaseTypes

import debug

database: "Database"


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("saves/test.vm", detect_types=sqlite3.PARSE_DECLTYPES)  # TODO name save file
        self.cursor = self.connection.cursor()

        self.log = DatabaseLog(self)
        self.member = DatabaseMember(self)
        self.member_nexus = DatabaseMemberNexus(self)
        self.types = DatabaseTypes(self)

    def __str__(self) -> str:
        return "Database"

    class CreateItem:
        def __init__(self, column_name: str, column_type: int, column_is_not_null: bool = False,
                     column_is_unique: bool = False, is_primary_key: bool = False, is_autoincrement: bool = False,
                     is_foreign_key: bool = False, foreign_reference: str | None = None) -> None:
            self.column_name: str = column_name
            self.column_type: int | str = column_type
            self.column_is_not_null: bool = column_is_not_null
            self.column_is_unique: bool = column_is_unique
            self.is_primary_key: bool = is_primary_key
            self.is_autoincrement: bool = is_autoincrement
            self.is_foreign_key: bool = is_foreign_key
            self.foreign_reference: str | None = foreign_reference

        def __str__(self) -> str:
            return "CreateItem"

        def is_correct_item(self) -> bool:
            if not type(self.column_name) == str:
                debug.error(item=self, keyword=self.column_name, message=f"{self.column_name} must be a str")
                return False

            elif not type(self.column_type) == int:
                debug.error(item=self, keyword=self.column_name,
                            message=f"{self.column_type} must be an integer")
                return False

            elif not self._transform_column_type():
                # Error in method
                return False

            elif self.is_primary_key and self.is_foreign_key:
                debug.error(item=self, keyword=self.column_name,
                            message=f"{self.is_primary_key} and {self.is_foreign_key} can not both be true")
                return False

            elif self.is_foreign_key and not self.foreign_reference:
                debug.error(item=self, keyword=self.column_name,
                            message=f"if {self.is_foreign_key} is True, {self.foreign_reference} can't be None")
                return False

            try:
                database.select_all(table_name=self.foreign_reference)
            except OperationalError:
                debug.error(item=self, keyword=self.foreign_reference, message="FOREIGN KEY reference not found")
                return False

            return True

        def _transform_column_type(self) -> bool:
            match self.column_type:
                case 0:
                    debug.error(item=self, keyword=self.column_name,
                                message=f"{self.column_type} // 'NULL' is not available in CREATE-statement")
                    return False
                case 1:  # int
                    self.column_type: str = "INTEGER"
                case 2:  # real
                    self.column_type: str = "REAL"
                case 3:  # text
                    self.column_type: str = "TEXT"
                case 4:  # blob
                    self.column_type: str = "BLOB"
                case 5:  # date
                    self.column_type: str = "TEXT"
                case _:
                    debug.error(item=self, keyword=self.column_name,
                                message=f"{self.column_type} must be an Integer between 0 and 5")
                    return False
            return True

    def create(self, table_name: str, columns: tuple[CreateItem]) -> None:
        if not type(table_name) == str:
            debug.error(item=self, keyword=table_name, message="table_name must be a string")
            return
        for item in columns:
            if not item.is_correct_item():
                # Error in method
                return
        if not self._is_correct_create_input(columns=columns):
            # Error in method
            return

        column_command: str = str()
        primary_key_command: str = str()
        foreign_key_command: str = str()

        for item in columns:
            column_command += f"""'{item.column_name}' {item.column_type} """
            if item.column_is_not_null:
                column_command += f"""NOT NULL """
            if item.column_is_unique:
                column_command += f"""UNIQUE """
            column_command += f""","""

            if item.is_primary_key:
                primary_key_command += f"""PRIMARY KEY ('{item.column_name}' """
                if item.is_autoincrement:
                    primary_key_command += f"""AUTOINCREMENT"""
                primary_key_command += f"""),"""

            if item.is_foreign_key:
                foreign_key_command += f"""FOREIGN KEY('{item.column_name}') REFERENCES '{item.foreign_reference}',"""

        sql_command: str = f"""CREATE TABLE IF NOT EXISTS '{table_name}' ("""
        sql_command += column_command
        sql_command += primary_key_command
        sql_command += foreign_key_command
        sql_command = sql_command[:-1]
        sql_command += f""");"""

        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
        except OperationalError:
            debug.error(item=self, keyword="Operational Error", message=f"Create {table_name} failed")

    def insert(self, sql_command: str, values: list) -> int:
        pass

    def update(self, sql_command: str, values: list) -> None:
        pass

    def delete(self, sql_command: str) -> None:
        pass

    def select_all(self, table_name: str, conditions: tuple[tuple[str, str]] = None, items: tuple | None = None,
                   is_or: bool = False) -> tuple:

        if not type(table_name) == str:
            debug.error(item=self, keyword="select all", message=f"{table_name} must be a string")
            return ()

    # sql_command: str = f"""SELECT {MemberTypes.ID.value},
    # {MemberTypes.FIRST_NAME.value},
    # {MemberTypes.LAST_NAME.value}
    # FROM {TableTypes.MEMBER.value}
    # WHERE {MemberTypes.ACTIVE_MEMBER.value} LIKE {active};"""

    def select_one(self, sql_command: str) -> list:
        pass

    def _is_correct_create_input(self, columns: tuple[CreateItem]) -> bool:
        for item in columns:
            for inner_item in columns:
                if item == inner_item:
                    continue
                elif item.column_name == inner_item.column_name:
                    debug.error(item=self, keyword=item.column_name,
                                message="No multiple columns with same name")
                    return False
                elif item.is_primary_key and inner_item.is_primary_key:
                    debug.error(item=self, keyword=item.column_name, message="No multiple PRIMARY KEYS")
                    return False
        return True


def create_database() -> None:
    global database
    database = Database()

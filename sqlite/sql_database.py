# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3

from sqlite.sql_log import DatabaseLog
from sqlite.sql_member import DatabaseMember
from sqlite.sql_member_nexus import DatabaseMemberNexus
from sqlite.sql_types import DatabaseTypes

database: "Database" or None = None


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("saves/test.vm", detect_types=sqlite3.PARSE_DECLTYPES)  # TODO name save file
        self.cursor = self.connection.cursor()

        self.log = DatabaseLog(self)
        self.member = DatabaseMember(self)
        self.member_nexus = DatabaseMemberNexus(self)
        self.types = DatabaseTypes(self)

    def create(self, sql_command: str) -> None:
        self.cursor.execute(sql_command)
        self.connection.commit()

    def insert(self, sql_command: str, values: list) -> int:
        self.cursor.execute(sql_command, values)
        self.connection.commit()
        return self.cursor.lastrowid

    def update(self, sql_command: str, values: list) -> None:
        self.cursor.execute(sql_command, values)
        self.connection.commit()

    def delete(self, sql_command: str) -> None:
        self.cursor.execute(sql_command)
        self.connection.commit()

    def select_all(self, sql_command: str) -> list:
        self.cursor.execute(sql_command)
        return self.cursor.fetchall()

    def select_one(self, sql_command: str) -> list:
        self.cursor.execute(sql_command)
        return self.cursor.fetchone()


def create_database() -> None:
    global database
    database = Database()

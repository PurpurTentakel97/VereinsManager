# Purpur Tentakel
# 13.02.2022
# VereinsManager / Database

import sqlite3

import debug

database: "Database"

database_path: str = "saves/test.vm"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

        self._create_tables()

    def _create_tables(self) -> None:
        with open("config/create.sql") as create_file:
            self.cursor.executescript(create_file.read())

        self.connection.commit()

    def load_all_from_id(self, table_name: str, id_: int) -> list:
        try:
            sql: str = f"""SELECT * FROM {table_name} WHERE ID is {id_};"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except sqlite3.OperationalError:
            debug.error(item=self, keyword="load_all_from_id",
                        message=f"load with table_name = {table_name} / id = {id_} failed")

    def load_all_from_condition(self, table_name: str, condition: str, value) -> list:
        try:
            sql: str = f"""SELECT * FROM {table_name} WHERE {condition} is {value};"""
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            debug.error(item=self, keyword="load_all_from_condition",
                        message=f"load with table_name = {table_name} / "
                                f"condition = {condition} / value = {value} failed")

    def load_single_from_id(self, column: str, table_name: str, id_: int) -> list:
        try:
            sql: str = f"""SELECT {column} FROM {table_name} WHERE ID is {id_};"""
            self.cursor.execute(sql)
            return self.cursor.fetchone()
        except sqlite3.OperationalError:
            debug.error(item=self, keyword="load_single_from_id",
                        message=f"load with table_name = {table_name} / column = {column} / id = {id_} failed")

    def load_single_from_condition(self, column: str, table_name: str, condition: str, value) -> list:
        try:
            sql: str = f"""SELECT {column} FROM {table_name} WHERE {condition} is {value};"""
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            debug.error(item=self, keyword="load_all_from_condition",
                        message=f"load with table_name = {table_name} / column = {column}/ "
                                f"condition = {condition} / value = {value} failed")


def crate_database() -> None:
    global database
    database = Database()

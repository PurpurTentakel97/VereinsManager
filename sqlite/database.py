# Purpur Tentakel
# 13.02.2022
# VereinsManager / Database
import asyncio
import sqlite3

import config_sheet

database: "Database"


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("saves/test.vm", detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()

        self._create_tables()

    def _create_tables(self) -> None:
        with open("config/create.sql") as create_file:
            self.cursor.executescript(create_file.read())

        self.connection.commit()


def crate_database() -> None:
    global database
    database = Database()

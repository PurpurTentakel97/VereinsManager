# Purpur Tentakel
# 13.02.2022
# VereinsManager / Database

import sqlite3

import debug

database: "Database"

database_path: str = "saves/test.vm"


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(database_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()
        self.OperationalError = sqlite3.OperationalError
        self.IntegrityError = sqlite3.IntegrityError

        self._create_tables()

    def __str__(self) -> str:
        return "Database"

    def _create_tables(self) -> None:
        with open("config/create.sql") as create_file:
            try:
                self.cursor.executescript(create_file.read())
            except self.OperationalError as error:
                debug.error(item=self, keyword="_create_tables", message=f"create tables failed\n"
                                                                         f"error = {' '.join(error.args)}")

        self.connection.commit()


def crate_database() -> None:
    global database
    database = Database()

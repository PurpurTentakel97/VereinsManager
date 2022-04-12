# Purpur Tentakel
# 13.02.2022
# VereinsManager / Database

import sqlite3
import os
import sys

from config import config_sheet as c
import debug

debug_str: str = "Database"

database: "Database"


class Database:
    def __init__(self) -> None:
        self.OperationalError = sqlite3.OperationalError
        self.IntegrityError = sqlite3.IntegrityError

        self.create_cursor_connection()
        self._create_tables()

    def _create_tables(self) -> None:
        with open(os.path.join("config", "create.sql")) as create_file:
            try:
                self.cursor.executescript(create_file.read())
            except self.OperationalError:
                debug.error(item=debug_str, keyword="_create_tables", error_=sys.exc_info())

        self.connection.commit()

    def create_cursor_connection(self) -> None:
        if not os.path.exists(os.path.join(c.config.dirs['save'], c.config.dirs['organisation'])):
            os.makedirs(os.path.join(c.config.dirs['save'], c.config.dirs['organisation']))
        self.connection = sqlite3.connect(
            os.path.join(c.config.dirs['save'], c.config.dirs['organisation'], c.config.files['database']),
            detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def drop_connection(self) -> None:
        self.connection.close()


def crate_database() -> None:
    global database
    database = Database()

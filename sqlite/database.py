# Purpur Tentakel
# 13.02.2022
# VereinsManager / Database

import sqlite3
import os

from config import config_sheet as c
import debug

debug_str: str = "Database"

database: "Database"

#dir_path:str = f"{c.config.save_dir}/{c.config.organisation_dir}"


class Database:
    def __init__(self) -> None:
        self.OperationalError = sqlite3.OperationalError
        self.IntegrityError = sqlite3.IntegrityError

        self.create_cursor_connection()
        self._create_tables()

    def __str__(self) -> str:
        return "Database"

    def _create_tables(self) -> None:
        with open("config/create.sql") as create_file:
            try:
                self.cursor.executescript(create_file.read())
            except self.OperationalError as error:
                debug.error(item=debug_str, keyword="_create_tables", message=f"create tables failed\n"
                                                                              f"error = {' '.join(error.args)}")

        self.connection.commit()

    def create_cursor_connection(self) -> None:
        if not os.path.exists(f"{c.config.save_dir}/{c.config.organisation_dir}"):
            os.makedirs(f"{c.config.save_dir}/{c.config.organisation_dir}")
        self.connection = sqlite3.connect(f"{c.config.save_dir}/{c.config.organisation_dir}/{c.config.database_name}", detect_types=sqlite3.PARSE_DECLTYPES)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.connection.cursor()

    def drop_connection(self) -> None:
        pass


def crate_database() -> None:
    global database
    database = Database()

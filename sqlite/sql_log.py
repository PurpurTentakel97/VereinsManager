# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Log

from datetime import date

from enum_sheet import TableTypes, LogTypes
import enum_sheet

database_log: "DatabaseLog" or None = None


class DatabaseLog:
    def __init__(self, database):
        self.database = database

    def create_log_tables(self) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.LOG.value}" (
        "{LogTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{LogTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{LogTypes.LOG_TYPE.value}"	TEXT NOT NULL,
        "{LogTypes.DATE.value}"	TEXT NOT NULL,
        "{LogTypes.OLD_DATA.value}"	TEXT,
        "{LogTypes.NEW_DATA.value}"	TEXT,
        FOREIGN KEY("{LogTypes.MEMBER_ID.value}") REFERENCES "member",
        PRIMARY KEY("{LogTypes.ID.value}" AUTOINCREMENT));"""

        self.database.create(sql_command=sql_command)

    def log_data(self, member_id: int, log_type: str, log_date: date, old_data: str | None,
                 new_data: str | None) -> None:
        sql_command: str = f"""INSERT INTO "{TableTypes.LOG.value}"
        ("{LogTypes.MEMBER_ID.value}",
         "{LogTypes.LOG_TYPE.value}",
         "{LogTypes.DATE.value}",
         "{LogTypes.OLD_DATA.value}",
         "{LogTypes.NEW_DATA.value}")
        VALUES (?, ?, ?, ?, ?);"""
        values: list = [member_id, log_type,
                        log_date.strftime(enum_sheet.date_format) if log_date is not None else None]

        if type(old_data) == bool or type(new_data) == bool:
            values.append(old_data)
            values.append(new_data)
        else:
            values.append(old_data or None)
            values.append(new_data or None)

        self.database.insert(sql_command=sql_command, values=tuple(values))

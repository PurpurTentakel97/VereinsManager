# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Log

from datetime import date

from enum_sheet import TableTypes, LogTypes
import enum_sheet
import debug

database_log: "DatabaseLog" or None = None


class DatabaseLog:
    def __init__(self, database):
        self.database = database
        self.CreateItem = database.CreateItem

    def __str__(self) -> str:
        return "Database Log"

    def create_log_tables(self) -> None:
        sql_items: list = [
            self.CreateItem(column_name=LogTypes.ID.value, column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True),
            self.CreateItem(column_name=LogTypes.MEMBER_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference=TableTypes.MEMBER.value),
            self.CreateItem(column_name=LogTypes.LOG_TYPE.value, column_type=3, column_is_not_null=True),
            self.CreateItem(column_name=LogTypes.DATE.value, column_type=5, column_is_not_null=True),
            self.CreateItem(column_name=LogTypes.OLD_DATA.value, column_type=3),
            self.CreateItem(column_name=LogTypes.NEW_DATA.value, column_type=3)
        ]
        self.database.create(table_name=TableTypes.LOG.value, columns=tuple(sql_items))

    def log_data(self, member_id: int, log_type: str, log_date: date, old_data: str | None,
                 new_data: str | None) -> None:
        debug.info(item=self, keyword=f"{new_data}", message=f"Log saved")
        # sql_command: str = f"""INSERT INTO "{TableTypes.LOG.value}"
        # ("{LogTypes.MEMBER_ID.value}",
        #  "{LogTypes.LOG_TYPE.value}",
        #  "{LogTypes.DATE.value}",
        #  "{LogTypes.OLD_DATA.value}",
        #  "{LogTypes.NEW_DATA.value}")
        # VALUES (?, ?, ?, ?, ?);"""
        # values: list = [member_id, log_type,
        #                 log_date.strftime(enum_sheet.date_format) if log_date is not None else None]
        #
        # if type(old_data) == bool or type(new_data) == bool:
        #     values.append(old_data)
        #     values.append(new_data)
        # else:
        #     values.append(old_data or None)
        #     values.append(new_data or None)
        #
        # self.database.insert(sql_command=sql_command, values=tuple(values))

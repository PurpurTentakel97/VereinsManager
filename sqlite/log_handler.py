# Purpur Tentakel
# 13.02.2022
# VereinsManager / Log Handler

import time

from sqlite.database import Database
from config import error_code as e
from logic import validation as v

import debug

debug_str: str = "Log Handler"

log_handler: "LogHandler"


class LogHandler(Database):
    def __init__(self):
        super().__init__()

    # type
    def log_type(self, target_id: int, target_column: str, old_data, new_data) -> str or None:
        log_date: int = int(time.time())
        try:
            v.validation.must_positive_int(target_id, max_length=None)
            v.validation.must_str(target_column)
        except (e.NoInt, e.NoPositiveInt, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="log_type", message=f"Error = {error.message}")

        return self._log(target_table="type", target_id=target_id, target_column=target_column, old_data=old_data,
                         new_data=new_data, log_date=log_date)

    # member
    def log_member(self, ID: int, old_data: tuple | None, new_data: dict, log_date: int | None):
        if not log_date:
            log_date = int(time.time())
        try:
            v.validation.must_int(int_=log_date)
        except (e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="log_member", message=f"Error = {error.message}")
            return error.message

        if old_data:
            return self._log_member(ID=ID, old_data=old_data, new_data=new_data, log_date=log_date)
        else:
            return self._log_initial_member(ID=ID, new_data=new_data, log_date=log_date)

    def _log_member(self, ID: int, old_data: tuple, new_data: dict, log_date: int):
        pass

    def _log_initial_member(self, ID: int, new_data: dict, log_date: int):
        result = self._log(target_table="member", target_id=ID, target_column="active", old_data=None, new_data=True,
                           log_date=log_date)
        if isinstance(result, str):
            return result

        keys: tuple = (
            "first_name",
            "last_name",
            "street",
            "number",
            "zip_code",
            "birth_date",
            "entry_date",
            "city",
            "membership_type",
            "special_member",
            "comment_text",
        )

        for key in keys:
            if new_data[key]:
                result = self._log(target_table="member", target_id=ID, target_column=key, old_data=None,
                                   new_data=new_data[key], log_date=log_date)
                if isinstance(result, str):
                    return result

    # log
    def _log(self, target_table: str, target_id: int, target_column: str, old_data, new_data,
             log_date: int) -> str | None:
        sql_command: str = f"""INSERT INTO log (target_table,target_id,target_column,old_data,new_data,log_date) 
        VALUES (?, ?, ?, ?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (target_table, target_id, target_column, old_data, new_data, log_date))
            self.connection.commit()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message


def create_log_handler() -> None:
    global log_handler
    log_handler = LogHandler()

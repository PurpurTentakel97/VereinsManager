# Purpur Tentakel
# 13.02.2022
# VereinsManager / Log Handler

from sqlite.database import Database
from config import error_code as e

import debug

debug_str: str = "Log Handler"

log_handler: "LogHandler"


class LogHandler(Database):
    def __init__(self):
        super().__init__()

    def _log(self, target_table: str, target_id: int, old_data, new_data, log_date: int) -> str | None:
        sql_command: str = f"""INSERT INTO log (target_table,target_id,old_data,new_data,log_date) 
        VALUES (?, ?, ?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (target_table, target_id, old_data, new_data, log_date))
            self.connection.commit()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message


def create_log_handler() -> None:
    global log_handler
    log_handler = LogHandler()

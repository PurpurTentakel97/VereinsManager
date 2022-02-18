# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config.error_code import ErrorCode
import debug

select_handler: "SelectHandler"


class SelectHandler(Database):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Select Handler"

    # type
    def get_raw_types(self) -> [ErrorCode, tuple]:
        sql_command: str = f"""SELECT ID,type_name FROM raw_type ORDER BY type_name ASC;"""
        try:
            return ErrorCode.LOAD_S, self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_raw_types", message=f"load raw types failed\n"
                                                                    f"command = {sql_command}\n"
                                                                    f"error = {' '.join(error.args)}")
            return ErrorCode.LOAD_E, ()

    def get_single_type(self, raw_type_id: int, active: bool = True) -> [ErrorCode, tuple]:
        table: str = "v_active_type" if active else "v_inactive_type"
        sql_command: str = f"""SELECT * FROM {table} WHERE type_id is ? ORDER BY name ASC;"""
        try:
            return ErrorCode.LOAD_S, self.cursor.execute(sql_command, (raw_type_id,)).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_single_type", message=f"load raw types failed\n"
                                                                      f"command = {sql_command}\n"
                                                                      f"error = {' '.join(error.args)}")
            return ErrorCode.LOAD_E, ()

    # member
    def get_names_of_member(self, active: bool = True) -> [ErrorCode, tuple]:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return ErrorCode.LOAD_S, self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                          f"command = {sql_command}\n"
                                                                          f"error = {' '.join(error.args)}")
            return ErrorCode.LOAD_E, ()

    def get_data_from_member_by_id(self, id_: int, active: bool = True) -> [ErrorCode, tuple]:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID = ?;"""
        try:
            return ErrorCode.LOAD_S, self.cursor.execute(sql_command, (id_,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return ErrorCode.LOAD_E, ()


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

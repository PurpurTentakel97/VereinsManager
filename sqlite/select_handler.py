# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation as v
import debug

select_handler: "SelectHandler"


class SelectHandler(Database):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Select Handler"

    # type
    def get_raw_types(self) -> tuple | str:
        sql_command: str = f"""SELECT ID,type_name FROM raw_type ORDER BY type_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_raw_types", message=f"load raw types failed\n"
                                                                    f"command = {sql_command}\n"
                                                                    f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Raw Types").message

    def get_all_single_type(self) -> tuple | str:
        sql_command: str = f"""SELECT ID,name,type_id,_active FROM type ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_all_single_type", message=f"load all types failed\n"
                                                                          f"command = {sql_command}\n"
                                                                          f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Typen").message

    def get_single_type(self, raw_type_id: int, active: bool = True) -> tuple | str:
        try:
            v.validation.must_id(id_=raw_type_id)
            v.validation.must_bool(bool_=active)
        except (e.NoBool, e.NoId) as error:
            return error.message

        table: str = "v_active_type" if active else "v_inactive_type"
        sql_command: str = f"""SELECT * FROM {table} WHERE type_id is ? ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command, (raw_type_id,)).fetchall()

        except self.OperationalError as error:
            debug.error(item=self, keyword="get_single_type", message=f"load types failed\n"
                                                                      f"command = {sql_command}\n"
                                                                      f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typen").message

    # member
    def get_names_of_member(self, active: bool = True) -> tuple | str:
        try:
            v.validation.must_bool(bool_=active)
        except e.NoBool as error:
            return error.message

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                          f"command = {sql_command}\n"
                                                                          f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedernamen").message

    def get_data_from_member_by_id(self, id_: int, active: bool = True) -> tuple | str:
        try:
            v.validation.must_id(id_=id_)
            v.validation.must_bool(bool_=active)
        except (e.NoId, e.NoBool) as error:
            return error.message

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID = ?;"""
        try:
            return self.cursor.execute(sql_command, (id_,)).fetchone()

        except self.OperationalError as error:
            debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdaten").message


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

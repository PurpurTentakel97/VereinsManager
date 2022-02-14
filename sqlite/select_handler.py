# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler
import sqlite3

from sqlite.database import Database
import debug

select_handler: "SelectHandler"


class SelectHandler(Database):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Select Handler"

    def get_names_of_member(self, active: bool = True) -> tuple:
        active_str: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {active_str} ORDER BY last_name ASC,first_name ASC;"""
        try:
            data = self.cursor.execute(sql_command).fetchall()
            debug.info(item=self, keyword="get_names_of_member", message=f"member names = {data}")
            return tuple(data)
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                          f"command = {sql_command}\n"
                                                                          f"error = {' '.join(error.args)}")

    def get_data_from_member_by_id(self, id_: int, active: bool = True) -> tuple:
        active_str: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {active_str} WHERE ID = {id_};"""
        try:
            data = self.cursor.execute(sql_command).fetchone()
            debug.info(item=self, keyword="get_data_from_member_by_id", message=f"member names = {data}")
            return data  # TODO move return
        except sqlite3.OperationalError as error:
            debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")

    def get_types_of_member(self, active: bool = True) -> tuple:
        active_str: str = "v_active_member_type" if active else "v_inactive_member_type"
        sql_command: str = f"""SELECT * FROM {active_str} ORDER BY type ASC,name ASC;"""

        try:
            data = self.cursor.execute(sql_command).fetchall()
            debug.info(item=self, keyword="get_types_of_member", message=f"member names = {data}")
            return data
        except sqlite3.OperationalError as error:
            debug.error(item=self, keyword="get_types_of_member", message=f"load member types failed\n"
                                                                          f"command = {sql_command}\n"
                                                                          f"error = {' '.join(error.args)}")
    #     data: tuple = (
    #         database.database.load_all_from_condition(table_name="type", condition="type", value=0),
    #         database.database.load_all_from_condition(table_name="type", condition="type", value=1),
    #         database.database.load_all_from_condition(table_name="type", condition="type", value=2),
    #         database.database.load_all_from_condition(table_name="type", condition="type", value=3),
    #     )
    #     debug.info(item="Select Handler", keyword="get_types_of_member", message=f"member types = {data}")
    #
    #     return data  # TODO move return


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

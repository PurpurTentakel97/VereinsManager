# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config.error_code import ErrorCode
import debug

update_handler: "UpdateHandler"


class UpdateHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "UpdateHandler(Database)"

    # types
    def update_type(self, id_: int, name: str) -> ErrorCode:
        # TODO Validation
        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (name, id_))
            self.connection.commit()
            return ErrorCode.UPDATE_S
        except self.OperationalError as error:
            debug.error(item=self, keyword="update_type", message=f"update type failed\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return ErrorCode.UPDATE_E

    def update_type_activity(self, id_: int, active: bool) -> ErrorCode:
        # TODO Validation
        sql_command: str = """UPDATE type SET _active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, id_))
            self.connection.commit()
            return ErrorCode.UPDATE_S
        except self.OperationalError as error:
            debug.error(item=self, keyword="update_type_activity", message=f"update type failed\n"
                                                                           f"command = {sql_command}\n"
                                                                           f"error = {' '.join(error.args)}")
            return ErrorCode.UPDATE_E


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

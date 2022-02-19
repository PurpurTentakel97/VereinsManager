# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from logic import validation as v
from config import error_code as e
import debug

update_handler: "UpdateHandler"


class UpdateHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "UpdateHandler(Database)"

    # types
    def update_type(self, id_: int, name: str) -> str | None:
        try:
            v.validation.edit_type(new_id=id_, new_name=name)
        except (e.NoInput, e.NoId, e.NoChance, e.NotFound) as error:
            return error.message

        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (name.strip().title(), id_))
            self.connection.commit()
            return
        except self.OperationalError as error:
            debug.error(item=self, keyword="update_type", message=f"update type failed\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return e.UpdateFailed(info=name).message

    def update_type_activity(self, id_: int, active: bool) -> str | None:
        try:
            v.validation.edit_type_activity(id_=id_, active=active)
        except (e.NoInput, e.NoId, e.NoChance, e.NotFound) as error:
            return error.message

        sql_command: str = """UPDATE type SET _active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (False if active else True, id_))
            self.connection.commit()
            return

        except self.OperationalError as error:
            debug.error(item=self, keyword="update_type_activity", message=f"update type failed\n"
                                                                           f"command = {sql_command}\n"
                                                                           f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

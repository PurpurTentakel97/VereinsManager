# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from logic import validation as v
from config import error_code as e
from sqlite import select_handler as s_h
import debug
from config import config_sheet as c

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
        except (e.NoStr, e.NoPositiveInt, e.NoChance, e.NotFound) as error:
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
        except (e.NoStr, e.NoPositiveInt, e.NoChance, e.NotFound) as error:
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

    # member
    def update_member(self, id_: int | None, data: dict) -> str | None:
        # validation in global handler

        result = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])
        if isinstance(result, str):
            return result
        else:
            if result:
                data["membership_type"] = result[0]
            else:
                data["membership_type"] = result

        if data["birth_date"] == c.config.date_format["None_date"]:
            data["birth_date"] = None
        if data["entry_date"] == c.config.date_format["None_date"]:
            data["entry_date"] = None

        sql_command: str = f"""Update member SET first_name = ?, last_name = ?, street = ?,number = ?,zip_code = ?,
        city = ?,b_day = ?,entry_day = ?, membership_type = ?,special_member = ?,comment = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (
                data["first_name"],
                data["last_name"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["birth_date"],
                data["entry_date"],
                data["membership_type"],
                data["special_member"],
                data["comment_text"],
                id_
            ))
            self.connection.commit()
            return
        except self.OperationalError as error:
            debug.error(item=self, keyword="update_member", message=f"update member failed\n"
                                                                    f"command = {sql_command}\n"
                                                                    f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

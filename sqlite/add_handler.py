# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation
import debug

add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> str | None:
        try:
            validation.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
        except (e.NoInput, e.NoId, e.AlreadyExists) as error:
            return error.message

        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name.strip().title(), raw_type_id))
            self.connection.commit()
            return
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.AddFailed(info=type_name).message


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()

# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from config.error_code import ErrorCode
from logic import validation
import debug

add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> ErrorCode:
        error_code: ErrorCode = validation.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
        if error_code == ErrorCode.OK_S:
            sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
            try:
                self.cursor.execute(sql_command, (type_name.strip().title(), raw_type_id))
                self.connection.commit()
                return ErrorCode.ADD_S
            except self.OperationalError as error:
                debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
                return ErrorCode.ADD_E
        else:
            return error_code


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()

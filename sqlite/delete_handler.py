# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation as v
import debug
debug_str:str = "DeleteHandler"

delete_handler: "DeleteHandler"


class DeleteHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "DeleteHandler(Database)"

    # type
    def delete_type(self, id_: int) -> str | None:
        try:
            v.validation.must_positive_int(id_)
        except e.NoPositiveInt as error:
            return error.message

        sql_command: str = """DELETE FROM type WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (id_,))
            self.connection.commit()
            return

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="delete_type", message=f"delete type failed\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return e.DeleteFailed(info="Typ").message

        except self.IntegrityError as error:
            debug.error(item=debug_str, keyword="delete_type", message=f"delete type still used\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            self.connection.commit()
            return e.ForeignKeyError(info="Typ").message


def create_delete_handler() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

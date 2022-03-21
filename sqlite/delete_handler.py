# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from sqlite import select_handler as s_h, log_handler as l_h
from config import exception_sheet as e
import debug

debug_str: str = "DeleteHandler"

delete_handler: "DeleteHandler"


class DeleteHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "DeleteHandler(Database)"

    # type
    def delete_type(self, ID: int) -> [str | None, bool]:
        sql_command: str = """DELETE FROM type WHERE ID is ?;"""
        try:
            name: str = s_h.select_handler.get_type_name_by_ID(ID=ID)
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
            result, valid = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=name[0],
                                                     new_data=None)
            if not valid:
                return result, False

            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="delete_type", message=f"delete type failed\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            return e.DeleteFailed(info="Typ").message, False

        except self.IntegrityError as error:
            debug.error(item=debug_str, keyword="delete_type", message=f"delete type still used\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            self.connection.commit()
            return e.ForeignKeyError(info="Typ").message, False


def create_delete_handler() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

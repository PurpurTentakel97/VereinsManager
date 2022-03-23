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
            l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=name[0],
                                     new_data=None)
        except self.OperationalError:
            raise e.DeleteFailed(info="Typ")

        except self.IntegrityError:
            self.connection.commit()
            raise e.ForeignKeyError(info="Typ")


def create_delete_handler() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

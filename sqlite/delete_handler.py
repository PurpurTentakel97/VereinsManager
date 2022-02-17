# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
import debug

delete_handler: "DeleteHandler"


class DeleteHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "DeleteHandler(Database)"

    # type
    def delete_type(self, id_: int) -> bool:
        sql_command: str = """DELETE FROM type WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (id_,))
            self.connection.commit()
            return True
        except self.OperationalError as error:
            debug.error(item=self, keyword="delete_type", message=f"delete type failed\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return False
        except self.IntegrityError as error:
            debug.error(item=self, keyword="delete_type", message=f"delete type still used\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return False


def create_delete_handler() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

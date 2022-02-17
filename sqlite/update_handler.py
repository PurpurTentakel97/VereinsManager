# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
import debug

update_handler: "UpdateHandler"


class UpdateHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "UpdateHandler(Database)"

    # types
    def update_type(self, id_: int, name: str) -> bool:
        sql_command: str = f"""UPDATE type SET name = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (name, id_))
            self.connection.commit()
            return True
        except self.OperationalError as error:
            debug.error(item=self, keyword="update_type", message=f"update type failed\n"
                                                                  f"command = {sql_command}\n"
                                                                  f"error = {' '.join(error.args)}")
            return False


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

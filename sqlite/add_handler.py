# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
import debug

add_handler: "AddHandler" or None = None


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> bool:
        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES ('{type_name}',{raw_type_id});"""
        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            return True
        except self.OperationalError as error:
            debug.error(item=self, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return False


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()

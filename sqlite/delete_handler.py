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

    # type
    def delete_type(self, ID: int) -> [str | None, bool]:
        sql_command: str = """DELETE FROM type WHERE ID is ?;"""
        try:
            name: tuple = s_h.select_handler.get_type_name_by_ID(ID=ID)
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
            l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=name[0],
                                     new_data=None)
        except self.OperationalError:
            error = e.DeleteFailed(info="Typ")
            debug.error(item=debug_str, keyword="delete_type", message=f"Error = {error.message}")
            raise error

        except self.IntegrityError:
            self.connection.commit()
            error = e.ForeignKeyError(info="Typ")
            debug.error(item=debug_str, keyword="delete_type", message=f"Error = {error.message}")
            raise error

    # member
    def delete_member(self, ID: int) -> None:
        sql_command: str = """DELETE FROM member WHERE ID = ?;"""
        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", message=f"delete member failed")

    # member_nexus
    def delete_member_phone(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_phone WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", message=f"delete member phone failed")

    def delete_member_mail(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_mail WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", message=f"delete member mail failed")

    def delete_member_position(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_position WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", message=f"delete member position failed")

    # user
    def delete_user(self, ID: int) -> None:
        sql_command: str = """DELETE FROM user WHERE ID = ?;"""
        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_user", message=f"delete user failed")


def create_delete_handler() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

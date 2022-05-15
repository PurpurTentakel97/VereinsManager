# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

import sys

from config import exception_sheet as e
from logic.sqlite.database import Database
from logic.sqlite import select_handler as s_h, log_handler as l_h
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
            reference_data: tuple = s_h.select_handler.get_type_name_and_extra_value_by_ID(ID=ID)
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
            l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0],
                                     new_data=None)
            l_h.log_handler.log_type(target_id=ID, target_column="extra_value", old_data=reference_data[1],
                                     new_data=None)

        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_type", error_=sys.exc_info())
            raise e.DeleteFailed(info="Typ")

        except self.IntegrityError:
            self.connection.commit()
            debug.error(item=debug_str, keyword="delete_type", error_=sys.exc_info())
            raise e.ForeignKeyError(info="Typ")

    # member
    def delete_member(self, ID: int) -> None:
        sql_command: str = """DELETE FROM member WHERE ID = ?;"""
        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", error_=sys.exc_info())

    # member_nexus
    def delete_member_phone(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_phone WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", error_=sys.exc_info())

    def delete_member_mail(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_mail WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", error_=sys.exc_info())

    def delete_member_position(self, member_id: int) -> None:
        sql_command: str = """DELETE FROM member_position WHERE member_id = ?;"""
        try:
            self.cursor.execute(sql_command, (member_id,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_member", error_=sys.exc_info())

    # user
    def delete_user(self, ID: int) -> None:
        sql_command: str = """DELETE FROM user WHERE ID = ?;"""
        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_user", error_=sys.exc_info())

    # location
    def delete_location(self, ID: int) -> None:
        sql_command: str = """DELETE from location WHERE ID IS ?;"""

        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_location", error_=sys.exc_info())
            raise e.DeleteFailed("delete Location failed")

    # schedule
    def delete_schedule_day(self, ID: int) -> None:
        sql_command: str = """DELETE FROM schedule_day WHERE ID IS ?;"""

        try:
            self.cursor.execute(sql_command, (ID,))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword=f"delete_schedule_day", error_=sys.exc_info())
            raise e.DeleteFailed("Delete Schedule Day")


def create() -> None:
    global delete_handler
    delete_handler = DeleteHandler()

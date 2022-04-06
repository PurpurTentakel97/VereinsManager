# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler
import sys

from sqlite.database import Database
from config import exception_sheet as e
import debug

debug_str: str = "UpdateHandler"

update_handler: "UpdateHandler"


class UpdateHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # types
    def update_type(self, ID: int, name: str) -> None:
        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:

            self.cursor.execute(sql_command, (name, ID))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_type", error_=sys.exc_info())
            raise e.UpdateFailed(info=name)

    def update_type_activity(self, ID: int, active: bool) -> None:
        sql_command: str = """UPDATE type SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_type_activity", error_=sys.exc_info())
            raise e.ActiveSetFailed()

    # member
    def update_member(self, ID: int | None, data: dict) -> None:
        sql_command: str = f"""Update member SET first_name = ?, last_name = ?, street = ?,number = ?,zip_code = ?,
        city = ?,maps = ?,b_day = ?,entry_day = ?, membership_type = ?,special_member = ?,comment = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (
                data["first_name"],
                data["last_name"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["maps"],
                data["birth_date"],
                data["entry_date"],
                data["membership_type"],
                data["special_member"],
                data["comment_text"],
                ID
            ))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member", error_=sys.exc_info())
            raise e.ActiveSetFailed("update member")

    def update_member_activity(self, ID: int, active: bool) -> None:
        sql_command: str = f"""UPDATE member SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID,))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_activity", error_=sys.exc_info())
            raise e.ActiveSetFailed()

    # member nexus
    def update_member_nexus_phone(self, ID: int, number: str) -> None:
        sql_command: str = f"""UPDATE member_phone SET number = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (number, ID))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_nexus_phone", error_=sys.exc_info())
            raise e.ActiveSetFailed(info=number)

    def update_member_nexus_mail(self, ID: int, mail: str) -> None:
        sql_command: str = f"""UPDATE member_mail SET mail = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (mail, ID))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_nexus_mail", error_=sys.exc_info())
            raise e.ActiveSetFailed(info=mail)

    def update_member_nexus_position(self, ID: int, active: bool) -> None:
        sql_command: str = f"""UPDATE member_position SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_nexus_position", error_=sys.exc_info())
            raise e.ActiveSetFailed(info=str(active))

    def update_member_active_phone(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_phone SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_active_phone", error_=sys.exc_info())
            raise e.UpdateFailed(info=str(active))

    def update_member_active_mail(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_mail SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_active_mail", error_=sys.exc_info())
            raise e.UpdateFailed(info=str(active))

    def update_member_active_position(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_position SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_member_active_position", error_=sys.exc_info())
            raise  e.UpdateFailed(info=str(active))

    # user
    def update_user(self, ID: int, data: dict) -> None:
        sql_command: str = """UPDATE user SET first_name = ?,last_name = ?,street = ?,number = ?,zip_code = ?,city = ?,
        phone = ?,mail = ?, position = ? WHERE ID is ?;"""

        try:
            self.cursor.execute(sql_command, (
                data["firstname"],
                data["lastname"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["phone"],
                data["mail"],
                data["position"],
                ID
            ))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_user", error_=sys.exc_info())
            raise e.ActiveSetFailed("update user")

    def update_user_password(self, ID: int, password: bytes) -> None:
        sql_command: str = """UPDATE user SET password = ? WHERE ID is ?;"""

        try:
            self.cursor.execute(sql_command, (
                password,
                ID,
            ))
            self.connection.commit()

        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_user_password", error_=sys.exc_info())
            raise e.ActiveSetFailed()

    def update_user_activity(self, ID: int, active: bool) -> None:
        sql_command: str = """UPDATE user SET _active = ? WHERE ID IS ?;"""

        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="update_user_activity", error_=sys.exc_info())
            raise e.ActiveSetFailed()


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

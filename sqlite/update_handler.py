# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

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
            error = e.UpdateFailed(info=name)
            debug.error(item=debug_str, keyword="update_type", message=f"Error = {error.message}")
            raise error

    def update_type_activity(self, ID: int, active: bool) -> None:
        sql_command: str = """UPDATE type SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed()
            debug.error(item=debug_str, keyword="update_type_activity", message=f"Error = {error.message}")
            raise error

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
            error = e.ActiveSetFailed("update member")
            debug.error(item=debug_str, keyword="update_member", message=f"Error = {error.message}")
            raise error

    def update_member_activity(self, ID: int, active: bool) -> None:
        sql_command: str = f"""UPDATE member SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID,))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed()
            debug.error(item=debug_str, keyword="update_member_activity", message=f"Error = {error.message}")
            raise error

    # member nexus
    def update_member_nexus_phone(self, ID: int, number: str) -> None:
        sql_command: str = f"""UPDATE member_phone SET number = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (number, ID))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed(info=number)
            debug.error(item=debug_str, keyword="update_member_nexus_phone", message=f"Error = {error.message}")
            raise error

    def update_member_nexus_mail(self, ID: int, mail: str) -> None:
        sql_command: str = f"""UPDATE member_mail SET mail = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (mail, ID))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed(info=mail)
            debug.error(item=debug_str, keyword="update_member_nexus_mail", message=f"Error = {error.message}")
            raise error

    def update_member_nexus_position(self, ID: int, active: bool) -> None:
        sql_command: str = f"""UPDATE member_position SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed(info=str(active))
            debug.error(item=debug_str, keyword="update_member_nexus_position", message=f"Error = {error.message}")
            raise error

    def update_member_active_phone(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_phone SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError:
            error = e.UpdateFailed(info=str(active))
            debug.error(item=debug_str, keyword="update_member_active_phone", message=f"Error= {error.message}")
            raise error

    def update_member_active_mail(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_mail SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError as error:
            error = e.UpdateFailed(info=str(active))
            debug.error(item=debug_str, keyword="update_member_active_mail", message=f"Error= {error.message}")
            raise error

    def update_member_active_position(self, member_id: int, active: bool) -> None:
        sql_command: str = """UPDATE member_position SET _active_member = ? WHERE member_id = ?"""
        try:
            self.cursor.execute(sql_command, (active, member_id))
            self.connection.commit()
        except self.OperationalError as error:
            error = e.UpdateFailed(info=str(active))
            debug.error(item=debug_str, keyword="update_member_active_position", message=f"Error= {error.message}")
            raise error

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
            error = e.ActiveSetFailed("update user")
            debug.error(item=debug_str, keyword="update_user", message=f"Error = {error.message}")
            raise error

    def update_user_password(self, ID: int, password: bytes) -> None:
        sql_command: str = """UPDATE user SET password = ? WHERE ID is ?;"""

        try:
            self.cursor.execute(sql_command, (
                password,
                ID,
            ))
            self.connection.commit()

        except self.OperationalError:
            error = e.ActiveSetFailed()
            debug.error(item=debug_str, keyword="update_user_password", message=f"Error = {error.message}")
            raise error

    def update_user_activity(self, ID: int, active: bool) -> None:
        sql_command: str = """UPDATE user SET _active = ? WHERE ID IS ?;"""

        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
        except self.OperationalError:
            error = e.ActiveSetFailed()
            debug.error(item=debug_str, keyword="update_user_activity", message=f"Error = {error.message}")
            raise error


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

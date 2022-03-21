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
    def update_type(self, ID: int, name: str) -> [str | None, bool]:
        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:

            self.cursor.execute(sql_command, (name, ID))
            self.connection.commit()
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type", message=f"update type failed\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            return e.UpdateFailed(info=name).message, False

    def update_type_activity(self, ID: int, active: bool) -> [str | None, bool]:
        sql_command: str = """UPDATE type SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type_activity", message=f"update type failed\n"
                                                                                f"command = {sql_command}\n"
                                                                                f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    # member
    def update_member(self, ID: int | None, data: dict) -> [str | None, bool]:
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
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    def update_member_activity(self, ID: int, active: bool) -> [str | None, bool]:
        sql_command: str = f"""UPDATE member SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID,))
            self.connection.commit()
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_activity", message=f"update member activity failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    # member nexus
    def update_member_nexus_phone(self, ID: int, number: str) -> [str | None, bool]:
        sql_command: str = f"""UPDATE member_phone SET number = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (number, ID))
            self.connection.commit()
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=number).message, False

    def update_member_nexus_mail(self, ID: int, mail: str) -> [str | None, bool]:
        sql_command: str = f"""UPDATE member_mail SET mail = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (mail, ID))
            self.connection.commit()
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=mail).message, False

    def update_member_nexus_position(self, ID: int, active: bool) -> [str | None, bool]:
        sql_command: str = f"""UPDATE member_position SET active = ? WHERE ID is ?;"""
        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=str(active)).message, False

    # user
    def update_user(self, ID: int, data: dict) -> [str | None, bool]:
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
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_user", message=f"update user failed\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    def update_user_password(self, ID: int, password: bytes) -> [str | None, bool]:
        sql_command: str = """UPDATE user SET password = ? WHERE ID is ?;"""

        try:
            self.cursor.execute(sql_command, (
                password,
                ID,
            ))
            self.connection.commit()
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_user_password", message=f"update user password failed\n"
                                                                                f"command = {sql_command}\n"
                                                                                f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    def update_user_activity(self, ID: int, active: bool) -> [str | None, bool]:
        sql_command: str = """UPDATE user SET _active = ? WHERE ID IS ?;"""

        try:
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_user_activity", message=f"update user activity failed\n"
                                                                                f"command = {sql_command}\n"
                                                                                f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

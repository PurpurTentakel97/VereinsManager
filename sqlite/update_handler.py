# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from logic import validation as v
from config import error_code as e
from sqlite import select_handler as s_h, log_handler as l_h
from config import config_sheet as c
import debug

debug_str: str = "UpdateHandler"

update_handler: "UpdateHandler"


class UpdateHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "UpdateHandler(Database)"

    # types
    def update_type(self, ID: int, name: str) -> [str | None, bool]:
        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_type_name_by_ID(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (name, ID))
            self.connection.commit()
            result, valid = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0],
                                                     new_data=name)
            if not valid:
                return result, False
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type", message=f"update type failed\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            return e.UpdateFailed(info=name).message, False

    def update_type_activity(self, ID: int, active: bool) -> [str | None, bool]:
        sql_command: str = """UPDATE type SET active = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_type_active_by_id(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            result, valid = l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0],
                                                     new_data=active)
            if not valid:
                return result, False
            return None, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type_activity", message=f"update type failed\n"
                                                                                f"command = {sql_command}\n"
                                                                                f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    # member
    def update_member(self, ID: int | None, data: dict, log_date: int | None) -> [str | None, bool]:
        # validation in global handler
        result, valid = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])
        if not valid:
            return result, False
        else:
            if result:
                data["membership_type"] = result[0]
            else:
                data["membership_type"] = result

        if data["birth_date"] == c.config.date_format["None_date"]:
            data["birth_date"] = None
        if data["entry_date"] == c.config.date_format["None_date"]:
            data["entry_date"] = None

        sql_command: str = f"""Update member SET first_name = ?, last_name = ?, street = ?,number = ?,zip_code = ?,
        city = ?,maps = ?,b_day = ?,entry_day = ?, membership_type = ?,special_member = ?,comment = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_member_data_by_id(ID=ID)
            if not valid:
                return reference_data, False
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
            result, valid = l_h.log_handler.log_member(target_id=ID, old_data=reference_data, new_data=data,
                                                       log_date=log_date)
            if not valid:
                return result, False
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    def update_member_activity(self, ID: int, active: bool, log_date: int | None) -> [str | None, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoPositiveInt, e.NoBool) as error:
            debug.error(item=debug_str, keyword="update_member_activity", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""UPDATE member SET active = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_member_activity_by_id(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (
                active,
                ID,
            ))
            self.connection.commit()
            result, valid = l_h.log_handler.log_member_activity(target_id=ID, old_activity=reference_data,
                                                                new_activity=active,
                                                                log_date=log_date)
            if not valid:
                return result, False
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_activity", message=f"update member activity failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message, False

    # member nexus
    def update_member_nexus_phone(self, ID: int, number: str, log_date: int) -> [str | None, bool]:
        # validation in global handler
        sql_command: str = f"""UPDATE member_phone SET number = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_phone_number_by_ID(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (number, ID))
            self.connection.commit()
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=number,
                                                             log_date=log_date, type_="phone")
            if not valid:
                return result, False
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=number).message, False

    def update_member_nexus_mail(self, ID: int, mail: str, log_date: int) -> [str | None, bool]:
        # validation in global handler
        sql_command: str = f"""UPDATE member_mail SET mail = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_mail_member_by_ID(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (mail, ID))
            self.connection.commit()
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=mail,
                                                             log_date=log_date, type_="mail")
            if not valid:
                return result, False
            return None, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=mail).message, False

    def update_member_nexus_position(self, ID: int, active: bool, log_date: int) -> [str | None, bool]:
        # validation in global handler
        sql_command: str = f"""UPDATE member_position SET active = ? WHERE ID is ?;"""
        try:
            reference_data, valid = s_h.select_handler.get_position_member_by_ID(ID=ID)
            if not valid:
                return reference_data, False
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=active,
                                                             log_date=log_date, type_="position")
            if not valid:
                return result, False
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

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
    def update_type(self, ID: int, name: str) -> str | None:
        name = name.strip().title()
        try:
            v.validation.update_type(ID=ID, new_name=name)
        except (e.NoStr, e.NoInt, e.NoPositiveInt, e.NoChance, e.NotFound, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_type", message=f"Error 0 {error.message}")
            return error.message

        sql_command: str = """UPDATE type SET name = ? WHERE ID is ?;"""
        try:
            reference_data: tuple = s_h.select_handler.get_type_name_by_id(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (name, ID))
            self.connection.commit()
            result = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=reference_data[0],
                                              new_data=name)
            if isinstance(result, str):
                return result
            return
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type", message=f"update type failed\n"
                                                                       f"command = {sql_command}\n"
                                                                       f"error = {' '.join(error.args)}")
            return e.UpdateFailed(info=name).message

    def update_type_activity(self, ID: int, active: bool) -> str | None:
        try:
            v.validation.update_type_activity(ID=ID, active=active)
        except (e.NoStr, e.NoPositiveInt, e.NoChance, e.NotFound, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_type_activity", message=f"Error = {error.message}")
            return error.message

        sql_command: str = """UPDATE type SET active = ? WHERE ID is ?;"""
        try:
            reference_data: tuple = s_h.select_handler.get_type_active_by_id(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            result = l_h.log_handler.log_type(target_id=ID, target_column="active", old_data=reference_data[0],
                                              new_data=active)
            if isinstance(result, str):
                return result
            return

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_type_activity", message=f"update type failed\n"
                                                                                f"command = {sql_command}\n"
                                                                                f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message

    # member
    def update_member(self, ID: int | None, data: dict, log_date: int | None) -> str | None:
        # validation in global handler
        result = s_h.select_handler.get_id_by_type_name(raw_id=1, name=data["membership_type"])
        if isinstance(result, str):
            return result
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
        city = ?,b_day = ?,entry_day = ?, membership_type = ?,special_member = ?,comment = ? WHERE ID is ?;"""
        try:
            reference_data: dict = s_h.select_handler.get_member_data_by_id(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (
                data["first_name"],
                data["last_name"],
                data["street"],
                data["number"],
                data["zip_code"],
                data["city"],
                data["birth_date"],
                data["entry_date"],
                data["membership_type"],
                data["special_member"],
                data["comment_text"],
                ID
            ))
            self.connection.commit()
            l_h.log_handler.log_member(target_id=ID, old_data=reference_data, new_data=data, log_date=log_date)
            return
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message

    def update_member_activity(self, ID: int, active: bool, log_date: int | None) -> str | None:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoPositiveInt, e.NoBool) as error:
            debug.error(item=debug_str, keyword="update_member_activity", message=f"Error = {error.message}")
            return error.message

        sql_command: str = f"""UPDATE member SET active = ? WHERE ID is ?;"""
        try:
            reference_data = s_h.select_handler.get_member_activity_from_id(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (
                active,
                ID,
            ))
            self.connection.commit()
            result = l_h.log_handler.log_member_activity(target_id=ID, old_activity=reference_data, new_activity=active,
                                                         log_date=log_date)
            if isinstance(result, str):
                return result
            return
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_activity", message=f"update member activity failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message

    # member nexus
    def update_member_nexus_phone(self, ID: int, number: str, log_date: int) -> str or None:
        # validation in global handler
        sql_command: str = f"""UPDATE member_phone SET number = ? WHERE ID is ?;"""
        try:
            reference_data = s_h.select_handler.get_phone_number_by_ID(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (number, ID))
            self.connection.commit()
            result = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=number,
                                                      log_date=log_date, type_="phone")
            if isinstance(result, str):
                return result
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=number).message

    def update_member_nexus_mail(self, ID: int, mail: str, log_date: int) -> str or None:
        # validation in global handler
        sql_command: str = f"""UPDATE member_mail SET mail = ? WHERE ID is ?;"""
        try:
            reference_data = s_h.select_handler.get_mail_member_by_ID(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (mail, ID))
            self.connection.commit()
            result = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=mail,
                                                      log_date=log_date, type_="mail")
            if isinstance(result, str):
                return result
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=mail).message

    def update_member_nexus_position(self, ID: int, active: bool, log_date: int) -> str or None:
        # validation in global handler
        sql_command: str = f"""UPDATE member_position SET active = ? WHERE ID is ?;"""
        try:
            reference_data = s_h.select_handler.get_position_member_by_ID(ID=ID)
            if isinstance(reference_data, str):
                return reference_data
            self.cursor.execute(sql_command, (active, ID))
            self.connection.commit()
            result = l_h.log_handler.log_member_nexus(target_id=ID, old_data=reference_data[0], new_data=active,
                                                      log_date=log_date, type_="position")
            if isinstance(result,str):
                return result
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member_nexus", message=f"update member nexus failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed(info=str(active)).message


def crate_update_handler() -> None:
    global update_handler
    update_handler = UpdateHandler()

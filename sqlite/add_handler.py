# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from sqlite import select_handler as s_h, log_handler as l_h
from config import error_code as e, config_sheet as c
from logic import validation
import debug

debug_str: str = "AddHandler"
add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> str | int:
        try:
            validation.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
        except (e.NoStr, e.NoInt, e.NoPositiveInt, e.AlreadyExists) as error:
            return error.message

        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name.strip().title(), raw_type_id))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            result = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=None, new_data=type_name)
            if isinstance(result, str):
                return result
            return ID
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_id",
                        message=f"load single member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.AddFailed(info=type_name).message

    # member
    def add_member(self, data: dict) -> int | str:
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

        sql_command: str = f"""INSERT INTO member 
        (first_name,last_name,street,number,zip_code,city,b_day,entry_day,membership_type,special_member,comment) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?);"""

        try:
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
            ))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member", message=f"add member failed\n"
                                                                      f"command = {sql_command}\n"
                                                                      f"error = {' '.join(error.args)}")
            return e.AddFailed().message

    # member nexus
    def add_member_nexus_phone(self, type_id: int, value: str, member_id: int) -> int or str:
        sql_command: str = f"""INSERT INTO member_phone (member_id, type_id, number) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_phone", message=f"add member nexus failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.AddFailed(info=value).message

    def add_member_nexus_mail(self, type_id: int, value: str, member_id: int) -> int or str:
        sql_command: str = f"""INSERT INTO member_mail (member_id, type_id, mail) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_mail", message=f"add member nexus failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.AddFailed(info=value).message

    def add_member_nexus_position(self, type_id: int, value: bool, member_id: int) -> int or str:
        sql_command: str = f"""INSERT INTO member_position (member_id, type_id, active) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            return self.cursor.lastrowid
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_position", message=f"add member nexus failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
            return e.AddFailed(info=str(value)).message


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()

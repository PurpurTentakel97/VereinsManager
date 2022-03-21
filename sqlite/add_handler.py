# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from sqlite import select_handler as s_h, log_handler as l_h
from config import exception_sheet as e, config_sheet as c
import debug

debug_str: str = "AddHandler"
add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> [str | int, bool]:
        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name, raw_type_id))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            result, valid = l_h.log_handler.log_type(target_id=ID, target_column="name", old_data=None,
                                                     new_data=type_name)
            if not valid:
                return result, False

            member_ids, valid = s_h.select_handler.get_all_IDs_from_member(active=True)
            if not valid:
                return member_ids, False
            function_ = None
            value = None
            if raw_type_id == c.config.raw_type_id["phone"]:
                function_ = self.add_member_nexus_phone
            elif raw_type_id == c.config.raw_type_id["mail"]:
                function_ = self.add_member_nexus_mail
            elif raw_type_id == c.config.raw_type_id["position"]:
                function_ = self.add_member_nexus_position
                value = False
            for member_id in member_ids:
                member_id = member_id[0]
                result, valid = function_(type_id=ID, value=value, member_id=member_id, log_date=None)
                if not valid:
                    return result, False
            return ID, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_id",
                        message=f"load single member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.AddFailed(info=type_name).message, False

    # member
    def add_member(self, data: dict, log_date: int | None) -> [int | str, bool]:
        sql_command: str = f"""INSERT INTO member 
        (first_name,last_name,street,number,zip_code,city,maps,b_day,entry_day,membership_type,special_member,comment) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""

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
            ))
            self.connection.commit()
            ID = self.cursor.lastrowid
            result, valid = l_h.log_handler.log_member(target_id=ID, old_data=None, new_data=data, log_date=log_date)
            if not valid:
                return result
            return ID, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member", message=f"add member failed\n"
                                                                      f"command = {sql_command}\n"
                                                                      f"error = {' '.join(error.args)}")
            return e.AddFailed().message, False

    # member nexus
    def add_member_nexus_phone(self, type_id: int, value: str, member_id: int, log_date: int | None) \
            -> [int or str, bool]:
        sql_command: str = f"""INSERT INTO member_phone (member_id, type_id, number) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value,
                                                             log_date=log_date,
                                                             type_="phone")
            if not valid:
                return result, False
            return ID, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_phone", message=f"add member nexus failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.AddFailed(info=value).message, False

    def add_member_nexus_mail(self, type_id: int, value: str, member_id: int, log_date: int | None) \
            -> [int or str, bool]:
        sql_command: str = f"""INSERT INTO member_mail (member_id, type_id, mail) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value,
                                                             log_date=log_date,
                                                             type_="mail")
            if not valid:
                return result, False
            return ID, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_mail", message=f"add member nexus failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.AddFailed(info=value).message, False

    def add_member_nexus_position(self, type_id: int, value: bool, member_id: int, log_date: int | None) \
            -> [int or str, bool]:
        sql_command: str = f"""INSERT INTO member_position (member_id, type_id, active) VALUES (?,?,?);"""
        try:
            self.cursor.execute(sql_command, (member_id, type_id, value))
            self.connection.commit()
            ID: int = self.cursor.lastrowid
            result, valid = l_h.log_handler.log_member_nexus(target_id=ID, old_data=None, new_data=value,
                                                             log_date=log_date,
                                                             type_="position")
            if not valid:
                return result, False
            return ID, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_member_nexus_position", message=f"add member nexus failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
            return e.AddFailed(info=str(value)).message, False

    # user
    def add_user(self, data: dict) -> [int | str, bool]:
        sql_command: str = """INSERT INTO user (first_name,last_name,street,number,zip_code,city,phone,mail,
        position,password) VALUES (?,?,?,?,?,?,?,?,?,?);"""

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
                data["password_hashed"],
            ))
            self.connection.commit()
            return self.cursor.lastrowid, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="add_user", message=f"add user failed\n"
                                                                    f"command = {sql_command}\n"
                                                                    f"error = {' '.join(error.args)}")
            return e.AddFailed().message, False


def create_add_handler() -> None:
    global add_handler
    add_handler = AddHandler()

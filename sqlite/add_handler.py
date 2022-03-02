# Purpur Tentakel
# 13.02.2022
# VereinsManager / Add Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation
import debug
debug_str:str = "AddHandler"
add_handler: "AddHandler"


class AddHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "AddHandler(Database)"

    # type
    def add_type(self, type_name: str, raw_type_id: int) -> str | None:
        try:
            validation.validation.add_type(type_name=type_name, raw_type_id=raw_type_id)
        except (e.NoStr, e.NoPositiveInt, e.AlreadyExists) as error:
            return error.message

        sql_command: str = f"""INSERT INTO type (name,type_id) VALUES (?,?);"""
        try:
            self.cursor.execute(sql_command, (type_name.strip().title(), raw_type_id))
            self.connection.commit()
            return
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_id", message=f"load single member data failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.AddFailed(info=type_name).message

    # member
    def add_member(self) -> int | str:
        sql_command: str = f"""INSERT INTO member (first_name) VALUES (?);"""
        try:
            self.cursor.execute(sql_command, (None,))
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
        sql_command: str = f"""INSERT INTO member_position (member_id, type_id, _active) VALUES (?,?,?);"""
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

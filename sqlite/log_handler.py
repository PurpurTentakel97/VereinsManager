# Purpur Tentakel
# 13.02.2022
# VereinsManager / Log Handler

import time

from sqlite.database import Database
from config import error_code as e, config_sheet as c
from logic import validation as v
from sqlite import select_handler as s_h

import debug

debug_str: str = "Log Handler"

log_handler: "LogHandler"


class LogHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def log_type(self, target_id: int, target_column: str, old_data, new_data) -> str | None:
        log_date = self.transform_log_none_date(none_date=None)
        try:
            v.validation.must_positive_int(target_id, max_length=None)
            v.validation.must_str(target_column)
        except (e.NoInt, e.NoPositiveInt, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="log_type", message=f"Error = {error.message}")

        return self._log(target_table="type", target_id=target_id, target_column=target_column, old_data=old_data,
                         new_data=new_data, log_date=log_date)

    # member
    def log_member(self, ID: int, old_data: dict | None, new_data: dict, log_date: int | None) -> str | None:
        log_date = self.transform_log_none_date(none_date=log_date)
        try:
            v.validation.must_int(int_=log_date)
        except (e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="log_member", message=f"Error = {error.message}")
            return error.message

        if old_data:
            return self._log_member(ID=ID, old_data=old_data, new_data=new_data, log_date=log_date)
        else:
            return self._log_initial_member(ID=ID, new_data=new_data, log_date=log_date)

    def _log_member(self, ID: int, old_data: dict, new_data: dict, log_date: int) -> str | None:
        # transform none date to none
        if old_data["birth_date"] == c.config.date_format["None_date"]:
            old_data["birth_date"] = None
        if old_data["entry_date"] == c.config.date_format["None_date"]:
            old_data["entry_date"] = None

        # transform membership to ID
        result = s_h.select_handler.get_id_by_type_name(raw_id=1, name=old_data["membership_type"])
        if isinstance(result, str):
            return result
        else:
            if result:
                old_data["membership_type"] = result[0]
            else:
                old_data["membership_type"] = result

        keys: tuple = (
            "first_name",
            "last_name",
            "street",
            "number",
            "zip_code",
            "birth_date",
            "entry_date",
            "city",
            "membership_type",
            "special_member",
            "comment_text",
        )

        for key in keys:
            if old_data[key] != new_data[key]:
                result = self._log(target_table="member", target_id=ID, target_column=key,
                                   old_data=old_data[key], new_data=new_data[key], log_date=log_date)
                if isinstance(result, str):
                    return result

    def _log_initial_member(self, ID: int, new_data: dict, log_date: int) -> str | None:
        result = self._log(target_table="member", target_id=ID, target_column="active", old_data=None, new_data=True,
                           log_date=log_date)
        if isinstance(result, str):
            return result

        keys: tuple = (
            "first_name",
            "last_name",
            "street",
            "number",
            "zip_code",
            "birth_date",
            "entry_date",
            "city",
            "membership_type",
            "special_member",
            "comment_text",
        )

        for key in keys:
            if new_data[key]:
                result = self._log(target_table="member", target_id=ID, target_column=key, old_data=None,
                                   new_data=new_data[key], log_date=log_date)
                if isinstance(result, str):
                    return result

    def log_member_activity(self, ID: int, old_activity: bool, new_activity: bool, log_date: int) -> str | None:
        log_date = self.transform_log_none_date(none_date=log_date)
        try:
            v.validation.must_int(int_=log_date)
        except (e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="log_member", message=f"Error = {error.message}")
            return error.message

        try:
            v.validation.must_bool(old_activity)
            v.validation.must_bool(new_activity)
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong, e.NoBool) as error:
            debug.error(item=debug_str, keyword="log_member_activity", message=f"Error = {error.message}")
            return error.message

        if old_activity != new_activity:
            result = self._log(target_id=ID, target_table="member", target_column="active", old_data=old_activity,
                               new_data=new_activity, log_date=log_date)
            if isinstance(result, str):
                return result

    # log member nexus
    def log_member_nexus(self, ID: int, old_data: str | bool | None, new_data: str | int | None, log_date: int | None,
                         type_: str) -> str | None:
        log_date = self.transform_log_none_date(none_date=log_date)
        match type_:
            case "phone":
                if old_data != new_data:
                    return self._log(target_table="member_phone", target_id=ID, target_column="number",
                                     old_data=old_data,
                                     new_data=new_data, log_date=log_date)
            case "mail":
                if old_data != new_data:
                    return self._log(target_table="member_mail", target_id=ID, target_column="mail", old_data=old_data,
                                     new_data=new_data, log_date=log_date)
            case "position":
                if old_data != new_data:
                    return self._log(target_table="member_position", target_id=ID, target_column="position",
                                     old_data=old_data, new_data=new_data, log_date=log_date)

    # log
    def _log(self, target_table: str, target_id: int, target_column: str, old_data, new_data,
             log_date: int) -> str | None:
        sql_command: str = f"""INSERT INTO log (target_table,target_id,target_column,old_data,new_data,log_date) 
        VALUES (?, ?, ?, ?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (target_table, target_id, target_column, old_data, new_data, log_date))
            self.connection.commit()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="update_member", message=f"update member failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.ActiveSetFailed().message

    # general
    @staticmethod
    def transform_log_none_date(none_date: int | None) -> int:
        if not none_date:
            none_date = int(time.time())
        return none_date


def create_log_handler() -> None:
    global log_handler
    log_handler = LogHandler()

# Purpur Tentakel
# 13.02.2022
# VereinsManager / Log Handler

import sys
import time

from helper import validation
from logic.sqlite.database import Database
from logic.sqlite import select_handler as s_h
from config import exception_sheet as e, config_sheet as c

import debug

debug_str: str = "Log Handler"

log_handler: "LogHandler"


class LogHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def log_type(self, target_id: int, target_column: str, old_data, new_data) -> None:
        log_date = self.transform_log_none_date(none_date=None)

        if old_data == new_data:
            return

        validation.must_positive_int(target_id, max_length=None)
        validation.must_int(int_=log_date)
        validation.must_str(target_column)

        self._log(target_table="type", target_id=target_id, target_column=target_column, old_data=old_data,
                  new_data=new_data, log_date=log_date)

    # member
    def log_member(self, target_id: int, old_data: dict | None, new_data: dict, log_date: int | None) -> None:
        log_date = self.transform_log_none_date(none_date=log_date)

        validation.must_int(int_=log_date)

        if old_data:
            self._log_member(target_id=target_id, old_data=old_data, new_data=new_data, log_date=log_date)
        else:
            self._log_initial_member(target_id=target_id, new_data=new_data, log_date=log_date)

    def _log_member(self, target_id: int, old_data: dict, new_data: dict, log_date: int) -> None:
        old_data["birth_date"] = self.transform_none_date_to_none(old_data["birth_date"])
        old_data["entry_date"] = self.transform_none_date_to_none(old_data["entry_date"])
        old_data = self.transform_type_to_id(key="membership_type", data=old_data)
        old_data = self.transform_type_to_id(key="country", data=old_data)

        keys: tuple = (
            "first_name",
            "last_name",
            "street",
            "number",
            "zip_code",
            "birth_date",
            "entry_date",
            "city",
            "country",
            "maps",
            "membership_type",
            "special_member",
            "comment_text",
        )

        for key in keys:
            if old_data[key] != new_data[key]:
                self._log(target_table="member", target_id=target_id, target_column=key,
                          old_data=old_data[key], new_data=new_data[key], log_date=log_date)

    def _log_initial_member(self, target_id: int, new_data: dict, log_date: int) -> None:
        self._log(target_table="member", target_id=target_id, target_column="active", old_data=None,
                  new_data=True, log_date=log_date)

        keys: tuple = (
            "first_name",
            "last_name",
            "street",
            "number",
            "zip_code",
            "birth_date",
            "entry_date",
            "city",
            "country",
            "maps",
            "membership_type",
            "special_member",
            "comment_text",
        )

        for key in keys:
            if new_data[key]:
                self._log(target_table="member", target_id=target_id, target_column=key, old_data=None,
                          new_data=new_data[key], log_date=log_date)

    def log_member_activity(self, target_id: int, old_activity: bool, new_activity: bool, log_date: int) -> None:
        log_date = self.transform_log_none_date(none_date=log_date)

        validation.must_int(int_=log_date)
        validation.must_bool(old_activity)
        validation.must_bool(new_activity)

        if old_activity != new_activity:
            self._log(target_id=target_id, target_table="member", target_column="active",
                      old_data=old_activity,
                      new_data=new_activity, log_date=log_date)

    # log member nexus
    def log_member_nexus(self, target_id: int, old_data: str | bool | None, new_data: str | int | None,
                         log_date: int | None, type_: str) -> None:
        log_date = self.transform_log_none_date(none_date=log_date)

        validation.must_int(int_=log_date)

        match type_:
            case "phone":
                if old_data != new_data:
                    self._log(target_table="member_phone", target_id=target_id, target_column="number",
                              old_data=old_data,
                              new_data=new_data, log_date=log_date)
            case "mail":
                if old_data != new_data:
                    self._log(target_table="member_mail", target_id=target_id, target_column="mail",
                              old_data=old_data,
                              new_data=new_data, log_date=log_date)
            case "position":
                if old_data != new_data:
                    self._log(target_table="member_position", target_id=target_id, target_column="position",
                              old_data=old_data, new_data=new_data, log_date=log_date)

    # log
    def _log(self, target_table: str, target_id: int, target_column: str, old_data, new_data,
             log_date: int) -> None:
        sql_command: str = f"""INSERT INTO log (target_table,target_id,target_column,old_data,new_data,log_date) 
        VALUES (?, ?, ?, ?, ?, ?);"""
        try:
            self.cursor.execute(sql_command, (target_table, target_id, target_column, old_data, new_data, log_date))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="_log", error_=sys.exc_info())
            raise e.AddFailed("Log failed")

    # delete
    def delete_log(self, target_id: int, target_table: str) -> None:
        sql_command: str = """DELETE FROM log WHERE target_id = ? AND target_table = ?;"""
        try:
            self.cursor.execute(sql_command, (target_id, target_table))
            self.connection.commit()
        except self.OperationalError:
            debug.error(item=debug_str, keyword="delete_log",
                        error_=sys.exc_info())

    # helper
    @staticmethod
    def transform_log_none_date(none_date: int | None) -> int:
        if not none_date:
            none_date = int(time.time())
        return none_date

    @staticmethod
    def transform_none_date_to_none(date):
        if date == c.config.date_format["None_date"]:
            date = None
        return date

    @staticmethod
    def transform_type_to_id(key: str, data: dict) -> dict:
        type_id: tuple = tuple()
        match key:
            case "membership_type":
                type_id = s_h.select_handler.get_id_by_type_name(raw_id=c.config.raw_type_id["membership"],
                                                                 name=data[key])
            case "country":
                type_id = s_h.select_handler.get_id_by_type_name(raw_id=c.config.raw_type_id["country"],
                                                                 name=data[key])
        if type_id:
            data[key] = type_id[0]
        else:
            data[key] = type_id
        return data


def create() -> None:
    global log_handler
    log_handler = LogHandler()

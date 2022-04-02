# Purpur Tentakel
# 29.03.2022
# VereinsManager / Statistics Handler

from datetime import date, datetime

from config import exception_sheet as e
from sqlite.database import Database
import debug

debug_str: str = "StatisticsHandler"

statistics_handler: "StatisticsHandler"


class StatisticsHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    def statistics(self, type_: str, raw_type_id: int, new_type_id: int | None, old_type_id: int | None = None,
                   old_data=None, new_data=None) -> None:
        try:
            match type_:
                case "membership":
                    self._membership_statistics(raw_type_id=raw_type_id, new_type_id=new_type_id,
                                                old_type_id=old_type_id)
                case "phone":
                    self._member_nexus_statistics(type_=type_, raw_type_id=raw_type_id, new_type_id=new_type_id,
                                                  old_data=old_data, new_data=new_data)
                case "mail":
                    self._member_nexus_statistics(type_=type_, raw_type_id=raw_type_id, new_type_id=new_type_id,
                                                  old_data=old_data, new_data=new_data)
                case "position":
                    self._member_nexus_statistics(type_=type_, raw_type_id=raw_type_id, new_type_id=new_type_id,
                                                  old_data=old_data, new_data=new_data)
                case _:
                    raise e.CaseException(info=f"statistic type // {type_}")

        except e.GeneralError as error:
            debug.error(item=debug_str, keyword="statistics", message=f"Error = {error.message}")

    def _membership_statistics(self, raw_type_id: int, new_type_id: int | None, old_type_id: int | None) -> None:
        if not self._is_valid_membership(new_membership_id=new_type_id, old_membership_id=old_type_id):
            return

        new_count, old_count = self._get_current_membership_counts(new_type_id=new_type_id, old_type_id=old_type_id)

        self._statistics(raw_type_id=raw_type_id, type_id=new_type_id, count=new_count)
        self._statistics(raw_type_id=raw_type_id, type_id=old_type_id, count=old_count)

    def _member_nexus_statistics(self, type_: str, raw_type_id: int, new_type_id: int | None, old_data,
                                 new_data) -> None:
        if new_type_id is None:
            return
        if not self._is_valid_data(data_1=old_data, data_2=new_data):
            return

        count = self._get_current_nexus_count(type_=type_, type_id=new_type_id)

        self._statistics(raw_type_id=raw_type_id, type_id=new_type_id, count=count)

    def _statistics(self, raw_type_id: int, type_id: int, count: int) -> None:
        if type_id is None:
            return

        current_entry = self._get_current_ID(type_id)

        if not current_entry:
            self._add(raw_type_id=raw_type_id, type_id=type_id, count=count)
            return
        self._update(ID=current_entry[0], count=count)

    def _add(self, raw_type_id: int, type_id: int, count: int) -> None:
        if type_id is None:
            return

        sql_command: str = """INSERT INTO statistics (_log_date, raw_type_id, type_id, count) VALUES (?, ?, ?, ?)"""
        try:
            today = date.today()
            self.cursor.execute(sql_command, (
                datetime.timestamp(datetime(today.year, today.month, today.day)),
                raw_type_id,
                type_id,
                count,
            ))
            self.connection.commit()
        except self.OperationalError:
            debug.debug(item=debug_str, keyword="_statistics", message=f"add statistics failed")

    def _update(self, ID: int, count: int) -> None:
        sql_command: str = """UPDATE statistics SET count = ? WHERE ID = ?;"""
        try:
            self.cursor.execute(sql_command, (count, ID))
            self.connection.commit()
        except self.OperationalError:
            debug.debug(item=debug_str, keyword="_statistics", message=f"update statistics failed")

    def _get_current_ID(self, type_id):
        sql_command: str = """SELECT * FROM statistics WHERE _log_date = ? and type_id = ?;"""
        try:
            today = date.today()
            return self.cursor.execute(sql_command, (
                datetime.timestamp(datetime(today.year, today.month, today.day)),
                type_id,
            )).fetchone()
        except self.OperationalError:
            debug.debug(item=debug_str, keyword="_statistics", message=f"get current statistic failed")

    def _get_current_membership_counts(self, new_type_id: int, old_type_id: int) -> [int]:
        sql_command: str = """SELECT membership_type FROM v_active_member WHERE membership_type is ?;"""
        try:
            counts: list = list()
            for type_id in [new_type_id, old_type_id]:
                list_ = self.cursor.execute(sql_command, (type_id,)).fetchall()
                if list_ is None:
                    counts.append(0)
                else:
                    counts.append(len(list_))
            return counts
        except self.OperationalError:
            debug.debug(item=debug_str, keyword="_statistics", message=f"select statistic count failed")

    def _get_current_nexus_count(self, type_: str, type_id: int) -> int:
        match type_:
            case "phone":
                sql_command: str = """SELECT number FROM member_phone WHERE type_id is ? and _active_member is ?;"""
            case "mail":
                sql_command: str = """SELECT mail FROM member_mail WHERE type_id is ? and _active_member is ?;"""
            case "position":
                sql_command: str = """SELECT active FROM member_position WHERE type_id is ? and _active_member is ?;"""
            case _:
                raise e.CaseException(info=f"nexus type // {type_}")

        try:
            data = self.cursor.execute(sql_command, (type_id, True)).fetchall()
            counter: int = 0
            for value, *_ in data:
                if value:
                    counter += 1
            return counter
        except self.OperationalError as error:
            debug.debug(item=debug_str, keyword="_get_current_nexus_count",
                        message=f"Command: {sql_command}\nError: {str(error)}")

    @staticmethod
    def _is_valid_data(data_1, data_2) -> bool:
        if not data_1 and not data_2:
            return False
        elif data_1 and data_2:
            return False
        return True

    @staticmethod
    def _is_valid_membership(new_membership_id: int, old_membership_id: int) -> bool:
        if new_membership_id != old_membership_id:
            return True
        return False


def create_statistics_handler() -> None:
    global statistics_handler
    statistics_handler = StatisticsHandler()

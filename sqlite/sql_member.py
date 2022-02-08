# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Member

import datetime

from enum_sheet import TableTypes, MemberTypes
import enum_sheet

database_member: "DatabaseMember" or None = None


class DatabaseMember:
    def __init__(self, database):
        self.database = database

    def create_member_table(self) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER.value}" (
            "{MemberTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
            "{MemberTypes.FIRST_NAME.value}"	TEXT,
            "{MemberTypes.LAST_NAME.value}"	TEXT,
            "{MemberTypes.STREET.value}"	TEXT,
            "{MemberTypes.NUMBER.value}"	TEXT,
            "{MemberTypes.ZIP_CODE.value}"	INTEGER,
            "{MemberTypes.CITY.value}"	TEXT,
            "{MemberTypes.B_DAY_DATE.value}"	TEXT,
            "{MemberTypes.ENTRY_DATE.value}"	TEXT,
            "{MemberTypes.MEMBERSHIP_TYPE.value}"	TEXT,
            "{MemberTypes.SPECIAL_MEMBER.value}"	INTEGER,
            "{MemberTypes.COMMENT.value}"	TEXT,
            "{MemberTypes.ACTIVE_MEMBER.value}" INTEGER,
            PRIMARY KEY("{MemberTypes.ID.value}" AUTOINCREMENT));"""

        self.database.create(sql_command)

    def save_member(self, output: dict) -> int:
        sql_command: str = f"""INSERT INTO "{TableTypes.MEMBER.value}" (
        "{MemberTypes.FIRST_NAME.value}", 
        "{MemberTypes.LAST_NAME.value}", 
        "{MemberTypes.STREET.value}", 
        "{MemberTypes.NUMBER.value}", 
        "{MemberTypes.ZIP_CODE.value}", 
        "{MemberTypes.CITY.value}", 
        "{MemberTypes.B_DAY_DATE.value}", 
        "{MemberTypes.ENTRY_DATE.value}", 
        "{MemberTypes.MEMBERSHIP_TYPE.value}", 
        "{MemberTypes.SPECIAL_MEMBER.value}", 
        "{MemberTypes.COMMENT.value}",
        "{MemberTypes.ACTIVE_MEMBER.value}") VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""

        values: tuple = (
            output[MemberTypes.FIRST_NAME.value] or None,
            output[MemberTypes.LAST_NAME.value] or None,
            output[MemberTypes.STREET.value] or None,
            output[MemberTypes.NUMBER.value] or None,
            output[MemberTypes.ZIP_CODE.value] or None,
            output[MemberTypes.CITY.value] or None,
            output[MemberTypes.B_DAY_DATE.value].strftime(enum_sheet.date_format) \
                if output[MemberTypes.B_DAY_DATE.value] is not None else None,
            output[MemberTypes.ENTRY_DATE.value].strftime(enum_sheet.date_format) \
                if output[MemberTypes.ENTRY_DATE.value] is not None else None,
            output[MemberTypes.MEMBERSHIP_TYPE.value] or None,
            output[MemberTypes.SPECIAL_MEMBER.value],
            output[MemberTypes.COMMENT.value] or None,
            True)

        return self.database.insert(sql_command=sql_command, values=values)

    def update_member(self, output: dict) -> None:
        sql_command: str = f"""UPDATE {TableTypes.MEMBER.value}
        SET {MemberTypes.FIRST_NAME.value} = ?,
        {MemberTypes.LAST_NAME.value} = ?,
        {MemberTypes.STREET.value} = ?,
        {MemberTypes.NUMBER.value} = ?,
        {MemberTypes.ZIP_CODE.value} = ?,
        {MemberTypes.CITY.value} = ?,
        {MemberTypes.B_DAY_DATE.value} = ?,
        {MemberTypes.ENTRY_DATE.value} = ?,
        {MemberTypes.MEMBERSHIP_TYPE.value} = ?,
        {MemberTypes.SPECIAL_MEMBER.value} = ?,
        {MemberTypes.COMMENT.value} = ?
        WHERE {MemberTypes.ID.value} = ?;"""

        values: tuple = (
            output[MemberTypes.FIRST_NAME.value] or None,
            output[MemberTypes.LAST_NAME.value] or None,
            output[MemberTypes.STREET.value] or None,
            output[MemberTypes.NUMBER.value] or None,
            output[MemberTypes.ZIP_CODE.value] or None,
            output[MemberTypes.CITY.value] or None,
            output[MemberTypes.B_DAY_DATE.value].strftime(enum_sheet.date_format) \
                if output[MemberTypes.B_DAY_DATE.value] is not None else None,
            output[MemberTypes.ENTRY_DATE.value].strftime(enum_sheet.date_format) \
                if output[MemberTypes.ENTRY_DATE.value] is not None else None,
            output[MemberTypes.MEMBERSHIP_TYPE.value] or None,
            output[MemberTypes.SPECIAL_MEMBER.value],
            output[MemberTypes.COMMENT.value] or None,
            output[MemberTypes.ID.value])

        self.database.update(sql_command=sql_command, values=values)

    def delete_recover_member(self, member_id: int, active: bool) -> None:
        sql_command: str = f"""UPDATE {TableTypes.MEMBER.value}
        SET {MemberTypes.ACTIVE_MEMBER.value} = ? 
        WHERE {MemberTypes.ID.value} = ?;"""
        values: tuple = (active, member_id)

        self.database.update(sql_command=sql_command, values=values)

    def load_all_member_names(self, active: bool) -> list:
        sql_command: str = f"""SELECT {MemberTypes.ID.value}, 
        {MemberTypes.FIRST_NAME.value}, 
        {MemberTypes.LAST_NAME.value} 
        FROM {TableTypes.MEMBER.value} 
        WHERE {MemberTypes.ACTIVE_MEMBER.value} LIKE {active};"""

        return self.database.select_all(sql_command=sql_command)

    def load_all_data_from_member(self, id_: int) -> list:
        sql_command: str = f"""SELECT * FROM '{TableTypes.MEMBER.value}' WHERE {MemberTypes.ID.value} = {id_}"""

        data = self.database.select_one(sql_command=sql_command)
        data = list(data)

        for i in range(1, len(data)):
            if data[i] == 1:
                data[i] = True
            elif data[i] == 0:
                data[i] = False

        return data

    def load_data_from_single_member(self, id_: int) -> list:
        data = self.load_all_data_from_member(id_=id_)
        data = data[:-1]
        if data[7] is not None:
            data[7] = datetime.datetime.strptime(data[7], enum_sheet.date_format).date()
        if data[8] is not None:
            data[8] = datetime.datetime.strptime(data[8], enum_sheet.date_format).date()
        return data

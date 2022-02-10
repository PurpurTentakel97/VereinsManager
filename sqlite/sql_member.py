# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Member

import datetime

import debug
from enum_sheet import TableTypes, MemberTypes
import enum_sheet

database_member: "DatabaseMember" or None = None


class DatabaseMember:
    def __init__(self, database):
        self.database = database
        self.CreateItem = database.CreateItem

    def __str__(self) -> str:
        return "DATABASE MEMBER"

    def create_member_table(self) -> None:
        sql_items: list = [
            self.CreateItem(column_name=MemberTypes.ID.value, column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True)
        ]
        text_columns: list = [
            MemberTypes.FIRST_NAME.value,
            MemberTypes.LAST_NAME.value,
            MemberTypes.STREET.value,
            MemberTypes.NUMBER.value,
            MemberTypes.CITY.value,
            MemberTypes.MEMBERSHIP_TYPE.value,
            MemberTypes.COMMENT.value
        ]
        integer_columns: list = [
            MemberTypes.ZIP_CODE.value,
            MemberTypes.SPECIAL_MEMBER.value
        ]
        date_columns: list = [
            MemberTypes.B_DAY_DATE.value,
            MemberTypes.ENTRY_DATE.value
        ]

        for column in text_columns:
            sql_items.append(self.CreateItem(column_name=column, column_type=3))
        for column in integer_columns:
            sql_items.append(self.CreateItem(column_name=column, column_type=1))
        for column in date_columns:
            sql_items.append(self.CreateItem(column_name=column, column_type=5))
        sql_items.append(self.CreateItem(column_name=MemberTypes.ACTIVE_MEMBER.value, column_type=1))

        self.database.create(table_name=TableTypes.MEMBER.value, columns=tuple(sql_items))

    def save_member(self, output: dict):
        # sql_command: str = f"""INSERT INTO "{TableTypes.MEMBER.value}" (
        # "{MemberTypes.FIRST_NAME.value}",
        # "{MemberTypes.LAST_NAME.value}",
        # "{MemberTypes.STREET.value}",
        # "{MemberTypes.NUMBER.value}",
        # "{MemberTypes.ZIP_CODE.value}",
        # "{MemberTypes.CITY.value}",
        # "{MemberTypes.B_DAY_DATE.value}",
        # "{MemberTypes.ENTRY_DATE.value}",
        # "{MemberTypes.MEMBERSHIP_TYPE.value}",
        # "{MemberTypes.SPECIAL_MEMBER.value}",
        # "{MemberTypes.COMMENT.value}",
        # "{MemberTypes.ACTIVE_MEMBER.value}") VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"""
        #
        # values: tuple = (
        #     output[MemberTypes.FIRST_NAME.value] or None,
        #     output[MemberTypes.LAST_NAME.value] or None,
        #     output[MemberTypes.STREET.value] or None,
        #     output[MemberTypes.NUMBER.value] or None,
        #     output[MemberTypes.ZIP_CODE.value] or None,
        #     output[MemberTypes.CITY.value] or None,
        #     output[MemberTypes.B_DAY_DATE.value].strftime(enum_sheet.date_format) \
        #         if output[MemberTypes.B_DAY_DATE.value] is not None else None,
        #     output[MemberTypes.ENTRY_DATE.value].strftime(enum_sheet.date_format) \
        #         if output[MemberTypes.ENTRY_DATE.value] is not None else None,
        #     output[MemberTypes.MEMBERSHIP_TYPE.value] or None,
        #     output[MemberTypes.SPECIAL_MEMBER.value],
        #     output[MemberTypes.COMMENT.value] or None,
        #     True)

        debug.info(item=self, keyword="member_save", message="member saved")

        # return self.database.insert(sql_command=sql_command, values=values)

    def update_member(self, output: dict) -> None:
        # sql_command: str = f"""UPDATE {TableTypes.MEMBER.value}
        # SET {MemberTypes.FIRST_NAME.value} = ?,
        # {MemberTypes.LAST_NAME.value} = ?,
        # {MemberTypes.STREET.value} = ?,
        # {MemberTypes.NUMBER.value} = ?,
        # {MemberTypes.ZIP_CODE.value} = ?,
        # {MemberTypes.CITY.value} = ?,
        # {MemberTypes.B_DAY_DATE.value} = ?,
        # {MemberTypes.ENTRY_DATE.value} = ?,
        # {MemberTypes.MEMBERSHIP_TYPE.value} = ?,
        # {MemberTypes.SPECIAL_MEMBER.value} = ?,
        # {MemberTypes.COMMENT.value} = ?
        # WHERE {MemberTypes.ID.value} = ?;"""
        #
        # values: tuple = (
        #     output[MemberTypes.FIRST_NAME.value] or None,
        #     output[MemberTypes.LAST_NAME.value] or None,
        #     output[MemberTypes.STREET.value] or None,
        #     output[MemberTypes.NUMBER.value] or None,
        #     output[MemberTypes.ZIP_CODE.value] or None,
        #     output[MemberTypes.CITY.value] or None,
        #     output[MemberTypes.B_DAY_DATE.value].strftime(enum_sheet.date_format) \
        #         if output[MemberTypes.B_DAY_DATE.value] is not None else None,
        #     output[MemberTypes.ENTRY_DATE.value].strftime(enum_sheet.date_format) \
        #         if output[MemberTypes.ENTRY_DATE.value] is not None else None,
        #     output[MemberTypes.MEMBERSHIP_TYPE.value] or None,
        #     output[MemberTypes.SPECIAL_MEMBER.value],
        #     output[MemberTypes.COMMENT.value] or None,
        #     output[MemberTypes.ID.value])

        debug.info(item=self, keyword="update member", message="member updated")

        # self.database.update(sql_command=sql_command, values=values)

    def delete_recover_member(self, member_id: int, active: bool) -> None:
        # sql_command: str = f"""UPDATE {TableTypes.MEMBER.value}
        # SET {MemberTypes.ACTIVE_MEMBER.value} = ?
        # WHERE {MemberTypes.ID.value} = ?;"""
        # values: tuple = (active, member_id)

        debug.info(item=self, keyword="delete member", message="member deleted")

        # self.database.update(sql_command=sql_command, values=values)

    def load_all_member_names(self, active: bool):
        # sql_command: str = f"""SELECT {MemberTypes.ID.value},
        # {MemberTypes.FIRST_NAME.value},
        # {MemberTypes.LAST_NAME.value}
        # FROM {TableTypes.MEMBER.value}
        # WHERE {MemberTypes.ACTIVE_MEMBER.value} LIKE {active};"""

        debug.info(item=self, keyword="load all member names", message="member names loaded")

        # return self.database.select_all(sql_command=sql_command)

    def load_all_data_from_member(self, id_: int):
        debug.info(item=self, keyword="load data from member", message="member loaded")
        # sql_command: str = f"""SELECT * FROM '{TableTypes.MEMBER.value}' WHERE {MemberTypes.ID.value} = {id_}"""

        # data = self.database.select_one(sql_command=sql_command)
        # data = list(data)

        # for i in range(1, len(data)):
        #     if data[i] == 1:
        #         data[i] = True
        #     elif data[i] == 0:
        #         data[i] = False
        #
        # return data

# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite
import datetime
import sqlite3
from datetime import date

import enum_sheet
import main
from enum_sheet import TypeType, MemberTypes, TableTypes, MemberPhoneTypes, MemberMailTypes, MemberPositionTypes, \
    LogTypes


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("saves/test.vm", detect_types=sqlite3.PARSE_DECLTYPES)  # TODO name save file
        self.cursor = self.connection.cursor()

    # types
    def create_type_table(self, table_name: str) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{table_name}" (
        "ID" INTEGER NOT NULL UNIQUE,
        "{table_name}" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("ID" AUTOINCREMENT));"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_type_list(self, table_name: str) -> list:
        sql_command: str = f"""SELECT * FROM {table_name} ORDER BY {table_name}"""
        self.cursor.execute(sql_command)
        types_list: list = self.cursor.fetchall()
        return types_list

    def add_type(self, table_name: str, type_: str) -> None:
        sql_command: str = f"""INSERT INTO "{table_name}"
        ("{table_name}")
        VALUES('{type_}');"""
        self.cursor.execute(sql_command)
        self.connection.commit()

    def edit_type(self, table_name: str, new_type: str, type_id: int):
        sql_command: str = f"""UPDATE {table_name} SET {table_name} = '{new_type}' WHERE ID = {type_id};"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def remove_type(self, table_name: str, type_id: int) -> bool:
        sql_command: str = f"""DELETE FROM {table_name} WHERE ID ='{type_id}';"""

        try:
            self.cursor.execute(sql_command)
            self.connection.commit()
            return True
        except:
            return False

    # member
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

        self.cursor.execute(sql_command)
        self.connection.commit()

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

        self.cursor.execute(sql_command, (
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
            True))
        self.connection.commit()

        return self.cursor.lastrowid

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

        self.cursor.execute(sql_command, (
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
            output[MemberTypes.ID.value]))
        self.connection.commit()

    def delete_recover_member(self, member_id: int, active: bool) -> None:

        sql_command: str = f"""UPDATE {TableTypes.MEMBER.value}
        SET {MemberTypes.ACTIVE_MEMBER.value} = ? 
        WHERE {MemberTypes.ID.value} = ?;"""

        self.cursor.execute(sql_command, (active, member_id))
        self.connection.commit()

    def load_all_member_names(self, active: bool) -> list:
        sql_command: str = f"""SELECT {MemberTypes.ID.value}, 
        {MemberTypes.FIRST_NAME.value}, 
        {MemberTypes.LAST_NAME.value} 
        FROM {TableTypes.MEMBER.value} 
        WHERE {MemberTypes.ACTIVE_MEMBER.value} LIKE ?;"""

        self.cursor.execute(sql_command, (active,))
        data = self.cursor.fetchall()
        return data

    def load_all_data_from_member(self, id_: int) -> list:
        sql_command: str = f"""SELECT * FROM '{TableTypes.MEMBER.value}' WHERE {MemberTypes.ID.value} = {id_}"""

        self.cursor.execute(sql_command)
        data = self.cursor.fetchall()
        data = list(data[0])

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

    # member nexus
    def create_member_nexus_tables(self) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_PHONE.value}" (
        "{MemberPhoneTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberPhoneTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.NUMBER.value}"	TEXT NOT NULL,
        PRIMARY KEY("{MemberPhoneTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberPhoneTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberPhoneTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.cursor.execute(sql_command)

        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_MAIL.value}" (
        "{MemberMailTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberMailTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberMailTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        "{MemberMailTypes.MAIL.value}"	TEXT NOT NULL,
        PRIMARY KEY("{MemberMailTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberMailTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberMailTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.cursor.execute(sql_command)

        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_POSITION.value}" (
        "{MemberPositionTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberPositionTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberPositionTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        PRIMARY KEY("{MemberPositionTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberPositionTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberPositionTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def save_member_nexus(self, table_type: TableTypes, member_id: int, value_id: int, value) -> int:
        sql_command: str = str()

        match table_type:
            case TableTypes.MEMBER_PHONE:
                sql_command: str = f"""INSERT INTO "{table_type.value}"
                ("{MemberPhoneTypes.MEMBER_ID.value}",
                "{MemberPhoneTypes.TYPE_ID.value}",
                "{MemberPhoneTypes.NUMBER.value}")
                VALUES ('{member_id}', '{value_id}', '{value}');"""
            case TableTypes.MEMBER_MAIL:
                sql_command: str = f"""INSERT INTO "{table_type.value}"
                    ("{MemberMailTypes.MEMBER_ID.value}",
                    "{MemberMailTypes.TYPE_ID.value}",
                    "{MemberMailTypes.MAIL.value}")
                    VALUES ('{member_id}', '{value_id}', '{value}');"""
            case TableTypes.MEMBER_POSITION:
                sql_command: str = f"""INSERT INTO "{table_type.value}"
                        ("{MemberPositionTypes.MEMBER_ID.value}",
                        "{MemberPositionTypes.TYPE_ID.value}")
                        VALUES ('{member_id}', '{value_id}');"""

        self.cursor.execute(sql_command)
        self.connection.commit()
        return self.cursor.lastrowid

    def update_member_nexus(self, table_type: TableTypes, member_table_id: int, value, value_id: int) -> None:
        sql_command: str = str()

        match table_type:
            case TableTypes.MEMBER_PHONE:
                sql_command = f"""UPDATE {TableTypes.MEMBER_PHONE.value}  
                            SET {MemberPhoneTypes.NUMBER.value} = ?
                            WHERE {MemberPhoneTypes.ID.value} = ?"""
                self.cursor.execute(sql_command, (value, member_table_id))
            case TableTypes.MEMBER_MAIL:
                sql_command = f"""UPDATE {TableTypes.MEMBER_MAIL.value}  
                            SET {MemberMailTypes.MAIL.value} = ?
                            WHERE {MemberMailTypes.ID.value} = ?"""
                self.cursor.execute(sql_command, (value, member_table_id))
            case TableTypes.MEMBER_POSITION:
                sql_command = f"""UPDATE {TableTypes.MEMBER_POSITION.value}  
                            SET {MemberPositionTypes.TYPE_ID.value} = ?
                            WHERE {MemberPositionTypes.ID.value} = ?"""
                self.cursor.execute(sql_command, (value_id, member_table_id))

    def delete_member_nexus(self) -> None:
        pass

    def load_nexus_item_from_id(self, table_type: TableTypes, id_: int) -> list:
        sql_command: str = f"""SELECT * FROM {table_type.value} WHERE ID is {id_};"""
        self.cursor.execute(sql_command)
        data = self.cursor.fetchall()
        return data

    # log
    def create_log_tables(self) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.LOG.value}" (
        "{LogTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{LogTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{LogTypes.LOG_TYPE.value}"	TEXT NOT NULL,
        "{LogTypes.DATE.value}"	TEXT NOT NULL,
        "{LogTypes.OLD_DATA.value}"	TEXT,
        "{LogTypes.NEW_DATA.value}"	TEXT,
        FOREIGN KEY("{LogTypes.MEMBER_ID.value}") REFERENCES "member",
        PRIMARY KEY("{LogTypes.ID.value}" AUTOINCREMENT));"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def log_data(self, member_id: int, log_type: str, log_date: date, old_data: str | None,
                 new_data: str | None) -> None:
        sql_command: str = f"""INSERT INTO "{TableTypes.LOG.value}"
        ("{LogTypes.MEMBER_ID.value}",
         "{LogTypes.LOG_TYPE.value}",
         "{LogTypes.DATE.value}",
         "{LogTypes.OLD_DATA.value}",
         "{LogTypes.NEW_DATA.value}")
        VALUES (?, ?, ?, ?, ?);"""
        values = [
            member_id,
            log_type,
            log_date.strftime(enum_sheet.date_format) if log_date is not None else None,
        ]
        if type(old_data) == bool or type(new_data) == bool:
            values.append(old_data)
            values.append(new_data)
        else:
            values.append(old_data or None)
            values.append(new_data or None)

        self.cursor.execute(sql_command, tuple(values))
        self.connection.commit()


class Handler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_all_tables() -> None:
        for type_ in enum_sheet.get_all_types():
            database.create_type_table(table_name=type_[0])
        database.create_member_table()
        database.create_member_nexus_tables()
        database.create_log_tables()

    @staticmethod
    def get_display_types(type_type: TypeType) -> list[str]:
        display_types: list = list()
        dummy_list: list = list()

        match type_type:
            case TypeType.ALL:
                dummy_list = enum_sheet.get_all_types()
            case TypeType.MEMBER:
                dummy_list = enum_sheet.member_types

        for type_ in dummy_list:
            display_types.append(type_[1])
        return display_types

    @staticmethod
    def get_type_from_display_name(display_name: str) -> str:
        for type_ in enum_sheet.get_all_types():
            if display_name in type_:
                return type_[0]

    @staticmethod
    def save_member_nexus(member_id: int, table_type, output: tuple):
        for _ in output:
            member_table_id, value_id, value_type, value = _
            if member_table_id is None and len(value) == 0:  # no entry
                continue

            elif member_table_id is None and len(value) > 0:  # save entry
                database.save_member_nexus(table_type=table_type, member_id=member_id, value_id=value_id,
                                                 value=value)
                main.log_initial_member_nexus(member_id=member_id, log_type=value_type, new_data=value)

            elif member_table_id is not None and len(value) > 0:  # update entry
                reference_data = database.load_nexus_item_from_id(table_type=table_type, id_=member_table_id)
                database.update_member_nexus(table_type=table_type, member_table_id=member_table_id, value=value,
                                             value_id=value_id)
                main.log_update_member_nexus(reverence_data=reference_data, new_data=value)

            elif member_table_id is not None and len(value) == 0:  # delete entry
                database.delete_member_nexus()
            else:
                print("Error save member nexus")


database: Database | None = None
handler: Handler | None = None

# date = datetime.strptime( "2022-10-01", '%Y %m %d').date()

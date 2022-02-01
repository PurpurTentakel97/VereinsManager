# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite

import sqlite3

import enum_sheet
from enum_sheet import TypeType, MemberTypes, TableTypes, MemberPhoneTypes


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
            "{MemberTypes.B_DAY_DATE.value}"	DATE,
            "{MemberTypes.ENTRY_DATE.value}"	DATE,
            "{MemberTypes.MEMBERSHIP_TYPE.value}"	TEXT,
            "{MemberTypes.SPECIAL_MEMBER.value}"	INTEGER,
            "{MemberTypes.COMMENT.value}"	TEXT,
            PRIMARY KEY("ID" AUTOINCREMENT));"""

        self.cursor.execute(sql_command)
        self.connection.commit()

    def save_member(self, output: dict) -> int:
        null = "NULL,"
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
        "{MemberTypes.COMMENT.value}") VALUES ("""
        sql_command += f"'{output[MemberTypes.FIRST_NAME.value]}'," \
            if output[MemberTypes.FIRST_NAME.value] is not None else null
        sql_command += f"'{output[MemberTypes.LAST_NAME.value]}'," \
            if output[MemberTypes.LAST_NAME.value] is not None else null
        sql_command += f"'{output[MemberTypes.STREET.value]}'," \
            if output[MemberTypes.STREET.value] is not None else null
        sql_command += f"'{output[MemberTypes.NUMBER.value]}'," \
            if output[MemberTypes.NUMBER.value] is not None else null
        sql_command += f"{output[MemberTypes.ZIP_CODE.value]}," \
            if output[MemberTypes.ZIP_CODE.value] is not None else null
        sql_command += f"'{output[MemberTypes.CITY.value]}'," if output[MemberTypes.CITY.value] is not None else null
        sql_command += f"{output[MemberTypes.B_DAY_DATE.value]}," \
            if output[MemberTypes.B_DAY_DATE.value] is not None else null
        sql_command += f"{output[MemberTypes.ENTRY_DATE.value]}," \
            if output[MemberTypes.ENTRY_DATE.value] is not None else null
        sql_command += f"'{output[MemberTypes.MEMBERSHIP_TYPE.value]}'," \
            if output[MemberTypes.MEMBERSHIP_TYPE.value] is not None else null
        sql_command += f'{1},' if output[MemberTypes.SPECIAL_MEMBER.value] else f'{0},'
        sql_command += f"'{output[MemberTypes.COMMENT.value]}'," if output[MemberTypes.COMMENT.value] != "" else null
        sql_command = sql_command[:-1]
        sql_command += ");"

        self.cursor.execute(sql_command)
        self.connection.commit()

        return self.cursor.lastrowid

    # member phone
    def create_member_phone_table(self) -> None:
        sql_command: str = f"""CREATE TABLE "{TableTypes.MEMBER_PHONE.value}" (
        "{MemberPhoneTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberPhoneTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.NUMBER.value}"	TEXT NOT NULL,
        PRIMARY KEY("{MemberPhoneTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberPhoneTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberPhoneTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.cursor.execute(sql_command)
        self.connection.commit()


class Handler:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_all_tables() -> None:
        for type_ in enum_sheet.get_all_types():
            database.create_type_table(table_name=type_[0])
        database.create_member_table()
        database.create_member_phone_table()

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


database: Database | None = None
handler: Handler | None = None

# date = datetime.strptime( "2022-10-01", '%Y %m %d').date()
# date_str=t.strftime('%m/%d/%Y')

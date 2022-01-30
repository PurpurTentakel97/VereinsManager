# Purpur Tentakel
# 21.01.2022
# VereinsManager / SQLite
import os
import sqlite3
import os
from datetime import date

from logic.enum_sheet import MemberEntries, SQLite_Table

path_: str = str()


def create_connection() -> None:
    if not os.path.exists(os.path.dirname(path_)):
        os.makedirs(os.path.dirname(path_))
    global connection
    connection = sqlite3.connect(path_,
                                 detect_types=sqlite3.PARSE_DECLTYPES |
                                              sqlite3.PARSE_COLNAMES)
    global cursor
    cursor = connection.cursor()


def create_table(table: SQLite_Table) -> None:
    sql_command: str = str()
    match table:
        case SQLite_Table.MEMBERS:
            sql_command: str = f"""
            CREATE TABLE IF NOT EXISTS {table.value}(
            {MemberEntries.ID.value} INTEGER PRIMARY KEY,
            {MemberEntries.FIRST_NAME.value} STRING,
            {MemberEntries.LAST_NAME.value} STRING,
            {MemberEntries.STREET.value} STRING,
            {MemberEntries.NUMBER.value} STRING,
            {MemberEntries.ZIP_CODE.value} INTEGER,
            {MemberEntries.CITY.value} STRING,
            {MemberEntries.BIRTH_DAY.value} TIMESTAMP,
            {MemberEntries.ENTRY_DATE.value} TIMESTAMP,
            {MemberEntries.PHONE_NUMBERS.value} DICT,
            {MemberEntries.MAIL_ADDRESSES.value} DICT,
            {MemberEntries.MEMBERSHIP_TYPE.value} STRING,
            {MemberEntries.SPECIAL_MEMBER.value} BOOL,
            {MemberEntries.POSITIONS.value} LIST,
            {MemberEntries.INSTRUMENTS.value} LIST,
            {MemberEntries.COMMENT_TEXT.value} STRING,
            {MemberEntries.LOG.value} DICT);"""

    if sql_command:
        cursor.execute(sql_command)


def write_data(table: SQLite_Table, data: list[dict]) -> None:
    create_table(table=table)
    for single_data in data:
        command_str = f"""INSERT INTO {table.value} (id,"""
        value_str = """VALUES (NULL,"""
        for key, value in single_data.items():
            if not key == MemberEntries.ID:
                command_str += f"{key.value},"
                if type(value) == bool:
                    value_str += f'{1 if value else 0},'
                else:
                    value_str += f'"{value}",' if value is not None else "NULL,"
        command_str = command_str[:-1]
        value_str = value_str[:-1]
        command_str += ") "
        value_str += ");"
        sql_command = command_str + value_str

        cursor.execute(sql_command)
    connection.commit()
    read_data(table)


def read_data(table: SQLite_Table) -> list:
    create_table(table=table)
    cursor.execute(f"SELECT * FROM {table.value}")
    data: list[table] = cursor.fetchall()
    input_data = list()
    for single_data in data:
        single_input_data: dict = {
            MemberEntries.ID: single_data[0],

            MemberEntries.FIRST_NAME: single_data[1],
            MemberEntries.LAST_NAME: single_data[2],

            MemberEntries.STREET: single_data[3],
            MemberEntries.NUMBER: single_data[4],
            MemberEntries.ZIP_CODE: single_data[5],
            MemberEntries.CITY: single_data[6],

            MemberEntries.BIRTH_DAY: single_data[7],
            MemberEntries.ENTRY_DATE: single_data[8],

            MemberEntries.PHONE_NUMBERS: single_data[9],
            MemberEntries.MAIL_ADDRESSES: single_data[10],

            MemberEntries.MEMBERSHIP_TYPE: single_data[11],
            MemberEntries.SPECIAL_MEMBER: single_data[12] == 1,  # bool
            MemberEntries.POSITIONS: single_data[13],
            MemberEntries.INSTRUMENTS: single_data[14],

            MemberEntries.COMMENT_TEXT: single_data[15],
            MemberEntries.LOG: single_data[16]}

        input_data.append(single_input_data)

    return input_data


def edit_data(table: SQLite_Table, data: list[dict]) -> None:
    create_table(table=table)
    for single_data in data:
        sql_statement = f"""UPDATE {table.value} SET"""
        for update in single_data.items():
            key, value = update
            if not key == MemberEntries.ID:
                if type(value) == bool:
                    sql_statement += f'{key.value} = {1 if value else 0},'
                else:
                    sql_statement += f' {key.value} = "{value}",' if value else f"{key.value} = NULL,"
        sql_statement = sql_statement[:-1]
        sql_statement += f" WHERE {MemberEntries.ID.value} = {single_data[MemberEntries.ID]}"
        cursor.execute(sql_statement)
    connection.commit()


def delete_data(table: SQLite_Table, ids: list[int]) -> None:
    create_table(table=table)
    sql_statement = f"""DELETE FROM {table.value} WHERE id IN ({','.join(["?"] * len(ids))})"""
    print(sql_statement)
    cursor.execute(sql_statement, ids)

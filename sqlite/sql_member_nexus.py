# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Member Nexus

from enum_sheet import TableTypes, MemberPhoneTypes, MemberMailTypes, MemberPositionTypes


class DatabaseMemberNexus:
    def __init__(self, database):
        self.database = database

    def create_member_nexus_tables(self) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_PHONE.value}" (
        "{MemberPhoneTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberPhoneTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        "{MemberPhoneTypes.NUMBER.value}"	TEXT NOT NULL,
        PRIMARY KEY("{MemberPhoneTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberPhoneTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberPhoneTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.database.create(sql_command=sql_command)

        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_MAIL.value}" (
        "{MemberMailTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberMailTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberMailTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        "{MemberMailTypes.MAIL.value}"	TEXT NOT NULL,
        PRIMARY KEY("{MemberMailTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberMailTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberMailTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.database.create(sql_command=sql_command)

        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{TableTypes.MEMBER_POSITION.value}" (
        "{MemberPositionTypes.ID.value}"	INTEGER NOT NULL UNIQUE,
        "{MemberPositionTypes.MEMBER_ID.value}"	INTEGER NOT NULL,
        "{MemberPositionTypes.TYPE_ID.value}"	INTEGER NOT NULL,
        PRIMARY KEY("{MemberPositionTypes.ID.value}" AUTOINCREMENT),
        FOREIGN KEY("{MemberPositionTypes.TYPE_ID.value}") REFERENCES "phone_number_type",
        FOREIGN KEY("{MemberPositionTypes.MEMBER_ID.value}") REFERENCES "member")"""

        self.database.create(sql_command=sql_command)

    def save_member_nexus(self, table_type: TableTypes, member_id: int, value_id: int, value) -> int:
        sql_command: str = str()
        values: list = list()

        match table_type:
            case TableTypes.MEMBER_PHONE:
                sql_command: str = f"""INSERT INTO "{table_type.value}"
                ("{MemberPhoneTypes.MEMBER_ID.value}",
                "{MemberPhoneTypes.TYPE_ID.value}",
                "{MemberPhoneTypes.NUMBER.value}")
                VALUES (?,?,?);"""
                values: tuple = (member_id, value_id, value)

            case TableTypes.MEMBER_MAIL:
                sql_command: str = f"""INSERT INTO "{table_type.value}"
                    ("{MemberMailTypes.MEMBER_ID.value}",
                    "{MemberMailTypes.TYPE_ID.value}",
                    "{MemberMailTypes.MAIL.value}")
                    VALUES (?,?,?);"""
                values: tuple = (member_id, value_id, value)

        return self.database.insert(sql_command=sql_command, values=values)

    def save_member_nexus_position(self, member_id: int, value_id: int) -> int:
        sql_command: str = f"""INSERT INTO {TableTypes.MEMBER_POSITION.value} 
        ("{MemberPositionTypes.MEMBER_ID.value}", "{MemberPositionTypes.TYPE_ID.value}")
        VALUES (?,?);"""
        values: tuple = (member_id, value_id)
        return self.database.insert(sql_command=sql_command, values=values)

    def update_member_nexus(self, table_type: TableTypes, member_table_id: int, value) -> None:
        match table_type:
            case TableTypes.MEMBER_PHONE:
                sql_command = f"""UPDATE {TableTypes.MEMBER_PHONE.value}  
                            SET {MemberPhoneTypes.NUMBER.value} = ?
                            WHERE {MemberPhoneTypes.ID.value} = ?"""
                values: tuple = (value, member_table_id)
                self.database.update(sql_command=sql_command, values=values)

            case TableTypes.MEMBER_MAIL:
                sql_command = f"""UPDATE {TableTypes.MEMBER_MAIL.value}  
                            SET {MemberMailTypes.MAIL.value} = ?
                            WHERE {MemberMailTypes.ID.value} = ?"""
                values: tuple = (value, member_table_id)
                self.database.update(sql_command=sql_command, values=values)

            case TableTypes.MEMBER_POSITION:
                sql_command = f"""UPDATE {TableTypes.MEMBER_POSITION.value}  
                                SET {MemberPositionTypes.TYPE_ID.value} = ?
                                WHERE {MemberPositionTypes.ID.value} = ?"""
                values: tuple = (value, member_table_id)
                self.database.update(sql_command=sql_command, values=values)

    def delete_member_nexus(self, table_type: TableTypes, id_: int) -> None:
        sql_command: str = f"""DELETE FROM {table_type.value} WHERE ID IS {id_};"""
        self.database.delete(sql_command=sql_command)

    def load_member_nexus(self, member_id, table_type: str) -> list:
        sql_command: str = f"""SELECT * FROM {table_type} WHERE member_id is {member_id}"""
        return self.database.select_all(sql_command)

    def load_nexus_item_from_id(self, table_type: TableTypes, id_: int) -> tuple:
        sql_command: str = f"""SELECT * FROM {table_type.value} WHERE ID is {id_};"""
        data = self.database.select_one(sql_command)
        return data

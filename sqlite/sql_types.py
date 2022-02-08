# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite types


class DatabaseTypes:
    def __init__(self, database):
        self.database = database

    def create_type_table(self, table_name: str) -> None:
        sql_command: str = f"""CREATE TABLE IF NOT EXISTS "{table_name}" (
        "ID" INTEGER NOT NULL UNIQUE,
        "{table_name}" TEXT NOT NULL UNIQUE,
        PRIMARY KEY("ID" AUTOINCREMENT));"""

        self.database.create(sql_command=sql_command)

    def get_type_list(self, table_name: str) -> list:
        sql_command: str = f"""SELECT * FROM {table_name} ORDER BY {table_name}"""
        return self.database.select_all(sql_command=sql_command)

    def get_type_from_id(self, id_: int, table_type: str) -> str:
        sql_command: str = f"""SELECT {table_type} FROM {table_type} WHERE ID is {id_}"""
        type_ = self.database.select_all(sql_command=sql_command)
        return type_[0][0]

    def add_type(self, table_name: str, type_: str) -> None:
        sql_command: str = f"""INSERT INTO "{table_name}"
        ("{table_name}")
        VALUES(?);"""
        values: tuple = (type_,)
        self.database.insert(sql_command=sql_command, values=values)

    def edit_type(self, table_name: str, new_type: str, type_id: int):
        sql_command: str = f"""UPDATE {table_name} SET {table_name} = ? WHERE ID = ?;"""
        values: tuple = (new_type, type_id)

        self.database.update(sql_command=sql_command, values=values)

    def remove_type(self, table_name: str, type_id: int):
        sql_command: str = f"""DELETE FROM {table_name} WHERE ID ={type_id};"""
        self.database.delete(sql_command)

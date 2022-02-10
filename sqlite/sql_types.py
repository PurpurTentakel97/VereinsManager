# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite types

import debug


class DatabaseTypes:
    def __init__(self, database):
        self.database = database
        self.CreateItem = database.CreateItem

    def __str__(self) -> str:
        return "DatabaseTypes"

    def create_type_table(self, table_name: str) -> None:
        sql_items: list = [
            self.CreateItem(column_name="ID", column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True),
            self.CreateItem(column_name=table_name, column_type=3, column_is_not_null=True,
                            column_is_unique=True)
        ]
        self.database.create(table_name=table_name, columns=sql_items)

    def get_type_list(self, table_name: str):
        debug.info(item=self, keyword=f"{table_name}", message=f"{table_name} types loaded")
        # sql_command: str = f"""SELECT * FROM {table_name} ORDER BY {table_name}"""
        # return self.database.select_all(sql_command=sql_command)

    def get_type_from_id(self, id_: int, table_type: str):
        debug.info(item=self, keyword=f"{table_type}", message=f"Type loaded from id")
        # sql_command: str = f"""SELECT {table_type} FROM {table_type} WHERE ID is {id_}"""
        # type_ = self.database.select_all(sql_command=sql_command)
        # return type_[0][0]

    def add_type(self, table_name: str, type_: str) -> None:
        debug.info(item=self, keyword=f"{table_name}", message=f"{type_} added")
        # sql_command: str = f"""INSERT INTO "{table_name}"
        # ("{table_name}")
        # VALUES(?);"""
        # values: tuple = (type_,)
        # self.database.insert(sql_command=sql_command, values=values)

    def edit_type(self, table_name: str, new_type: str, type_id: int):
        debug.info(item=self, keyword=f"{table_name}", message=f"{new_type} edit")
        # sql_command: str = f"""UPDATE {table_name} SET {table_name} = ? WHERE ID = ?;"""
        # values: tuple = (new_type, type_id)
        #
        # self.database.update(sql_command=sql_command, values=values)

    def remove_type(self, table_name: str, type_id: int):
        debug.info(item=self, keyword=f"{table_name}", message=f"{type_id} deleted")
        # sql_command: str = f"""DELETE FROM {table_name} WHERE ID ={type_id};"""
        # self.database.delete(sql_command)

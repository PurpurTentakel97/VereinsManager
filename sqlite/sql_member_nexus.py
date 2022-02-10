# Purpur Tentakel
# 07.02.2022
# VereinsManager / SQLite Member Nexus

from enum_sheet import TableTypes, MemberPhoneTypes, MemberMailTypes, MemberPositionTypes
import debug


class DatabaseMemberNexus:
    def __init__(self, database):
        self.database = database
        self.CreateItem = database.CreateItem

    def __str__(self) -> str:
        return "Database Member Nexus"

    def create_member_nexus_tables(self) -> None:
        # phone member
        sql_items: list = [
            self.CreateItem(column_name=MemberPhoneTypes.ID.value, column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True),
            self.CreateItem(column_name=MemberPhoneTypes.MEMBER_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference=TableTypes.MEMBER.value),
            self.CreateItem(column_name=MemberPhoneTypes.TYPE_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference="type_phone_number"),  # TODO refactor Types
            self.CreateItem(column_name=MemberPhoneTypes.NUMBER.value, column_type=3, column_is_not_null=True)
        ]
        self.database.create(table_name=TableTypes.MEMBER_PHONE.value, columns=tuple(sql_items))

        # mail member
        sql_items: list = [
            self.CreateItem(column_name=MemberMailTypes.ID.value, column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True),
            self.CreateItem(column_name=MemberMailTypes.MEMBER_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference=TableTypes.MEMBER.value),
            self.CreateItem(column_name=MemberMailTypes.TYPE_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference="type_mail"),  # TODO refactor Types
            self.CreateItem(column_name=MemberMailTypes.MAIL.value, column_type=3, column_is_not_null=True)
        ]
        self.database.create(table_name=TableTypes.MEMBER_MAIL.value, columns=tuple(sql_items))

        # member position
        sql_items: list = [
            self.CreateItem(column_name=MemberPositionTypes.ID.value, column_type=1, column_is_not_null=True,
                            column_is_unique=True, is_primary_key=True, is_autoincrement=True),
            self.CreateItem(column_name=MemberPositionTypes.MEMBER_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference=TableTypes.MEMBER.value),
            self.CreateItem(column_name=MemberPositionTypes.TYPE_ID.value, column_type=1, column_is_not_null=True,
                            is_foreign_key=True, foreign_reference="type_position"),  # TODO refactor Types
        ]
        self.database.create(table_name=TableTypes.MEMBER_POSITION.value, columns=tuple(sql_items))

    def save_member_nexus(self, table_type: TableTypes, member_id: int, value_id: int, value):
        debug.info(item=self, keyword=f"{table_type.value}", message=f"{member_id} saved")

        # sql_command: str = str()
        # values: list = list()
        #
        # match table_type:
        #     case TableTypes.MEMBER_PHONE:
        #         sql_command: str = f"""INSERT INTO "{table_type.value}"
        #         ("{MemberPhoneTypes.MEMBER_ID.value}",
        #         "{MemberPhoneTypes.TYPE_ID.value}",
        #         "{MemberPhoneTypes.NUMBER.value}")
        #         VALUES (?,?,?);"""
        #         values: tuple = (member_id, value_id, value)
        #
        #     case TableTypes.MEMBER_MAIL:
        #         sql_command: str = f"""INSERT INTO "{table_type.value}"
        #             ("{MemberMailTypes.MEMBER_ID.value}",
        #             "{MemberMailTypes.TYPE_ID.value}",
        #             "{MemberMailTypes.MAIL.value}")
        #             VALUES (?,?,?);"""
        #         values: tuple = (member_id, value_id, value)
        #
        # return self.database.insert(sql_command=sql_command, values=values)

    def save_member_nexus_position(self, member_id: int, value_id: int):
        debug.info(item=self, keyword=f"{member_id}", message=f"{value_id} saved")
        # sql_command: str = f"""INSERT INTO {TableTypes.MEMBER_POSITION.value}
        # ("{MemberPositionTypes.MEMBER_ID.value}", "{MemberPositionTypes.TYPE_ID.value}")
        # VALUES (?,?);"""
        # values: tuple = (member_id, value_id)
        # return self.database.insert(sql_command=sql_command, values=values)

    def update_member_nexus(self, table_type: TableTypes, member_table_id: int, value) -> None:
        debug.info(item=self, keyword=f"{table_type.value}", message=f"{value} updated")
        # match table_type:
        #     case TableTypes.MEMBER_PHONE:
        #         sql_command = f"""UPDATE {TableTypes.MEMBER_PHONE.value}
        #                     SET {MemberPhoneTypes.NUMBER.value} = ?
        #                     WHERE {MemberPhoneTypes.ID.value} = ?"""
        #         values: tuple = (value, member_table_id)
        #         self.database.update(sql_command=sql_command, values=values)
        #
        #     case TableTypes.MEMBER_MAIL:
        #         sql_command = f"""UPDATE {TableTypes.MEMBER_MAIL.value}
        #                     SET {MemberMailTypes.MAIL.value} = ?
        #                     WHERE {MemberMailTypes.ID.value} = ?"""
        #         values: tuple = (value, member_table_id)
        #         self.database.update(sql_command=sql_command, values=values)
        #
        #     case TableTypes.MEMBER_POSITION:
        #         sql_command = f"""UPDATE {TableTypes.MEMBER_POSITION.value}
        #                         SET {MemberPositionTypes.TYPE_ID.value} = ?
        #                         WHERE {MemberPositionTypes.ID.value} = ?"""
        #         values: tuple = (value, member_table_id)
        #         self.database.update(sql_command=sql_command, values=values)

    def delete_member_nexus(self, table_type: TableTypes, id_: int) -> None:
        debug.info(item=self, keyword=f"{table_type.value}", message=f"{id_} deleted")
        # sql_command: str = f"""DELETE FROM {table_type.value} WHERE ID IS {id_};"""
        # self.database.delete(sql_command=sql_command)

    def load_member_nexus(self, member_id, table_type: str):
        debug.info(item=self, keyword=f"{table_type}", message=f"{member_id} loaded")
        # sql_command: str = f"""SELECT * FROM {table_type} WHERE member_id is {member_id}"""
        # return self.database.select_all(sql_command)

    def load_nexus_item_from_id(self, table_type: TableTypes, id_: int):
        debug.info(item=self, keyword=f"{table_type}", message=f"{id_} loaded")
        # sql_command: str = f"""SELECT * FROM {table_type.value} WHERE ID is {id_};"""
        # data = self.database.select_one(sql_command)
        # return data

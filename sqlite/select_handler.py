# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config import exception_sheet as e
import debug

debug_str: str = "SelectHandler"
select_handler: "SelectHandler"


class SelectHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def get_raw_types(self) -> tuple:
        sql_command: str = f"""SELECT ID,type_name FROM raw_type ORDER BY type_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="all raw types")
            debug.error(item=debug_str, keyword="get_raw_types", message=f"Error = {error.message}")
            raise error

    def get_all_single_type(self) -> tuple:
        sql_command: str = f"""SELECT ID,name,type_id,active FROM type ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="all types")
            debug.error(item=debug_str, keyword="get_all_single_type", message=f"Error = {error.message}")
            raise error

    def get_single_raw_type_types(self, raw_type_id: int, active: bool) -> tuple:
        table: str = "v_active_type" if active else "v_inactive_type"
        sql_command: str = f"""SELECT * FROM {table} WHERE type_id is ? ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command, (raw_type_id,)).fetchall()

        except self.OperationalError:
            error = e.LoadingFailed(info="single raw type types")
            debug.error(item=debug_str, keyword="get_single_raw_type_types", message=f"error = {error.message}")
            raise error

    def get_active_member_type(self) -> tuple:
        sql_command: str = f"""SELECT * FROM v_active_member_type ORDER BY type_id ASC, name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="active member type")
            debug.error(item=debug_str, keyword="get_active_member_type", message=f"Error = {error.message}")
            raise error

    def get_type_name_by_ID(self, ID: int) -> tuple:
        sql_command: str = f"""SELECT name FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="typ ID")
            debug.error(item=debug_str, keyword="get_type_name_by_ID", message=f"Error = {error.message}")
            raise error

    def get_type_active_by_id(self, ID: int) -> tuple:
        sql_command: str = f"""SELECT active FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="typ ID")
            debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"Error = {error.message}")
            raise error

    def get_id_by_type_name(self, raw_id: int, name: str) -> tuple:
        sql_command: str = f"""SELECT ID FROM type WHERE type_id = ? and name = ?;"""
        try:
            return self.cursor.execute(sql_command, (
                raw_id,
                name,
            )).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="typ name")
            debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"Error = {error.message}")

    # member
    def get_names_of_member(self, active: bool) -> tuple:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="member names")
            debug.error(item=debug_str, keyword="get_names_of_member", message=f"Error = {error.message}")
            raise error

    def get_name_and_dates_from_member(self, active: bool) -> tuple:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name,b_day,entry_day FROM {table};"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="member names and dates")
            debug.error(item=debug_str, keyword="get_name_and_dates_from_member", message=f"Error = {error.message}")
            raise error

    def get_data_from_member_by_membership_type_id(self, active: bool, membership_type_id: int) -> tuple:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE membership_type is ? ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command, (membership_type_id,)).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="all member data")
            debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                        message=f"Error = {error.message}")
            raise error

    def get_member_data_by_id(self, ID: int, active: bool) -> list:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID = ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()

        except self.OperationalError:
            error = e.LoadingFailed(info="single member data")
            debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
            raise error

    def get_member_activity_and_membership_by_id(self, ID: int) -> list:
        sql_command: str = f"""SELECT active,membership_type FROM "member" WHERE ID = ?;"""

        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()

        except self.OperationalError:
            error = e.LoadingFailed(info="single member activity")
            debug.error(item=debug_str, keyword="get_member_activity_and_membership_by_id",
                        message=f"Error = {error.message}")
            raise error

    def get_all_IDs_from_member(self, active: bool) -> tuple:
        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID FROM {table};"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="all member IDs")
            debug.error(item=debug_str, keyword="get_all_IDs_from_member", message=f"Error = {error.message}")
            raise error

    # member nexus
    def get_phone_number_by_member_id(self, member_id: int) -> tuple:
        sql_command: str = f"""SELECT ID,type_id,number FROM member_phone WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="member phone number")
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
            raise error

    def get_phone_number_by_ID(self, ID: int) -> tuple:
        sql_command: str = f"""SELECT number,type_id FROM member_phone WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="single phone number")
            debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"Error = {error.message}")
            raise error

    def get_mail_by_member_id(self, member_id: int) -> tuple:
        sql_command: str = f"""SELECT ID,type_id,mail FROM member_mail WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="member mail address")
            debug.error(item=debug_str, keyword="get_mail_by_member_id", message=f"Error = {error.message}")
            raise error

    def get_mail_member_by_ID(self, ID: int) -> tuple:
        sql_command: str = f"""SELECT mail, type_id FROM member_mail WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="single mail address")
            debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"Error = {error.message}")
            raise error

    def get_position_by_member_id(self, member_id: int) -> tuple:
        sql_command: str = f"""SELECT ID,type_id,active FROM member_position WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="member position")
            debug.error(item=debug_str, keyword="get_position_by_member_id", message=f"Error = {error.message}")
            raise error

    def get_position_member_by_ID(self, ID: int) -> tuple:
        sql_command: str = f"""SELECT active,type_id FROM member_position WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError:
            error = e.LoadingFailed(info="single position")
            debug.error(item=debug_str, keyword="get_position_member_by_ID", message=f"Error = {error.message}")
            raise error

    # user
    def get_names_of_user(self, active: bool) -> tuple:
        table: str = "v_active_user" if active else "v_inactive_user"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError:
            error = e.LoadingFailed(info="user names")
            debug.error(item=debug_str, keyword="get_names_of_user", message=f"Error = {error.message}")
            raise error

    def get_data_of_user_by_ID(self, ID: int, active: bool) -> tuple:
        table: str = "v_active_user" if active else "v_inactive_user"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID is ?;"""

        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()

        except self.OperationalError:
            error = e.LoadingFailed(info="user data")
            debug.error(item=debug_str, keyword="get_data_of_user_by_ID", message=f"Error = {error.message}")
            raise error

    def get_hashed_password_by_ID(self, ID: int) -> bytes:
        sql_command: str = """SELECT password FROM v_active_user_password WHERE ID IS ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()[0]
        except self.OperationalError:
            error = e.LoadingFailed(info="user passsword")
            debug.error(item=debug_str, keyword="get_hashed_password_by_ID", message=f"Error = {error.message}")
            raise error


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

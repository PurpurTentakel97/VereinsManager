# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation as v
from config import config_sheet as c
import debug

debug_str: str = "SelectHandler"
select_handler: "SelectHandler"


class SelectHandler(Database):
    def __init__(self) -> None:
        super().__init__()

    # type
    def get_raw_types(self) -> [tuple | str, bool]:
        sql_command: str = f"""SELECT ID,type_name FROM raw_type ORDER BY type_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_raw_types", message=f"load raw types failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Raw Types").message, False

    def get_all_single_type(self) -> [tuple | str, bool]:
        sql_command: str = f"""SELECT ID,name,type_id,active FROM type ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_all_single_type", message=f"load all types failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Typen").message, False

    def get_single_raw_type_types(self, raw_type_id: int, active: bool = True) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=raw_type_id)
            v.validation.must_bool(bool_=active)
        except (e.NoBool, e.NoPositiveInt) as error:
            return error.message, False

        table: str = "v_active_type" if active else "v_inactive_type"
        sql_command: str = f"""SELECT * FROM {table} WHERE type_id is ? ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command, (raw_type_id,)).fetchall(), True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_single_type", message=f"load types failed\n"
                                                                           f"command = {sql_command}\n"
                                                                           f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typen").message, False

    def get_active_member_type(self) -> [tuple | str, bool]:
        sql_command: str = f"""SELECT * FROM v_active_member_type ORDER BY type_id ASC, name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_active_member_type", message=f"load raw types failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Active Member Type").message, False

    def get_type_name_by_ID(self, ID: int) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT name FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"load single type name failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ ID").message, False

    def get_type_active_by_id(self, ID: int) -> [tuple or str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT active FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"load single type active failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ ID").message, False

    def get_id_by_type_name(self, raw_id: int, name: str) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=raw_id, max_length=None)
            v.validation.must_str(str_=name)
        except (e.NoInt, e.NoPositiveInt, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT ID FROM type WHERE type_id = ? and name = ?;"""
        try:
            return self.cursor.execute(sql_command, (
                raw_id,
                name,
            )).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"load single type failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ Name").message, False

    # member
    def get_names_of_member(self, active: bool = True) -> [tuple | str, bool]:
        try:
            v.validation.must_bool(bool_=active)
        except e.NoBool as error:
            debug.error(item=debug_str, keyword="get_names_of_member", message=f"Error = {error.message}")
            return error.message, False

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedernamen").message, False

    def get_name_and_dates_from_member(self, active: bool = True) -> [tuple | str, bool]:
        try:
            v.validation.must_bool(bool_=active)
        except e.NoBool as error:
            debug.error(item=debug_str, keyword="get_name_and_dates_from_member", message=f"Error = {error.message}")
            return error.message, False

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name,b_day,entry_day FROM {table};"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedernamen").message, False

    def get_data_from_member_by_membership_type_id(self, active: bool, membership_type_id: int) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=membership_type_id, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoInt, e.NoPositiveInt, e.ToLong, e.NoBool) as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                        message=f"Error = {error.message}")
            return error.message, False

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE membership_type is ? ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command, (membership_type_id,)).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                        message=f"load all member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Mitglieder Daten").message, False

    def get_member_data_by_id(self, ID: int, active: bool = True) -> [dict | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
            return error.message, False

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID = ?;"""
        try:
            data = self.cursor.execute(sql_command, (ID,)).fetchone()
            data_ = {
                "ID": data[0],
                "first_name": data[1],
                "last_name": data[2],
                "street": data[3],
                "number": data[4],
                "zip_code": data[5],
                "city": data[6],
                "maps": data[7],
                "birth_date": data[8],
                "entry_date": data[9],
                "membership_type": data[10],
                "special_member": data[11],
                "comment_text": data[12],
            }
            if isinstance(data_["membership_type"], int):
                data, valid = self.get_type_name_by_ID(data_["membership_type"])
                if not valid:
                    return data, False
                else:
                    data_["membership_type"] = data[0]

            if data_["birth_date"] is None:
                data_["birth_date"] = c.config.date_format["None_date"]
            if data_["entry_date"] is None:
                data_["entry_date"] = c.config.date_format["None_date"]

            return data_, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_id",
                        message=f"load single member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdaten").message, False

    def get_member_activity_by_id(self, ID: int) -> [bool | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT active FROM "member" WHERE ID = ?;"""

        try:
            data = self.cursor.execute(sql_command, (ID,)).fetchone()
            if isinstance(data[0], int):
                data = data[0] == 1
            return data, True

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_member_activity_from_id",
                        message=f"load single member activity failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdatensaktivität").message, False

    def get_all_IDs_from_member(self, active: bool = True) -> [list or None, bool]:
        try:
            v.validation.must_bool(bool_=active)
        except e.NoBool as error:
            debug.error(item=debug_str, keyword="get_all_IDs_from_member", message=f"Error = {error.message}")
            return error.message, False

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID FROM {table};"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_member_activity_from_id",
                        message=f"load single member activity failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdatensaktivität").message, False

    # member nexus
    def get_phone_number_by_member_id(self, member_id: int) -> [tuple or None, bool]:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT ID,type_id,number FROM member_phone WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"load phone numbers failed\n"
                                                                                         f"command = {sql_command}\n"
                                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    def get_phone_number_by_ID(self, ID: int) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT number FROM member_phone WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"load phone number by ID failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    def get_mail_by_member_id(self, member_id: int) -> [tuple or None, bool]:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT ID,type_id,mail FROM member_mail WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_mail_by_member_id", message=f"load mails failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    def get_mail_member_by_ID(self, ID: int) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT mail FROM member_mail WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"load mail number by ID failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    def get_position_by_member_id(self, member_id: int) -> [tuple or None, bool]:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT ID,type_id,active FROM member_position WHERE member_id is ? ORDER BY type_id ASC;"""
        try:
            data: list = (self.cursor.execute(sql_command, (member_id,)).fetchall())
            for i in range(len(data)):
                data[i] = list(data[i])
            for i in data:
                data[data.index(i)][2] = data[data.index(i)][2] == 1
            for i in range(len(data)):
                data[i] = tuple(data[i])
            return data, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_position_by_member_id", message=f"load positions failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    def get_position_member_by_ID(self, ID: int) -> [tuple | str, bool]:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_position_member_by_ID", message=f"Error = {error.message}")
            return error.message, False

        sql_command: str = f"""SELECT active FROM member_position WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_position_member_by_ID",
                        message=f"load position number by ID failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message, False

    # user
    def get_names_of_user(self, active: bool) -> [tuple | str, bool]:
        table: str = "v_active_user" if active else "v_inactive_user"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall(), True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_names_of_user", message=f"load user names failed\n"
                                                                             f"command = {sql_command}\n"
                                                                             f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Benutzernamen").message, False

    def get_data_of_user_by_ID(self, ID: int, active: bool) -> [dict | str, bool]:
        table: str = "v_active_user" if active else "v_inactive_user"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID is ?;"""

        try:
            data = self.cursor.execute(sql_command, (ID,)).fetchone()
            data_: dict = {
                "ID": data[0],
                "firstname": data[1],
                "lastname": data[2],
                "street": data[3],
                "number": data[4],
                "zip_code": data[5],
                "city": data[6],
                "phone": data[7],
                "mail": data[8],
                "position": data[9],
            }
            return data_, True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_of_user_by_ID", message=f"load user data failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Benutzerdaten").message, False

    def get_hashed_password_by_ID(self, ID: int) -> [str, bool]:
        sql_command: str = """SELECT password FROM v_active_user_password WHERE ID IS ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()[0], True
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_hashed_password_by_ID", message=f"load user password failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Benutzer Passwort").message, False


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

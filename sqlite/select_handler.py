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
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Select Handler"

    # type
    def get_raw_types(self) -> tuple | str:
        sql_command: str = f"""SELECT ID,type_name FROM raw_type ORDER BY type_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_raw_types", message=f"load raw types failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Raw Types").message

    def get_all_single_type(self) -> tuple | str:
        sql_command: str = f"""SELECT ID,name,type_id,active FROM type ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_all_single_type", message=f"load all types failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Typen").message

    def get_single_raw_type_types(self, raw_type_id: int, active: bool = True) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=raw_type_id)
            v.validation.must_bool(bool_=active)
        except (e.NoBool, e.NoPositiveInt) as error:
            return error.message

        table: str = "v_active_type" if active else "v_inactive_type"
        sql_command: str = f"""SELECT * FROM {table} WHERE type_id is ? ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command, (raw_type_id,)).fetchall()

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_single_type", message=f"load types failed\n"
                                                                           f"command = {sql_command}\n"
                                                                           f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typen").message

    def get_active_member_type(self) -> tuple | str:
        sql_command: str = f"""SELECT * FROM v_active_member_type ORDER BY type_id ASC, name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_active_member_type", message=f"load raw types failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Active Member Type").message

    def get_type_name_by_id(self, ID: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"Error = {error.message}")
            return error.message

        sql_command: str = f"""SELECT name FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"load single type name failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ ID").message

    def get_type_active_by_id(self, ID: int) -> tuple or str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoPositiveInt, e.NoInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"Error = {error.message}")
            return error.message

        sql_command: str = f"""SELECT active FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_type_active_by_id", message=f"load single type active failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ ID").message

    def get_id_by_type_name(self, raw_id: int, name: str) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=raw_id, max_length=None)
            v.validation.must_str(str_=name)
        except (e.NoInt, e.NoPositiveInt, e.NoStr, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"Error = {error.message}")
            return error.message

        sql_command: str = f"""SELECT ID FROM type WHERE type_id = ? and name = ?;"""
        try:
            return self.cursor.execute(sql_command, (
                raw_id,
                name,
            )).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_id_by_type_name", message=f"load single type failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ Name").message

    # member
    def get_names_of_member(self, active: bool = True) -> tuple | str:
        try:
            v.validation.must_bool(bool_=active)
        except e.NoBool as error:
            return error.message

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT ID,first_name,last_name FROM {table} ORDER BY last_name ASC,first_name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_names_of_member", message=f"load member names failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedernamen").message

    def get_data_from_member_by_membership_type_id(self, active: bool, membership_type_id: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=membership_type_id, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoInt, e.NoPositiveInt, e.ToLong, e.NoBool) as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                        message=f"Error = {error.message}")
            return error.message

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE membership_type is ?;"""
        try:
            return self.cursor.execute(sql_command)
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_membership_type_id",
                        message=f"load all member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Mitglieder Daten").message

    def get_member_data_by_id(self, ID: int, active: bool = True) -> dict | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
            v.validation.must_bool(bool_=active)
        except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
            return error.message

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
                "birth_date": data[7],
                "entry_date": data[8],
                "membership_type": data[9],
                "special_member": data[10],
                "comment_text": data[11],
            }
            if isinstance(data_["membership_type"], int):
                data = self.get_type_name_by_id(data_["membership_type"])
                if isinstance(data, str):
                    return data
                else:
                    data_["membership_type"] = data[0]

            if data_["birth_date"] is None:
                data_["birth_date"] = c.config.date_format["None_date"]
            if data_["entry_date"] is None:
                data_["entry_date"] = c.config.date_format["None_date"]

            return data_

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_data_from_member_by_id",
                        message=f"load single member data failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdaten").message

    def get_member_activity_by_id(self, ID: int) -> bool | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_member_data_by_id", message=f"Error = {error.message}")
            return error.message

        sql_command: str = f"""SELECT active FROM "member" WHERE ID = ?;"""

        try:
            data = self.cursor.execute(sql_command, (ID,)).fetchone()
            if isinstance(data[0], int):
                data = data[0] == 1
            return data

        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_member_activity_from_id",
                        message=f"load single member activity failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Mitgliedsdatensaktivität").message

    # member nexus
    def get_phone_number_by_member_id(self, member_id: int) -> tuple or None:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT ID,type_id,number FROM member_phone WHERE member_id is ?;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"load phone numbers failed\n"
                                                                                         f"command = {sql_command}\n"
                                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_phone_number_by_ID(self, ID: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT number FROM member_phone WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_ID", message=f"load phone number by ID failed\n"
                                                                                  f"command = {sql_command}\n"
                                                                                  f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_mail_by_member_id(self, member_id: int) -> tuple or None:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT ID,type_id,mail FROM member_mail WHERE member_id is ?;"""
        try:
            return self.cursor.execute(sql_command, (member_id,)).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_mail_by_member_id", message=f"load mails failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_mail_member_by_ID(self, ID: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT mail FROM member_mail WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_mail_member_by_ID", message=f"load mail number by ID failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_position_by_member_id(self, member_id: int) -> tuple or None:
        try:
            v.validation.must_positive_int(int_=member_id, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT ID,type_id,active FROM member_position WHERE member_id is ?;"""
        try:
            data: list = (self.cursor.execute(sql_command, (member_id,)).fetchall())
            for i in range(len(data)):
                data[i] = list(data[i])
            for i in data:
                data[data.index(i)][2] = data[data.index(i)][2] == 1
            for i in range(len(data)):
                data[i] = tuple(data[i])
            return data
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_position_by_member_id", message=f"load positions failed\n"
                                                                                     f"command = {sql_command}\n"
                                                                                     f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_position_member_by_ID(self, ID: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="get_position_member_by_ID", message=f"Error = {error.message}")

        sql_command: str = f"""SELECT active FROM member_position WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (ID,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_position_member_by_ID",
                        message=f"load position number by ID failed\n"
                                f"command = {sql_command}\n"
                                f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

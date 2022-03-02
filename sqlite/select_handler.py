# Purpur Tentakel
# 13.02.2022
# VereinsManager / Select Handler

from sqlite.database import Database
from config import error_code as e
from logic import validation as v
import debug

debug_str: str = "SelectHandler"
from config import config_sheet as c

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
        sql_command: str = f"""SELECT ID,name,type_id,_active FROM type ORDER BY name ASC;"""
        try:
            return self.cursor.execute(sql_command).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_all_single_type", message=f"load all types failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Alle Typen").message

    def get_single_type(self, raw_type_id: int, active: bool = True) -> tuple | str:
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
            debug.error(item=debug_str, keyword="get_raw_types", message=f"load raw types failed\n"
                                                                         f"command = {sql_command}\n"
                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Active Member Type").message

    def get_type_name_by_id(self, id_: int) -> tuple | str:
        try:
            v.validation.must_positive_int(int_=id_)
        except e.NoPositiveInt as error:
            return error.message

        sql_command: str = f"""SELECT name FROM type WHERE ID is ?;"""
        try:
            return self.cursor.execute(sql_command, (id_,)).fetchone()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_type_name_by_id", message=f"load single type failed\n"
                                                                               f"command = {sql_command}\n"
                                                                               f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Typ ID").message

    def get_id_by_type_name(self, raw_id: int, name: str) -> tuple | str:
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

    def get_member_data_by_id(self, id_: int, active: bool = True) -> dict | str:
        try:
            v.validation.must_positive_int(int_=id_)
            v.validation.must_bool(bool_=active)
        except (e.NoInt,e.NoPositiveInt, e.NoBool) as error:
            return error.message

        table: str = "v_active_member" if active else "v_inactive_member"
        sql_command: str = f"""SELECT * FROM {table} WHERE ID = ?;"""
        try:
            data = self.cursor.execute(sql_command, (id_,)).fetchone()
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

    # member nexus
    def get_phone_number_by_member_id(self, id_: int) -> tuple or None:
        sql_command: str = f"""SELECT ID,type_id,number FROM member_phone WHERE member_id is ?;"""
        try:
            return self.cursor.execute(sql_command, (id_,)).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_phone_number_by_member_id", message=f"load phone numbers failed\n"
                                                                                         f"command = {sql_command}\n"
                                                                                         f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_mail_by_member_id(self, id_: int) -> tuple or None:
        sql_command: str = f"""SELECT ID,type_id,mail FROM member_mail WHERE member_id is ?;"""
        try:
            return self.cursor.execute(sql_command, (id_,)).fetchall()
        except self.OperationalError as error:
            debug.error(item=debug_str, keyword="get_mail_by_member_id", message=f"load mails failed\n"
                                                                                 f"command = {sql_command}\n"
                                                                                 f"error = {' '.join(error.args)}")
            return e.LoadingFailed(info="Phone Number").message

    def get_position_by_member_id(self, id_: int) -> tuple or None:
        sql_command: str = f"""SELECT ID,type_id,_active FROM member_position WHERE member_id is ?;"""
        try:
            data: list = (self.cursor.execute(sql_command, (id_,)).fetchall())
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


def create_select_handler() -> None:
    global select_handler
    select_handler = SelectHandler()

# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler

from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h, \
    log_handler as l_h
from logic import validation as v
from config import error_code as e

import debug

debug_str: str = "GlobalHandler"

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()

    def __str__(self) -> str:
        return "GlobalHandler"

    @staticmethod
    def create_handler() -> None:
        s_h.create_select_handler()
        a_h.create_add_handler()
        u_h.crate_update_handler()
        d_h.create_delete_handler()
        l_h.create_log_handler()

    # member
    @staticmethod
    def get_member_data(id_: int, active: bool = True) -> dict | str:
        member_data: dict = s_h.select_handler.get_member_data_by_id(id_=id_, active=active)
        if isinstance(member_data, str):
            return member_data

        phone_data: tuple or None = s_h.select_handler.get_phone_number_by_member_id(id_=id_)
        if isinstance(phone_data, str):
            return phone_data

        mail_data: tuple or None = s_h.select_handler.get_mail_by_member_id(id_=id_)
        if isinstance(mail_data, str):
            return mail_data

        position_data: tuple or None = s_h.select_handler.get_position_by_member_id(id_=id_)
        if isinstance(position_data, str):
            return position_data

        data: dict = {
            "member_data": member_data,
            "phone": phone_data,
            "mail": mail_data,
            "position": position_data,
        }

        return data

    def update_member_data(self, id_: int, data: dict, log_date: int | None) -> str | dict:
        try:
            v.validation.must_dict(dict_=data)
        except e.NoDict as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message

        member_data: dict = data["member_data"]
        member_nexus_data: dict = data["member_nexus_data"]

        try:
            v.validation.update_member(data=member_data)
        except (e.NoDict, e.NoStr, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message

        id_bool = True
        if id_ is None:
            id_: int = a_h.add_handler.add_member(data=member_data, log_date=log_date)
            if isinstance(id_, str):
                return id_
            id_bool = False
        try:
            v.validation.must_positive_int(int_=id_, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message

        if id_bool:
            result = u_h.update_handler.update_member(id_=id_, data=member_data, log_date=log_date)
            if isinstance(result, str):
                return result

        ids = self._update_member_nexus(data=member_nexus_data, member_id=id_, log_date=log_date)
        if isinstance(ids, str):
            return ids

        ids["member_id"] = id_
        return ids

    # member nexus
    @staticmethod
    def _update_member_nexus(data: dict, member_id: int, log_date: int | None) -> str | dict:
        try:
            v.validation.must_dict(data)
        except e.NoDict as error:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
            return error.message

        try:
            phone = data["phone"]
            mail = data["mail"]
            position = data["position"]
        except KeyError:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = KeyError")
            return e.NoDict(info="Member Nexus").message

        # phone
        phone_ids: list = list()
        for ID, type_id, Type, phone_number in phone:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, phone_number], type_="phone")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result: str | None = u_h.update_handler.update_member_nexus_phone(ID=ID, number=phone_number,
                                                                                  log_date=log_date)
                if isinstance(result, str):
                    return result
                phone_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result: str | int = a_h.add_handler.add_member_nexus_phone(type_id=type_id, value=phone_number,
                                                                           member_id=member_id, log_date=log_date)
                if isinstance(result, str):
                    return result
                phone_ids.append(result)

        # mail
        mail_ids: list = list()
        for ID, type_id, Type, mail_ in mail:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, mail_], type_="mail")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result: str | None = u_h.update_handler.update_member_nexus_mail(ID=ID, mail=mail_, log_date=log_date)
                if isinstance(result, str):
                    return result
                mail_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result: str | int = a_h.add_handler.add_member_nexus_mail(type_id=type_id, value=mail_,
                                                                          member_id=member_id, log_date=log_date)
                if isinstance(result, str):
                    return result
                mail_ids.append(result)

        # position
        position_ids: list = list()
        for ID, type_id, Type, active in position:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, active], type_="position")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.NoBool, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result: str | None = u_h.update_handler.update_member_nexus_position(ID=ID, active=active)
                if isinstance(result, str):
                    return result
                position_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result: str | int = a_h.add_handler.add_member_nexus_position(type_id=type_id, value=active,
                                                                              member_id=member_id, log_date=log_date)
                if isinstance(result, str):
                    return result
                position_ids.append(result)

        # result
        return {
            "phone": phone_ids,
            "mail": mail_ids,
            "position": position_ids,
        }


def create_global_handler() -> None:
    global global_handler
    global_handler = GlobalHandler()

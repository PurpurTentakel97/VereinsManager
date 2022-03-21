# Purpur Tentakel
# 13.02.2022
# VereinsManager / Global Handler
import os

import bcrypt
from sqlite import select_handler as s_h, add_handler as a_h, update_handler as u_h, delete_handler as d_h, \
    log_handler as l_h
from logic import validation as v
from config import error_code as e
from helper import hasher

import debug

debug_str: str = "GlobalHandler"

global_handler: "GlobalHandler"


class GlobalHandler:
    def __init__(self) -> None:
        self.create_handler()

    @staticmethod
    def create_handler() -> None:
        s_h.create_select_handler()
        a_h.create_add_handler()
        u_h.crate_update_handler()
        d_h.create_delete_handler()
        l_h.create_log_handler()

    # member
    @staticmethod
    def get_member_data(ID: int, active: bool = True) -> [dict | str, bool]:
        member_data, valid = s_h.select_handler.get_member_data_by_id(ID=ID, active=active)
        if not valid:
            return member_data, False

        phone_data, valid = s_h.select_handler.get_phone_number_by_member_id(member_id=ID)
        if not valid:
            return phone_data, False

        mail_data, valid = s_h.select_handler.get_mail_by_member_id(member_id=ID)
        if not valid:
            return mail_data, False

        position_data, valid = s_h.select_handler.get_position_by_member_id(member_id=ID)
        if not valid:
            return position_data, False

        data: dict = {
            "member_data": member_data,
            "phone": phone_data,
            "mail": mail_data,
            "position": position_data,
        }

        return data, True

    def update_member_data(self, ID: int, data: dict, log_date: int | None) -> [str | dict, bool]:
        try:
            v.validation.must_dict(dict_=data)
        except e.NoDict as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message, False

        member_data: dict = data["member_data"]
        member_nexus_data: dict = data["member_nexus_data"]

        try:
            v.validation.update_member(data=member_data)
        except (e.NoDict, e.NoStr, e.NoPositiveInt, e.NoBool, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message, False

        id_bool = True
        if ID is None:
            ID, valid = a_h.add_handler.add_member(data=member_data, log_date=log_date)
            if not valid:
                return ID, False
            id_bool = False
        try:
            v.validation.must_positive_int(int_=ID, max_length=None)
        except (e.NoInt, e.NoPositiveInt, e.ToLong) as error:
            debug.error(item=debug_str, keyword="update_member_data", message=f"Error = {error.message}")
            return error.message, False

        if id_bool:
            result, valid = u_h.update_handler.update_member(ID=ID, data=member_data, log_date=log_date)
            if not valid:
                return result, False

        ids, valid = self._update_member_nexus(data=member_nexus_data, member_id=ID, log_date=log_date)
        if not valid:
            return ids, False

        ids["member_id"] = ID
        return ids, True

    # member nexus
    @staticmethod
    def _update_member_nexus(data: dict, member_id: int, log_date: int | None) -> [str | dict, bool]:
        try:
            v.validation.must_dict(data)
        except e.NoDict as error:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
            return error.message, False

        try:
            phone = data["phone"]
            mail = data["mail"]
            position = data["position"]
        except KeyError:
            debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = KeyError")
            return e.NoDict(info="Member Nexus").message, False

        # phone
        phone_ids: list = list()
        for ID, type_id, Type, phone_number in phone:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, phone_number], type_="phone")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message, False
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result, valid = u_h.update_handler.update_member_nexus_phone(ID=ID, number=phone_number,
                                                                             log_date=log_date)
                if not valid:
                    return result, False
                phone_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result, valid = a_h.add_handler.add_member_nexus_phone(type_id=type_id, value=phone_number,
                                                                       member_id=member_id, log_date=log_date)
                if not valid:
                    return result, False
                phone_ids.append(result)

        # mail
        mail_ids: list = list()
        for ID, type_id, Type, mail_ in mail:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, mail_], type_="mail")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message, False
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result, valid = u_h.update_handler.update_member_nexus_mail(ID=ID, mail=mail_, log_date=log_date)
                if not valid:
                    return result, False
                mail_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result, valid = a_h.add_handler.add_member_nexus_mail(type_id=type_id, value=mail_,
                                                                      member_id=member_id, log_date=log_date)
                if not valid:
                    return result, False
                mail_ids.append(result)

        # position
        position_ids: list = list()
        for ID, type_id, Type, active in position:
            try:
                v.validation.update_member_nexus(data=[ID, type_id, Type, active], type_="position")
            except (e.NoInt, e.NoPositiveInt, e.WrongLength, e.NoList, e.NoStr, e.NoBool, e.ToLong) as error:
                debug.error(item=debug_str, keyword="_update_member_nexus", message=f"Error = {error.message}")
                return error.message, False
            try:
                v.validation.must_positive_int(ID, max_length=None)
                result, valid = u_h.update_handler.update_member_nexus_position(ID=ID, active=active,
                                                                                log_date=log_date)
                if not valid:
                    return result, False
                position_ids.append(result)
            except (e.NoPositiveInt, e.NoInt, e.ToLong):
                result, valid = a_h.add_handler.add_member_nexus_position(type_id=type_id, value=active,
                                                                          member_id=member_id, log_date=log_date)
                if not valid:
                    return result, False
                position_ids.append(result)

        # result
        return {
                   "phone": phone_ids,
                   "mail": mail_ids,
                   "position": position_ids,
               }, True

    # User
    @staticmethod
    def save_update_user(data: dict) -> [int | str | None, bool]:
        try:
            v.validation.save_update_user(data=data)
        except (e.NoDict, e.NoStr, e.NoInt, e.NoPositiveInt, e.DifferentPassword, e.PasswordToShort,
                e.PasswordHasSpace, e.LowPassword, e.VeryLowPassword, e.ToLong, e.DefaultUserException) as error:
            debug.error(item=debug_str, keyword="save_update_user", message=f"Error = {error.message}")
            return error.message, False

        if data["ID"]:
            result, valid = u_h.update_handler.update_user(ID=data["ID"], data=data)
            if not valid:
                return result, False
            if data["password_1"] is not None:
                data["password_hashed"] = hasher.hash_password(data["password_1"])
                return u_h.update_handler.update_user_password(ID=data["ID"], password=data["password_hashed"])
        else:
            data["password_hashed"] = hasher.hash_password(data["password_1"])
            return a_h.add_handler.add_user(data=data)


def create_global_handler() -> None:
    global global_handler
    global_handler = GlobalHandler()
